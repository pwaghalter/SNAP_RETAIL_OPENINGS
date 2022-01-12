# THE PURPOSE OF THIS SCRIPT IS TO CALCULATE THE TOTAL POPULATION PER COUNTY

import sys
import gzip
from collections import defaultdict as dd

# argv[1] = ZIP_COUNTY_092021.csv
# argv[2] = IncomePop.gz

# iterate through data which maps zip codes to counties and create dict
zip_county = {}
with open(sys.argv[1]) as c:
    for line in c:
        temp = line.split(",")[0:2]

        # there are some lines in the data not needed
        try:
            # try casting to int to make sure both zip and county are legitimate; there are some strings in the data which are not zips or counties
            int(temp[0])
            int(temp[1])
            zip_county[temp[0]] = temp[1]
        except: pass # there are some strings in the file that should not be included - they won't cast to int, so we'll skip them


# count pop of each county
# iterate through the population of the zip codes and aggregate to county level
county_pop_dict = dd(lambda: 0)

with gzip.open(sys.argv[2], "rt") as county_pop:
    for line in county_pop:
        line = line.split("|")

        if line[0] in zip_county:
            county = zip_county[line[0]]
            pop = line[3]

            # sum population of zip code to corresponding county population
            county_pop_dict[county]+=int(pop)

# print data to stdout
for county in county_pop_dict: print(county,county_pop_dict[county], sep="|")


