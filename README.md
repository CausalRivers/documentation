# Construction Pipeline for Rivers East Germany

This repo servers mainly for documentary purposes as the raw data is not mostly publicly available.

The following steps are performed to construct labels and time series for the Rivers East Germany benchmark. Steps are supdivided via numbers and should be executed in oder.

- 1_raw_data_processing: Here we perform an initial parse for both time series and meta data for each recieved dataproduct (each state provided data in a different format.)

- 2_wiki_crawls: Here we provide scripts to crawl wikipedia articles to gain information about naming, crossings and coordinates for various rivers.

- 3_unify_data_sources: Here we combine all data sources from 1 to a single meta data and a single time series product.

- 4_create_graph: Here we generate the actual ground truth graph based on subproduct from 3 and 2. Notably this is a dirty process that required a lot of manual labour which is specified in tools/handcrafted_info. Notably there were multiple rounds of quality control to ensure that all links are actually valid. We are quite confident that the graph is highly accurate.

- After this, we perform some quality control to ensure that all links are actually valid and create some visualization tools.

- Finally, we add additional edge information to the graph which can be used to subsample the giant graph.

Environment for all the processing can be installed via "construction_env.yml

# Currently included in the Dataset

<img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/States_of_Germany.svg" alt="drawing" width="300"/>

<a href="https://commons.wikimedia.org/wiki/User:Escondites">Escondites</a>, <a href="https://commons.wikimedia.org/wiki/File:States_of_Germany.svg">States of Germany</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/de/legalcode" rel="license">CC BY-SA 2.0 DE</a>

| State    | Current Progress |
| -------- | ------- |
| Brandenburg | We recieved a giant dataset including labels and 15 minute resolution (sent by hand) || Saxony-Anhalt | Downloaded by hand from: [portal](<https://gld.lhw-sachsen-anhalt.de/#(Gideon)>.|
| Saxony |Crawler for the API (last 5 years). Appropriate licensing was confirmed via e-mail|
| Berlin | After some discussion we got 10 stations with 15 minute resolution + meta (by hand). API works automatically for one year? <https://wasserportal.berlin.de/download/wasserportal_berlin_getting_data.pdf> |
| Thuringia |  We got a giant dataset including labels and 15 minute resolution (sent by hand) |
| Wasserstraßen Verband | We got personal access via <https://bscw.bund.de/pub/bscw.cgi/277364341?auth=3boYtEQY> to Data from the Elbe/Saale/Oder. More can be in principle requested.|
| Bavaria | High-resolution data is provided by the [Gewässerkundlicher Dienst Bayern](https://www.gkd.bayern.de/de/downloadcenter/wizard). By selecting individual periods of time, data in batches of at most 5 years becomes accessible. All measuring sites can be selected at once with the circle tool. Generating new download requests with cURL is trivial.|
| Mecklenburg Western Pomerania |  Data recieved (sent by hand)|
| Hessen | - |
| Northrhine-Westphalia | - |
| Rhineland Palatinate | - |
| Saarland | - |
| Baden-Württemberg | - |
| Hamburg |<ul><li>Data for all rivers except Elbe should be available from the WaBiHa for at least < 1 year (<https://www.wabiha.de/karte.html>, not machine-readable). Also, there exists a dataset with water levels <https://suche.transparenz.hamburg.de/dataset/pegel-an-binnengewaessern5> (appropriate license). However, the download link is currently not availabe. Data for the Elbe might be available here: <https://undine.bafg.de/elbe/zustand-aktuell/elbe_akt_WQ.html> or from WSV (see Bremen). Access for Hamburg data (likely except Elbe) requested, waiting for reply (Jan) |
| Bremen | <ul><li>Bremen does not seem to have its own measuring system but not all measurements within Bremen are included within the Lower Saxony data. </li><li>Some are also collected by federal authorities like the [WSV](https://www.wsa-weser-jade-nordsee.wsv.de/Webs/WSA/Weser-Jade-Nordsee/DE/Wasserstrassen/BauUnterhaltung/Gewaesserkunde/gewaesserkunde_node.html). </li><li>Long-term data for the WSV can be found under [here](https://www.kuestendaten.de/DE/Services/Messreihen_Dateien_Download/Download_Zeitreihen_node.html). Here, more recent data is up to minute-wise.</li></ul> |
| Lower Saxony | <ul><li>Access requested, in active contact (Gideon and Jan, contact is [Corinna Forberg](mailto:Corinna.Forberg@nlwkn.niedersachsen.de), on vacation until January 5, 2024)</li></ul> |
| Schleswig Holstein | <ul><li>Access requested, in active contact (Jan, contact is [Doris Wolf](mailto:Doris.Wolf@lkn.landsh.de))</li><li>Export will take a while (expect beginning / mid february) and will likely be limited to rivers with a certain size (area in sqm?). This size should be less than the official definition of a river (in distinction from a simple "Fließgewässer"). Data will likely start in the year 2000.</li><li>An overview of the stations including location can be found [here](https://hsi-sh.de/nuis/wafis/pegel/od/pegel.csv)</li></ul> |

# CausalRivers Benchmark Product Explanation

The product consists out of 3 networkx graphs, .3 meta data tables and 3 time series .csv. They share the same key (ID) to identify which node belongs to which time series.

Additionally, the meta data table contains information on the individual nodes.

- ID: Unique id
- R: River name
- X: X coordinate of measurement station
- Y: Y coordinate of measurement station
- D: Distance to the end of the river OR (in some cases) distance from the source (these are rare and we encoded them via negative numbers)
- H: Elevation of measurement station
- QD: Quality marker of the Distance
- QH: Quality marker of the Height
- QX: Quality marker of the X coordinate
- QY: Quality marker of the Y coordinate
- QR: Quality marker of the River name
- O: Origin of the node (data source)
- original_id: ID of the station in the raw data before unification and reindexing. These can be used, in combination with "0" to find the original station on the online services of the data providers (Ts likely only available for the last couple of weeks)

Further, both ground truth graph and edges hold additional informations.

### For nodes

- p: (X,Y coordinates)
- c: (color for consistency based on origin)
- origin: (origin of the node)
- H: as above
- R: as above
- D: as above
- QD: as above
- QH: as above
- QX: as above
- QY: as above
- QR: as above

### For edges

- h_distance: elevation change that appears between the two nodes
- km: euclidean distance between the two nodes
- quality_km: quality of the estimation. This depends on QX and QY of the nodes
- quality_h:  quality of the estimation. This depends on QH nodes
- origin: Through which strategy this edge was created. Further info below.

Quuality markers:

As the graph construction and especially the edge determination is consisting of multiple strategies, we provide quality markers for each information. Quality markers are defined as follows:

### For nodes

- -1: unknown as target value missing
- 0: original value
- Bigger than 0: Value that was estimated or looked up by hand. (Check construction pipeline for more details)

### For edges

- origin: The step under which the edge was added. E.g. origin 6 references to edges that were added as river splits by hand.
- quality_h: Sum of the quality of the corresponding Heights estimated of the connected nodes. E.g. 0 references that both height estimates were not estimated.
- quality_km: Sum of the quality of the corresponding coordinates(X,Y) estimated of the connected nodes. E.g. 0 references that both  coordinates were not estimated.
