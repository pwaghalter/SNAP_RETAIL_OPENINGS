# PURPOSE OF THIS SCRIPT IS TO ADD INCOME CLASSIFICATIONT TO EACH COUNTY THAT WILL BE GRAPHED
import sys

counties = sys.argv[1]

# load county and class to dict for O(1) lookup
county_classes = open(sys.argv[2])
county_class_dict = dict(line.strip().split("|")[0:3:2] for line in county_classes)

# iterate through the data, which is formated as COUNTY|expected_change|actual_change, and tag it with income classification calculated earlier
with open(counties) as r:
    for line in r:
        # get the county
        temp=line
        line = line.strip().split("|")
        county = line[0]

        # tag county with income class
        if county in county_class_dict:
            class_ = county_class_dict[county]

            # write to stdout
            print(temp.strip()+"|"+ class_)

        
