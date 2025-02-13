# Step 1 - Raw data processing

!THIS REPO IS FOR DOCUMENTARY PURPOSES ONLY. RAW DATA IS NOT AVAILABLE PUBLICLY.

As the data is recorded by each state and agency individually we require custom data preparation.

The parsing for each state is performed individually and it is then later unified.

For each state, the origin of the data and how it was provided is specified.

Importantly, not all data sources a publicly accessible.

All data sources are exported in a consistent manner here.

## Meta data format

- ID
- River Name
- X coord
- y coord
- Z coord
- distance to river end (or to the beginning. Inconsistent but is unified later.)
- We also create some quality markers (whether some value is estimated or provided)

### Time series format

datetime index and river id (+ state marker) as columns

### Current Progress by State

Please see the main [readme](/README.md).

### Construction pipeline

1. We first pipe all the data sources in a common format. It is saved as "processed"
2. We perform a wiki crawl to generate a graph. It is saved under "crawl_saves"
