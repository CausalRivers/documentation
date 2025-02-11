# Step 1 - Raw data processing


!THIS REPO IS FOR DOCUMENTARY PURPOSES ONLY. RAW DATA IS NOT AVAILABLE PUBLICLY.

As the data is recored by each state and agency individually we require custom data preparation. 

The parsing for each state is performed individually and it is then later unified.

For each state, the origin of the data and how it was provided is specified. 

Importantly, not all data sources a publicly accessible.

All data sources are exported in a consistent manner here.


### Meta data format: 

- ID
- River Name
- X coord
- y coord
- Z coord
- distance to river end (or to the beginning. Inconsistent but is unified later.)
- We also create some quality markers (whether some value is estimated or provided)


###  Time series format: 

datetime index and river id (+ state marker) as columns 






# Current Progress by State

<img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/States_of_Germany.svg" alt="drawing" width="300"/>

<a href="https://commons.wikimedia.org/wiki/User:Escondites">Escondites</a>, <a href="https://commons.wikimedia.org/wiki/File:States_of_Germany.svg">States of Germany</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/de/legalcode" rel="license">CC BY-SA 2.0 DE</a> 


| State    | Current Progress |
| -------- | ------- |
| Brandenburg | We recieved a giant dataset including labels and 15 minute resolution (sent by hand) || Saxony-Anhalt | Downloaded by hand from: [portal](https://gld.lhw-sachsen-anhalt.de/#(Gideon).|
| Saxony |Crawler for the API (last 5 years). Appropriate licensing was confirmed via e-mail|
| Berlin | After some discussion we got 10 stations with 15 minute resolution + meta (by hand). API works automatically for one year? https://wasserportal.berlin.de/download/wasserportal_berlin_getting_data.pdf |
| Thuringia |  We got a giant dataset including labels and 15 minute resolution (sent by hand) |
| Wasserstraßen Verband | We got personal access via https://bscw.bund.de/pub/bscw.cgi/277364341?auth=3boYtEQY to Data from the Elbe/Saale/Oder. More can be in principle requested.|
| Bavaria | High-resolution data is provided by the [Gewässerkundlicher Dienst Bayern](https://www.gkd.bayern.de/de/downloadcenter/wizard). By selecting individual periods of time, data in batches of at most 5 years becomes accessible. All measuring sites can be selected at once with the circle tool. Generating new download requests with cURL is trivial.|
| Mecklenburg Western Pomerania |  Data recieved (sent by hand)|
| Hessen | - |
| Northrhine-Westphalia | - |
| Rhineland Palatinate | - |
| Saarland | - |
| Baden-Württemberg | - |
| Hamburg |<ul><li>Data for all rivers except Elbe should be available from the WaBiHa for at least < 1 year (https://www.wabiha.de/karte.html, not machine-readable). Also, there exists a dataset with water levels https://suche.transparenz.hamburg.de/dataset/pegel-an-binnengewaessern5 (appropriate license). However, the download link is currently not availabe. Data for the Elbe might be available here: https://undine.bafg.de/elbe/zustand-aktuell/elbe_akt_WQ.html or from WSV (see Bremen). Access for Hamburg data (likely except Elbe) requested, waiting for reply (Jan) |
| Bremen | <ul><li>Bremen does not seem to have its own measuring system but not all measurements within Bremen are included within the Lower Saxony data. </li><li>Some are also collected by federal authorities like the [WSV](https://www.wsa-weser-jade-nordsee.wsv.de/Webs/WSA/Weser-Jade-Nordsee/DE/Wasserstrassen/BauUnterhaltung/Gewaesserkunde/gewaesserkunde_node.html). </li><li>Long-term data for the WSV can be found under [here](https://www.kuestendaten.de/DE/Services/Messreihen_Dateien_Download/Download_Zeitreihen_node.html). Here, more recent data is up to minute-wise.</li></ul> |
| Lower Saxony | <ul><li>Access requested, in active contact (Gideon and Jan, contact is [Corinna Forberg](mailto:Corinna.Forberg@nlwkn.niedersachsen.de), on vacation until January 5, 2024)</li></ul> |
| Schleswig Holstein | <ul><li>Access requested, in active contact (Jan, contact is [Doris Wolf](mailto:Doris.Wolf@lkn.landsh.de))</li><li>Export will take a while (expect beginning / mid february) and will likely be limited to rivers with a certain size (area in sqm?). This size should be less than the official definition of a river (in distinction from a simple "Fließgewässer"). Data will likely start in the year 2000.</li><li>An overview of the stations including location can be found [here](https://hsi-sh.de/nuis/wafis/pegel/od/pegel.csv)</li></ul> |





# Construction pipeline

1. We first pipe all the data sources in a common format. It is saved as "processed"
2. We perform a wiki crawl to generate a graph. It is saved under "crawl_saves"
