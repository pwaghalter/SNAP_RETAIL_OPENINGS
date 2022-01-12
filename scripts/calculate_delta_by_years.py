# THE PURPOSE OF THIS SCRIPT IS TO CALCULATE THE CHANGE IN NUMBER OF PEOPLE ON SNAP FOR EACH YEAR FROM JANUARY TO JANUARY BY DISTRICT
# FILE NAME IS YEARS AND INSIDE WILL BE DISTRICT FOLLOWED BY DELTA

from collections import defaultdict as dd
import sys

snap_dir = sys.argv[1]
output = sys.argv[2]

# creating a directory filled with files which just have counties and their deltas - each file corresponds with a set of 2 years
def generate_list_snap_ppl(data):
    
    with open(data) as fyd:
        snap_ppl = {}
        
        # the first 4 lines of each file are just set up, not data, so ignore them
        num=0
        for line in fyd:

            if num>3:

                fields = line.split(",,")
                
                # each file has one line that is a system automated estimate and irrelevant to this project
                if len(fields)>2:
                    county = fields[0].split(" ")[0][0:5]
                    
                    # second field is total people on SNAP, regardless of other welfare benefits
                    try: snap_ppl[county] = int(fields[2])

                    # empty field
                    except: snap_ppl[county] = 0

            num+=1

        return snap_ppl

# have data from 1989-2020
for i in range(1989, 2019):

    # looking at 2 year intervals
    first_yr = i
    second_yr = i+2

    # find data for start and end dates in order to calculate deltas
    first_yr_data = snap_dir + str(first_yr) + ".csv"
    second_yr_data = snap_dir + str(second_yr) + ".csv"

    # get just the number of ppl on snap in first yr from the file
    start_yr_snap_ppl = generate_list_snap_ppl(first_yr_data)

    # get just the number of ppl on snap in second yr from the file
    end_yr_snap_ppl = generate_list_snap_ppl(second_yr_data)

    # at this point, have each county and the delta of num ppl on snap from start yr to end yr
    start_end_deltas = {key: start_yr_snap_ppl[key] - end_yr_snap_ppl.get(key, 0) for key in start_yr_snap_ppl}

    #write the county and delta ppl on snap to file
    file_path = output+str(first_yr)+"_"+str(second_yr)

    with open(file_path, 'w') as fp:
        fp.write("COUNTY|DELTA\n")
        
        for county, delta in start_end_deltas.items():
            fp.write(str(county)+"|"+str(delta)+"\n")


    

