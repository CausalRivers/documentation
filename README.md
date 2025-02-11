## Construction Pipeline for Rivers East Germany



The following steps are performed to construct labels and time series for the Rivers East Germany benchmark. Steps are supdivided via numbers. 


- 1_raw_data_processing: Here we perform an initial parse for both time series and meta data for each recieved dataproduct (each state provided data in a different format.)

- 2_wiki_crawls: Here we provide scripts to crawl wikipedia articles to gain information about naming, crossings and coordinates for various rivers.

- 3_unify_data_sources: Here we combine all data sources from 1 to a single meta data and a single time series product.

- 4_create_graph: Here we generate the actual ground truth graph based on subproduct from 3 and 2. Notably this is a dirty process that required a lot of manual labour which is specified in tools/handcrafted_info. Notably there were multiple rounds of quality control to ensure that all links are actually valid. While this cannot be 100% garantueed we are quite confident that the graph is highly accurate.

- Finally, we perform some quality control to ensure that all links are actually valid and create some visualization tools. 