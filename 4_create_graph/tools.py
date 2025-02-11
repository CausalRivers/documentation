import requests
import matplotlib.pyplot as plt
import requests
import numpy as np
import geopandas as gpd
import networkx as nx

import matplotlib as mpl

preprocess_path = '/home/datasets4/stein/rivers/processed/'
output_path = '/home/datasets4/stein/rivers/processed_recreation/'
crawl_path = "/home/datasets4/stein/rivers/crawl_saves/"


def get_elevation_of_point(coords):
    # api-endpoint
    URL = "https://api.open-meteo.com/v1/elevation?"
    URL += "latitude="
    URL += str(coords[0])
    URL += "&"
    URL += "longitude="
    URL += str(coords[1])
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    # extracting data in json format
    data = r.json()
    return data["elevation"]



def plot_current_state_of_graph(
    G,
    dpi=100,
    lim=(50, 52),
    limx=(9.8, 13.4),
    node_size=50,
    arrowsize=20,
    fs=(10, 10),
    font_size=1,
    save=False,
    river_map=0,
    ger_map=0,
    emphasize=[],
    label=True,
    arrowstyle="fancy",
    autozoom=None,
    width=1,
    show_edge_origin=False,
    hardcode_colors = [],
    ger_path = "visualization/geomaps/vg2500_bld.shp",
    river_path = 'visualization/german_rivers_bg.shp',
    extra_points = []
):
#

    pos = {x: np.flip(np.array(G.nodes[x]["p"][:2]).astype(float)) for x in G.nodes}

    fig, ax = plt.subplots(1, 1, figsize=fs)

    if ger_map:
        fp = ger_path
        map_df2 = gpd.read_file(fp)
        map_df2.plot(color="green", ax=ax, alpha=0.3, linewidth=5, edgecolor="black")

    if river_map:
        fp = river_path
        map_df = gpd.read_file(fp)
        map_df.plot(color="blue", alpha=0.3, ax=ax, linewidth=0.5, edgecolor='blue')


    if hardcode_colors: 
        colors = hardcode_colors
    else:        
        colors = []
        for x in G.nodes:
            if x in emphasize:
                colors.append("black")
            else:
                colors.append(G.nodes[x]["c"])
    if show_edge_origin:
        cmap = mpl.colormaps['Set1']
        ege_base_colors = cmap(np.linspace(0, 1, 8))
        edge_colors = []
        for x in G.edges:
            edge_colors.append(tuple(ege_base_colors[G.edges[x]["origin"]]))
    nx.draw_networkx(
        G,
        pos,
        with_labels=label,
        font_size=font_size,
        node_size=node_size,
        arrows=True,
        node_color=colors,
        arrowsize=arrowsize,
        edge_color= edge_colors if show_edge_origin else "black",
        #arrowstyle=arrowstyle,
        width=width,
        ax=ax,
    )
    if autozoom:
        ax.set_xlim(
            min([pos[x][0] for x in pos.keys()]) - autozoom,
            max([pos[x][0] for x in pos.keys()]) + autozoom,
        )
        ax.set_ylim(
            min([pos[x][1] for x in pos.keys()]) - autozoom,
            max([pos[x][1] for x in pos.keys()]) + autozoom,
        )
    else:
        ax.set_ylim(lim[0], lim[1])
        ax.set_xlim(limx[0], limx[1])

    if save:
        plt.savefig("saves/" + save + "_G.svg", dpi=dpi)  # , dpi= 500
        plt.close()

    ax.set_title("River Causal Benchmark")
    ax.set_frame_on(True)

    if len(extra_points):
        for ex in extra_points:
            ax.scatter(ex[0],ex[1],color="black")
            ax.annotate(ex[2], (ex[0],ex[1]))

    plt.show()