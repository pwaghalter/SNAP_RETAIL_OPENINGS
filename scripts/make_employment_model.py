# PURPOSE OF THIS SCRIPT IS TO GENERATE MODEL OF EXPECTED JOBS CREATED BY AN OPENING OF EACH STORE TYPE
# USED ONLINE SOURCES WHEN POSSIBLE, OTHERWISE EDCUATED GUESSES

import sys

store_type = sys.argv[1]

# Store Types with Data Online:
# https://www.ibisworld.com/industry-statistics/employment/convenience-stores-united-states/
#    convenience store: 3.4 employees

# https://www.ams.usda.gov/sites/default/files/media/FarmersMarketMangersSurvey.pdf
#    farmer's market: 32.25 (took average of the average number of employees by region)

# https://www.ibisworld.com/industry-statistics/employment/supermarkets-grocery-stores-united-states/#:~:text=How%20many%20people%20does%20the,the%20US%20has%2042.9%20employees.
#    large grocery store: 42.9 employees

# https://www.ibisworld.com/industry-statistics/employment/specialty-food-stores-united-states/
#    specialty food stores: 2.8 employees

#https://www.statista.com/statistics/240965/average-per-store-number-of-ftes-of-us-supermarkets/
#    supermarket: 68.7 employees (averaged average number of employees from 3 years with free data)

#https://www.ibisworld.com/industry-statistics/employment/wholesale-trade-united-states/#:~:text=The%20average%20Wholesale%20Trade%20business%20in%20the%20US%20has%208.0%20employees.
#    wholesaler: 8.0 employees

# rest are educated guesses

# create dictionary corresponding with employment model
# keys are store type, data is expected number of jobs created
model = {'Convenience Store': 3.4, 'Specialty': 2.8, 'Farmers\' Market': 32.25, 'Supermarket': 68.7, 'Wholesaler': 8.0, 'Large Grocery Store': 42.9, 'Medium Grocery Store': 25, 'Small Grocery Store': 10, 'Military Commissary': 5, 'Delivery Route': 8, 'Food Buying Co-op': 12, 'Super Store': 80, 'Wholesaler': 100, 'Combination Grocery/Other': 20}


# write model to stdout, categorizing each store type in store type data based off the model
with open(store_type, 'r') as s:
        
        for i, v in enumerate(s):
            v = v.strip()

            # lump all specialty stores together since have same expected employment
            if "Specialty" in v: v = "Specialty"

            # assign number of estimated jobs produced to each store type
            if v in model: v += "|"+str(model[v])

            # there are some lines in the file that are not actual store types
            else: v += "|NO MODEL"

            # write to stdout
            print(v)
