import numpy as np


def distance(c1, c2):
    # Conversion X, Y to km distance (considering curvature)
    deglen = 110.25
    x = c1[0] - c2[0]
    y = (c1[1] - c2[1]) * np.cos(c1[0])
    return deglen * np.sqrt(x * x + y * y)


def find_river_flow_edges(lab):
    # simples walks down river based on height and river flow (TODO inconsistent!) and creates edges.
    edges = []
    for x in lab["R"].unique():
        if type(x) == str:
            single_river = lab.loc[lab["R"] == x].copy()
            c1 = single_river["D"].isnull().sum() == 0
            c2 = (single_river["D"] < 0).sum() == len(single_river)
            c3 = (single_river["D"] > 0).sum() == len(single_river)
            c4 = len(single_river["O"].unique()) == 1
            if c1 and c4 and (c2 or c3):
                single_river.sort_values(["D", "H"], ascending=False, inplace=True)
            else:
                single_river.sort_values(["H", "D"], ascending=False, inplace=True)
            single_river.reset_index(inplace=True)

            if len(single_river) > 0:

                for x in range(len(single_river) - 1):
                    lab.loc[single_river.iloc[x].ID, "Child found"] = 1

                    # # same sign
                    # if (single_river.iloc[x]["D"] * single_river.iloc[x+1]["D"]) >0:
                    #     distance_between = np.abs(single_river.iloc[x]["D"]- single_river.iloc[x + 1]["D"])

                    # elif np.isnan(single_river.iloc[x]["D"]) or np.isnan(single_river.iloc[x+1]["D"]):
                    #     distance_between = None
                    # else:
                    #     print("weird Distance combo detected.")
                    #     distance_between = None
                    #     print(x)

                    dist = eucl(
                        single_river.iloc[x]["X"],
                        single_river.iloc[x + 1]["X"],
                        single_river.iloc[x]["Y"],
                        single_river.iloc[x + 1]["Y"],
                    )

                    edges.append(
                        (
                            single_river.iloc[x].ID,
                            single_river.iloc[x + 1].ID,
                            {
                                "km": dist,
                                "h_distance": single_river.iloc[x]["H"]
                                - single_river.iloc[x + 1]["H"],
                                "quality_km": single_river.iloc[x]["QX"]
                                + single_river.iloc[x + 1]["QX"]
                                + single_river.iloc[x + 1]["QY"]
                                + single_river.iloc[x + 1]["QY"],
                                "quality_h": single_river.iloc[x]["QH"]
                                + single_river.iloc[x + 1]["QH"],
                                "origin": 1,
                            },
                        )
                    )
    return edges


def check_for_edge(r, G):
    # Now we need to find the end node.
    if len(G.edges(r)) == 0:
        return r, None, 1  # river unknown
    elif (
        len(G.edges(r)) > 1
    ):  # multiple endings of a river. this is a special case (shouldnt even occur based on the parsing.)
        end_river = list(G.edges(r))[1][1]
        return r, None, 2
    else:  # We found the single child node. return.
        end_river = list(G.edges(r))[0][1]
        return r, end_river, -1


def match_river(id, river, lab, G, big_rivers=None):
    # Tries to find the child river in the wiki graph.
    # we can specify bigger river systems for matching with big rivers (as this is what the naming scheme of Wiki does.)

    assert type(river) == str, "river should be a name"

    # Step 1: try to match the name to some node in the wiki graph.
    r = []
    if river in G.nodes:
        r.append(river)
    elif river + " (Fluss)" in G.nodes:
        r.append(river + " (Fluss)")
    # check for single infor bracket:
    elif len([x for x in G.nodes if river + " " in x]) == 1:
        r.append([x for x in G.nodes if river + " " in x][0])
    elif big_rivers:
        for big in big_rivers:
            c_river = river + " " + big
            if c_river in G.nodes:
                r.append(c_river)
    # Step 2: check if there is a child node. If there are multiple ones: Select properly.
    if len(r) == 0:  # River not found in G
        return None, None, 0

    if len(r) == 1:
        return check_for_edge(r[0], G)

    elif len(r) >= 2:

        # First step: We can filter rivers that have a higher end_point than the measurement station
        r = [x for x in r if lab.loc[id, "H"] > G.nodes[x]["h"]]

        # Next step. Location between measurement station and river end should be shortest
        # Not generally true but should be a good way to go.

        best = np.inf
        current = None
        river_name_selection = None
        for x in r:
            r, end_river, error = check_for_edge(x, G)
            if end_river:
                if G.nodes[r]["p"]:
                    eucl = (float(G.nodes[r]["p"][0]) - lab.loc[id, "X"]) ** 2 + (
                        float(G.nodes[r]["p"][1]) - lab.loc[id, "Y"]
                    ) ** 2
                    if eucl < best:
                        current = end_river
                        best = eucl
                        river_name_selection = r
        if best == np.inf:
            return None, None, 3
        else:
            return river_name_selection, current, -1


def find_next_river(lab, end_river):
    if end_river in lab["R"].unique():
        r = end_river
    elif end_river.split(" (")[0] in lab["R"].unique():
        r = end_river.split(" (")[0]
    else:
        return None, 4
    next_river = lab[lab["R"] == r].sort_values(["H", "D"], ascending=False)
    return next_river, -1


def eucl(X1, X2, Y1, Y2):
    return np.sqrt((X1 - X2) ** 2 + (Y1 - Y2) ** 2)


def create_edge(parent_node, relevant_nodes, lab, crossing_coords, origin=2):
    child_node = relevant_nodes.index[0]

    dist = eucl(
        lab.loc[parent_node, "X"],
        lab.loc[child_node, "X"],
        lab.loc[parent_node, "Y"],
        lab.loc[child_node, "Y"],
    )

    return (
        parent_node,
        child_node,
        {
            "h_distance": lab.loc[parent_node, "H"] - relevant_nodes["H"].values[0],
            "km": dist,
            "quality_km": lab.loc[parent_node, "QX"]
            + lab.loc[parent_node, "QY"]
            + lab.loc[child_node, "QX"]
            + lab.loc[child_node, "QY"],
            "quality_h": lab.loc[parent_node, "QH"] + relevant_nodes["QH"].values[0],
            "origin": origin,
        },
    )


def find_river_crossing(id, lab, G, big_rivers):
    # First option: clean finding.
    # Takes ID and return the edge information if existing, else none.
    parent_node = id
    river = lab.loc[id, "R"]

    # Attempts to find child river. (possible changes the river naming.)
    river, end_river, error_code = match_river(id, river, lab, G, big_rivers=big_rivers)
    if error_code >= 0:
        # No node found.
        return None, error_code

    # Now we need to find the End point.
    if not G.nodes[river]["h"]:
        return None, 4
    H = G.nodes[river]["h"][0]
    crossing_coords = G.nodes[river]["p"]
    # Now we need to find the id of the first point in the target river
    # that is lower than the hight of the crossing.
    next_river, error_code = find_next_river(lab, end_river)
    if error_code >= 0:
        return None, 5

    # Sort and find the node behind.
    relevant_nodes = next_river[next_river["H"] <= H].sort_values(
        ["H", "D"], ascending=False
    )
    if len(relevant_nodes) > 0:
        return create_edge(parent_node, relevant_nodes, lab, crossing_coords), -1
    else:
        return None, 6


def add_handcrafted_information(
    remain, additional_edges, additional_nodes, additional_height, lab, G, origin
):

    # 1. iter through the still available nodes in one state:
    to_add = []
    used_edges = []
    used_nodes = []
    for index, row in remain.iterrows():
        # 2. See if they have some handcrafted connection specified.
        match = np.where(additional_edges.T[0] == row["R"])[0]
        if len(match) > 0:
            # Check if we have infos on the river end or whether we need additional info from graph.
            river_end = additional_edges[match[0]][0]
            if river_end in [x[0] for x in additional_nodes]:
                river_end = [x for x in additional_nodes if x[0] == river_end][0]
                used_nodes.append(river_end)
                crossing_coords = river_end[1]
                H = additional_height[river_end[0]]

            elif river_end in G.nodes:
                river_end = [river_end, G.nodes[river_end]["p"]]
                H = G.nodes[river_end[0]]["h"][0]
                print("Check if the coords work here properly")
                crossing_coords = G.nodes[river_end[0]]["p"]

            else:
                print(index, "check that later. ")

            # 3. Check if the connection is directly in the final graph or whether matching via wiki graph is required:
            child = additional_edges[match[0]][1]
            if (child in lab["R"].values) or (child.split(" (")[0] in lab["R"].values):
                next_river = lab[lab["R"] == child]
                relevant_nodes = next_river[next_river["H"] <= H].sort_values(
                    ["H", "D"], ascending=False
                )
                if len(relevant_nodes) > 0:
                    edge = create_edge(
                        index, relevant_nodes, lab, crossing_coords, origin=origin
                    )
                    remain.loc[index, "Child found"] = 1
                    to_add.append(edge)
                    used_edges.append(list(additional_edges[match[0]]))
                else:  # Double jump required.
                    print(
                        row["R"]
                        + " might need double jump. If this happens a lot attempt to automate"
                    )
                # child = match_river(id,river,lab, G, big_rivers=None)
            else:
                print("Specified child wasnt found. Do by hand.")
    return to_add, remain, used_edges, used_nodes


def find_river_crossing_if_crossing_behind_last_measure(
    id, lab, G, current_G, big_rivers
):
    # Attempts to find child node for crossings after last measurements.
    # We know at least for the first iteration that the crossing is known

    parent_node = id
    river = lab.loc[id, "R"]

    # Attempts to find child river. (possible changes the river naming.)
    end_river, river, error_code = find_end_river(river, G, big_rivers=big_rivers)
    next_river, error_code = find_next_river(lab, end_river)

    # Now we know that there is no station in this river.
    # We therefore need to find the child node of the last river here.
    # This will also be the child of the current node
    # Check if the last node has a child node.
    existing_edge = current_G.edges(next_river.index[-1])
    if len(existing_edge) > 0:
        return (
            parent_node,
            list(existing_edge)[0][1],
            {
                "h_distance": lab.loc[parent_node, "H"]
                - lab.loc[list(existing_edge)[0][1], "H"],
                "km": lab.loc[parent_node, "D"],
            },
        ), -1
    else:
        return None, 8
