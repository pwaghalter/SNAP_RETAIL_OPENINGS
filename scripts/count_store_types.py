# PURPOSE OF THIS SCRIPT IS TO GENERATE EXPECTED NUMBER OF JOBS CREATED PER COUNTY PER YEAR USING EMPLOYMENT MODEL

# have a file  with what opened in each county - aka how many of each type, and what year
# have a file with expected num jobs created by each opening in a year
# look one year at a time
# for each county: create dict with key: year data: counter, key=store type
# write file: county, year w greatest expected delta, greatest expected delta

import sys
from collections import Counter, defaultdict

retailers = sys.argv[1]

#structure of dict: counties[county][year][store_type]=count of store type in that year in that county
counties = defaultdict(lambda: defaultdict(Counter))

# iterate through retailers file and use year of opening and store type to calculate num new job expected per year per county
with open(retailers) as r:

      for line in r:
          fields = line.split("|")
          #dict of counties, each county has dict of years, each year has count of each store type

          # increment county of store type for each year for each county
          counties[fields[15]][fields[13][-4:]][fields[2]]+=1

# file format: COUNTY|YEAR|STORE_TYPE,NUM_STORES|

# write the data to stdout, so that each county and year is followed by store types and number of that store type in that county in that year
for county in counties:

    for year in counties[county]:

        # county|year|
        line=str(county).strip()+"|"+str(year)+"|"
        
        for store_type in counties[county][year]:

            # store_type|num_stores|
            line += str(store_type)+","+str(counties[county][year][store_type])+"|"

        # write to stdout
        print(line)


        

         
