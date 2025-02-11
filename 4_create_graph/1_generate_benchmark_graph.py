import pandas as pd
import pickle
import networkx as nx


from tools import preprocess_path, output_path, crawl_path


from tools import (
    plot_current_state_of_graph,
    get_elevation_of_point,
)
from graph_construction_tools import (
    find_river_crossing,
    find_river_flow_edges,
    create_edge,
    match_river,
    find_next_river,
    add_handcrafted_information,
)
import numpy as np

from handcrafted_info import (
    saxony_node_name_corrections,
    thuringia_node_name_corrections,
    brandenburg_node_name_corrections,
    saxony_anhalt_node_name_corrections,
    berlin_node_name_corrections,
)

from handcrafted_info import (
    saxony_additional_nodes,
    thuringia_additional_nodes,
    brandenburg_additional_nodes,
    saxony_anhalt_additional_nodes,
    berlin_additional_nodes,
)

from handcrafted_info import (
    saxony_additional_edges,
    thuringia_additional_edges,
    brandenburg_additional_edges,
    saxony_anhalt_additional_edges,
    berlin_additional_edges,
)

from handcrafted_info import (
    sink_rivers,
    state_placeholder_edges,
    ignore_rivers,
    edges_by_hand,
    confounding,
    quality_control_add,
    quality_control_remove,
)


color_map = {
    "T": "darkred",
    "S": "darkgreen",
    "SA": "Navy",
    "BR": "yellow",
    "B": "orange",
    "PH": "pink",
    "BSCV": "violet",
    "BA": "Skyblue",
    "MV": "brown",
}


def plot_state(G, l):
    plot_current_state_of_graph(
        G,
        dpi=500,
        autozoom=False,
        lim=(50, 53.7),
        limx=(9.8, 15.5),
        node_size=30,
        save=l,
        river_map=True,
        ger_map=1,
        arrowsize=10,
        fs=(10, 10),
        font_size=1,
        emphasize=[],
    )


def main():

    path = preprocess_path

    plotting = False
    # Infos to join.
    lab = pd.read_csv(path + "meta_joined_final.csv", index_col=0)

    for to_cast in ["X", "Y", "D", "H"]:
        lab[to_cast] = lab[to_cast].astype(float)
    for to_cast in ["QX", "QY", "QD", "QH"]:
        lab[to_cast] = lab[to_cast].astype(int)
    for to_cast in ["R", "QR", "O"]:
        lab[to_cast] = lab[to_cast].astype(str)

    # Filter Bavaria from the benchmark set:
    lab = lab.loc[~(lab["O"].isin(["BA"]))]
    print(crawl_path)
    # Load the graph that specifies wiki information
    G = pickle.load(open(crawl_path + "base_G.pickle", "rb"))
    # For accurate matching we need some grouped list of rivers per state
    state_river_list = pickle.load(open(crawl_path + "seperated_river_names.p", "rb"))
    state_river_list = {
        key: ["(" + x.split(" (")[-1] for x in state_river_list[key].keys()]
        for key in state_river_list
    }
    print(state_river_list.keys())
    # mno list available as it is not as wiki state category
    state_river_list["BSCV"] = []
    print(lab.isnull().sum())

    assert (
        lab.isnull().sum()[[x for x in lab.columns if x != "D"]].max() == 0
    ), "Data issues, empty fields detected."

    # Error corrections from previous steps. Infos optained by hand. These are naming changes that help with the wiki info matching later.
    for x in saxony_node_name_corrections:
        lab.loc[(lab["R"] == x[0]) & (lab["O"] == "S"), "R"] = x[1]
    for x in thuringia_node_name_corrections:
        lab.loc[(lab["R"] == x[0]) & (lab["O"] == "T"), "R"] = x[1]
    for x in brandenburg_node_name_corrections:
        lab.loc[(lab["R"] == x[0]) & (lab["O"] == "BR"), "R"] = x[1]
    for x in berlin_node_name_corrections:
        lab.loc[(lab["R"] == x[0]) & (lab["O"] == "B"), "R"] = x[1]
    for x in saxony_anhalt_node_name_corrections:
        lab.loc[(lab["R"] == x[0]) & (lab["O"] == "SA"), "R"] = x[1]

    print(lab)

    # Fix to prevent edges between equally named rivers
    # Single occation of double name in the same state. Add this systematically if this happens more often:
    lab.loc[lab["original_id"] == "id_" + "5874100", "R"] = "Temnitz (Plane)"
    lab.loc[lab["original_id"] == "id_" + "5895001", "R"] = "Temnitz (Rhin)"
    lab.loc[lab["original_id"] == "id_" + "422300", "R"] = "Schwarza (Hasel)"
    lab.loc[lab["original_id"] == "id_" + "5874100", "QR"] = 1
    lab.loc[lab["original_id"] == "id_" + "5895001", "QR"] = 1
    lab.loc[lab["original_id"] == "id_" + "422300", "QR"] = 1

    # The graph.
    station_G = nx.DiGraph()
    print("adding nodes...")

    # First step: We add all measurement stations that we have as nodes:
    to_add = []
    for ind, line in lab.iterrows():
        to_add.append(
            (
                ind,
                {
                    "p": (line["X"], line["Y"]),
                    "c": color_map[line["O"]],
                    "origin": line["O"],
                    "H": line["H"],
                    "R": line["R"],
                    "D": line["D"],
                    "QH": line["QH"],
                    "QD": line["QD"],
                    "QX": line["QX"],
                    "QY": line["QY"],
                    "QR": line["QR"],
                },
            )
        )
    station_G.add_nodes_from(to_add)
    print("Nodes in graph: " + str(len(station_G.nodes)))

    # From here on, links are added.
    lab["Child found"] = 0

    if plotting:
        plot_state(station_G, "3")
    ##############
    print("adding river flows...")
    edges = find_river_flow_edges(lab)
    station_G.add_edges_from(edges)
    print("Found " + str(lab["Child found"].sum()) + " links...")
    remain = lab[lab["Child found"] == 0]
    # check if there are still double rivers: If yes, this requires special attention. shouldnt be.
    assert remain["R"].value_counts().max() == 1, "river flow not proper."
    if plotting:
        plot_state(station_G, "4")

    ##############
    # Now we try to match the child river.
    # We save here at which point the matching pipeline failed to fix it later.
    remain = remain.assign(problem_code=-1)
    # Now we go through every remainer and try to allocate the child river.
    print("adding river crossings...")
    to_add = []
    for index, row in remain.iterrows():
        edge, error_code = find_river_crossing(
            index,
            lab,
            G,
            big_rivers=list(set(state_river_list[row["O"]])),
        )
        if edge:
            to_add.append(edge)
            remain.loc[index, "Child found"] = 1
        elif error_code != -1:
            remain.loc[index, "problem_code"] = error_code
        else:
            print("This should not happen.")
    assert (remain["Child found"].sum() + (remain["problem_code"] != -1).sum()) == len(
        remain
    ), "Some nodes has no prolem code but also no match"

    station_G.add_edges_from(to_add)
    print("Found " + str(len(to_add)) + " links...")
    remain = remain[remain["Child found"] == 0]
    if plotting:
        plot_state(station_G, "5")

    ###############
    # Next, we mark some garantueed sink rivers.
    no_edges = 0
    print("Marking garantueed sinks...")
    remain.loc[remain["R"].isin(sink_rivers), "Child found"] = 1
    no_edges += len(remain.loc[remain["R"].isin(sink_rivers), "Child found"])
    remain = remain[remain["Child found"] == 0]
    print("Remaining unconnected: " + str(len(remain)))
    print(
        "Marking Rivers that end in other states (This should be adapted when new data is available)..."
    )
    condition = remain["R"].isin(
        [x[0].split(" (")[0] for x in state_placeholder_edges]
    ) | remain["R"].isin([x[0] for x in state_placeholder_edges])
    remain.loc[condition, "Child found"] = 1
    no_edges += condition.sum()
    remain = remain[remain["Child found"] == 0]
    print("Remaining unconnected: " + str(len(remain)))
    print(no_edges)

    print("Marking weird stations as done...")  # (these are fixed later)
    remain.loc[remain["R"].isin(ignore_rivers), "Child found"] = 1
    no_edges += len(remain.loc[remain["R"].isin(ignore_rivers), "Child found"])
    remain = remain[remain["Child found"] == 0]
    print("Remaining unconnected: " + str(len(remain)))
    print("Categories:")
    print(remain["problem_code"].value_counts())

    ##############

    print("Remaining unconnected: " + str(len(remain)))
    print("Categories:")
    print(remain["problem_code"].value_counts())
    print("0: Failed to match river in Wiki graph")
    print(
        "6: Crossing after the last measurement of the child river. This needs matching further to the next river"
    )
    print("5: Cant find river specified by wiki graph in the station table")
    print("1: There is no edge specified in the wiki graph. Node exists however.")
    print("adding handcrafted fixes...")

    additional_edges = (
        saxony_additional_edges
        + thuringia_additional_edges
        + brandenburg_additional_edges
        + saxony_anhalt_additional_edges
        + berlin_additional_edges
    )

    additional_edges = np.array(additional_edges)

    additional_nodes = (
        saxony_additional_nodes
        + thuringia_additional_nodes
        + brandenburg_additional_nodes
        + saxony_anhalt_additional_nodes
        + berlin_additional_nodes
    )
    # Generate this information or save it from cache.
    try:
        additional_height = pickle.load(open(crawl_path + "additional_height.p", "rb"))
    except:
        additional_height = {}
    for x in additional_nodes:
        if x[0] in additional_height:
            pass
        else:
            additional_height[x[0]] = get_elevation_of_point(
                np.array(x[1]).astype(str)
            )[0]
    pickle.dump(additional_height, open(crawl_path + "additional_height.p", "wb"))

    to_add, remain, used_edges, used_nodes = add_handcrafted_information(
        remain, additional_edges, additional_nodes, additional_height, lab, G, origin=3
    )
    station_G.add_edges_from(to_add)
    print("Found " + str(len(to_add)) + " links...")
    remain = remain[remain["Child found"] == 0]

    print("Remaining unconnected: " + str(len(remain)))
    print("Edges in graph: " + str(len(station_G.edges())))

    print("Categories:")
    print(remain["problem_code"].value_counts())

    if plotting:
        plot_state(station_G, "6")

    ##########

    print(
        "Adding special river crossings..."
    )  # crossing is after the last measurement of the child river.
    # We check if we can match the next river in line.
    # #We only do one recursive jump to not overcomplicate this here.
    print("Only 1 jump instead of recursive.")
    to_add = []
    for index, row in remain[remain["problem_code"] == 6].iterrows():
        river = row["R"]
        id = index

        river, end_river, error_code = match_river(
            id,
            river,
            lab,
            G,
            big_rivers=list(set(state_river_list[row["O"]])),
        )
        next_river, error_code = find_next_river(lab, end_river)

        river, end_river, error_code = match_river(
            next_river.index[0],
            next_river["R"].values[0],
            lab,
            G,
            big_rivers=list(set(state_river_list[row["O"]])),
        )
        if error_code >= 0:
            continue
        else:
            H = G.nodes[river]["h"][0]
            next_river, error_code = find_next_river(lab, end_river)
            if isinstance(next_river, pd.DataFrame):
                relevant_nodes = next_river[next_river["H"] <= H].sort_values(
                    ["H", "D"], ascending=False
                )

                if len(relevant_nodes) > 0:
                    to_add.append(
                        create_edge(
                            id, relevant_nodes, lab, crossing_coords=None, origin=4
                        )
                    )
                    remain.loc[index, "Child found"] = 1
                else:
                    print("one more step night be necessary? Double check.")

    station_G.add_edges_from(to_add)
    print("Found " + str(len(to_add)) + " links...")
    remain = remain[remain["Child found"] == 0]

    print("Remaining unconnected: " + str(len(remain)))
    print("Edges in graph: " + str(len(station_G.edges())))

    print("Categories:")
    print(remain["problem_code"].value_counts())

    if plotting:
        plot_state(station_G, "7")

    ##############

    #############
    # At the end we import handcrafted rules for the remaining links.
    print("Build in Edges specified by hand...")
    edges = []
    mark_as_done = []
    for x in edges_by_hand:
        id_1 = lab.loc[lab["original_id"] == "id_" + str(x[0]), "R"].index
        if len(id_1) == 0:
            print("Failed rule: ", x)
            continue
        if id_1[0] not in remain.index.values:
            print(x)
        else:
            if x[1]:
                id_2 = lab.loc[lab["original_id"] == "id_" + str(x[1]), "R"].index
                if len(id_2) == 0:
                    print("Failed rule: ", x)
                    continue
                edges.append(
                    create_edge(id_1[0], lab.loc[[id_2[0]]], lab, None, origin=5)
                )
            else:
                no_edges += 1
        mark_as_done.append(id_1[0])
    remain.loc[remain.index.isin(mark_as_done), "Child found"] = 1
    remain = remain[remain["Child found"] == 0]

    station_G.add_edges_from(edges)

    print("Remaining unconnected: " + str(len(remain)))
    print("Edges in graph: " + str(len(station_G.edges())))

    print("Nodes in graph: " + str(len(list(station_G.nodes))))
    print("Edges in graph: " + str(len(station_G.edges())))
    print("Edges that should miss: " + str(no_edges))

    if plotting:
        plot_state(station_G, "8")

    ############
    print("All nodes should be connected now:")
    print(remain)
    print("We further have some additional confounding (river splits).")

    for x in confounding:
        id_1 = lab.loc[lab["original_id"] == "id_" + str(x[0]), "R"].index
        id_2 = lab.loc[lab["original_id"] == "id_" + str(x[1]), "R"].index
        if len(id_1) == 0 or len(id_2) == 0:
            continue
        edges.append(create_edge(id_1[0], lab.loc[[id_2[0]]], lab, None, origin=6))
    station_G.add_edges_from(edges)
    print("Nodes in graph: " + str(len(list(station_G.nodes))))
    print("Edges in graph: " + str(len(station_G.edges())))

    # Check if rivers has single
    print("Check remaining rules that should be added.(Nothing should pop up here)")

    remaining_edge_info = [
        list(x) for x in additional_edges if list(x) not in used_edges
    ]
    print(remaining_edge_info)

    print("#############")
    remaining_node_info = [
        list(x) for x in additional_nodes if list(x) not in used_nodes
    ]
    print(remaining_node_info)

    # Here we edit single links by hand to correct for previous mistakes (mostly through flow or height errors)
    print("######")
    print("Performing handcrafted changes: ")
    station_G.remove_edges_from(quality_control_remove)

    to_add = [
        create_edge(x[0], lab.loc[[x[1]]], lab, None, origin=7)
        for x in quality_control_add
    ]
    station_G.add_edges_from(to_add)

    print("Done.")

    pickle.dump(station_G, open(output_path + "station_G.p", "wb"))
    remain.to_csv(output_path + "no_finished_stations.csv")

    print("Fix the rest by hand.")


if __name__ == "__main__":
    main()
