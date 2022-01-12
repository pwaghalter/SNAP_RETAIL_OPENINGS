# PURPOSE OF THIS FILE IS TO FIND THE SINGLE YEAR FOR EACH COUNTY WITH THE GREATEST EXPECTED NUMBER OF JOBS CREATED

from collections import defaultdict as dd
import sys

input = sys.argv[1]
model = sys.argv[2]

greatest_expected = dd(lambda: (0,0))
e_model = dd(lambda: 0)

# load employment model into dictionary for easy access
with open(model) as m:
    model_list = m.read().split("\n")

    for ml in model_list:
        ml = ml.split("|")

        # ignore blank line
        if len(ml)>1:
            try: e_model[ml[0]]=float(ml[1])

            # store types with no employment info are ingnored
            except: e_model[ml[0]]=0

with open(input) as i:
        # iterate through the counties and get total expected jobs per county
        for line in i:
            fields = line.split("|")

            county = fields[0]
        
            year = fields[1]

            num_jobs = 0

            try: year = int(year)
            except: year = 0

            # only have actual data starting in 1989-2020 (marking 2018 bc of two year intervals, so latest start date can be 2018)
            if year>=1989 and year<=2018:
                # add up total num jobs expected by looking at how many of each store type opened and multiplying by expected jobs per store
                for row in fields[2:]:
                    row = row.split(",")
                    if len(row)>1:
                        store_type, count = row[0], int(row[1])

                        # use model to predict how many new jobs should be created
                        num_jobs += e_model[store_type]*count

                # check if year has more expected jobs than previous max
                if num_jobs > greatest_expected[county][1]:
                    greatest_expected[county]=(year, num_jobs)

# load this information to stdout
for key, data in greatest_expected.items():

        line = str(key)+"|"+str(data[0])+"|"+str(data[1])
        print(line)        
            
