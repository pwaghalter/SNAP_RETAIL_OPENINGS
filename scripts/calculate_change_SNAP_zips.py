# purpose of this file is for each county to write all start end dates of retailer accepting SNAP (will avg deltas of the dates)

from collections import defaultdict as dd
import csv
import sys

retailers = sys.argv[1]

def main():

    calculate_start_end(retailers)

def calculate_start_end(retailers):

    # initialize default dict to hold lists
    start_end = dd(list)

    # iterate through retailers marking congressional districts and their start and end dates
    with open(retailers) as file:
        f = file.readline()

        while f:
            fields = f.split("|")

            county = fields[17].strip()

            # find the start/end dates for analysis
            # looking at 2 year period after which store opened
            
            try:
                x = int(fields[13][6:])
                y = int(fields[13][6:])+2
            except:
                x = fields[13]
                y = fields[14]

            data = str(x)+","+str(y)+"|"

            # create dict with key=county, data=start,end dates
            start_end[county]+=[data]
            f = file.readline()

    # write county and dates to file
    for data in start_end:
            dates = ""
            for item in start_end[data]: dates+=item

            line =data+":"+ dates
            
            print(line+"$")


main()
