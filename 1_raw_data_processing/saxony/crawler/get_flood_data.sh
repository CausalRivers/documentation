# here we completely crawl and preprocess flood data
# everything will be saved locally but can later be copied somewhere else
# But fear not, the standard paths are in the .gitignore

# step 1:   crawl saxony data for the Elbe flood region
#           for this we use the Hochwasser metadata.
#           also we crawl until the current day. 
#           if you do not want this set the --end_date             
python saxony_crawler.py --credentials credentials.json --resolution Ziel --start_date 2024-09-09 --stammdaten ../Stammdaten_Hochwasser.csv

# step 2:   download the pegelonline data under https://www.pegelonline.wsv.de/gast/pegeltabelle/download?messgroesse_ids=1966,1969,1967,1968&parameter=8
#           best is the csv format. Also unzip it and copy it to ./raw_manual/pegelonline.csv
#           if you save it somewhere else, then use --raw_path path/to/pegelonline-raw in step 3
echo "********************************************"
echo "* I hope you downloaded the manual data :) *"
echo "********************************************"

# step 3:   format and unify the manual data
python format_raw_manual.py

# step 4:   format everything into the Gideon format
python data_preparation.py