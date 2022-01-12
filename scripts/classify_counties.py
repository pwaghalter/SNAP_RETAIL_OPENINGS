# PURPOSE OF THIS SCRIPT IS TO CLASSIFY COUNTIES AS LOW, MIDDLE, OR HIGH INCOME
import sys, gzip
from collections import defaultdict as dd

# argv[1] = SNAP_DATA/ZIP_COUNTY_092021.csv
# argv[2] = IncomePop.gz
# argv[3] = SNAP_DATA/county_pop

# need to go through each zip in argv[1] and find out what proportion of the total pop of that county is in that zip, using argv[3]
# then need to multiply median income (in argv[2]) of that zip by the proportion of the pop in that zip and add it to the income of that county

# load the counties and total populations into dictionary for O(1) access
county_pop_file = open(sys.argv[3])
county_pop_dict = dict(line.strip().split("|") for line in county_pop_file)
county_pop_file.close()

# load median incomes of county into dictionary for O(1) access
zip_income_file = gzip.open(sys.argv[2], "rt")
zip_income_dict = dict(line.strip().split("|")[0:2] for line in zip_income_file)
zip_income_file.close()

# load population of each zip into dictionary for O(1) access
zip_income_file = gzip.open(sys.argv[2], "rt") 
zip_pop_dict = dict(line.strip().split("|")[0:4:3] for line in zip_income_file)
zip_income_file.close()  

# keep track of all the partial weighted incomes for each county, then sum them to get total income
county_incomes_to_sum=dd(lambda: [])

with open(sys.argv[1]) as zip_county_file:

    for line in zip_county_file:

        # get zip, county
        line = line.split(",")[0:2]

        # check that we have data on the zip
        if line[0] in zip_income_dict:

            zip_income = zip_income_dict[line[0]]

            zip_pop = zip_pop_dict[line[0]]

            # check that we have data on the county
            if line[1] in county_pop_dict:
                county_total_pop = county_pop_dict[line[1]]

                # calculate proportion of county's population is in that zip, using total population calculated in last script
                pop_propotion = float(zip_pop)/float(county_total_pop)

                # calculate weighted income
                weighted_income = float(zip_income)*pop_propotion

                # keep track of weighted incomes for each zip in each county
                county_incomes_to_sum[line[1]] += [weighted_income]

# sum the weighted incomes for each county to get total income for county
for key in county_incomes_to_sum:

    county_income = sum(county_incomes_to_sum[key])

    # classify the income class using: https://www.investopedia.com/financial-edge/0912/which-income-class-are-you.aspx
    if county_income<42000:
        class_ = "LOW"
    elif county_income<126000:
        class_ = "MID"
    else:
        class_ = "HIGH"

    # write data to stdout
    print(key, county_income, class_, sep = "|")


    

    
