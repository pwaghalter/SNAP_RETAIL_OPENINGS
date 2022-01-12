# PURPOSE OF THIS SCRIPT IS ORGANIZING THE DATA TO PLOT: COUNTY|EXPECTED|ACTUAL for the year in that county with greatest expected change
import sys

# data of expected num jobs per county
expected = sys.argv[1]

# data of actual change in people on SNAP per county
yearly_deltas = sys.argv[2]

file = open(expected)
lines = file.readlines()[2:]

# for each county, identify the actual change for the year expected to have the most change
for line in lines:
        fields = line.split("|")
        county, year, e_delta = fields[0], fields[1], fields[2]
        
        try:
                # access the file of actual change corresponding to that year
                actual_delta_file = yearly_deltas+str(year)+"_"+str(int(year)+2)
                with open(actual_delta_file) as a:
                        for temp in a:
                                t = temp.split("|")

                                # locate county and find the actual change in num ppl on SNAP
                                if t[0]==county:

                                        # write to stdout
                                        print(county+"|"+e_delta.strip()+"|"+t[1].strip())
                                        
        except: pass
file.close()

