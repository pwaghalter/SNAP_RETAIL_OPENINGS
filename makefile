all: plot.pdf

# STEP 1: CLASSIFY COUNTIES BY INCOME CLASS
# calculate the total population for each county, to be used later in weighted average of zip incomes
SNAP_DATA/county_pop: SNAP_DATA/ZIP_COUNTY_092021.csv IncomePop.gz
	python3 scripts/get_total_county_pop.py SNAP_DATA/ZIP_COUNTY_092021.csv IncomePop.gz  >SNAP_DATA/county_pop

# classify each county as low, mid, or high income using weighted averages of zip median incomes
SNAP_DATA/counties_incomes_classified: SNAP_DATA/ZIP_COUNTY_092021.csv IncomePop.gz SNAP_DATA/county_pop
	python3 scripts/classify_counties.py SNAP_DATA/ZIP_COUNTY_092021.csv IncomePop.gz SNAP_DATA/county_pop >SNAP_DATA/counties_incomes_classified

# STEP 2: CALCULATE ACTUAL CHANGE IN NUMBER OF PEOPLE ON SNAP PER COUNTY PER 2 YEAR PERIOD
# map each retailer to its corresponding county
SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv: SNAP_DATA/HistoricalSNAPRetailerLocatorDataTab.tsv SNAP_DATA/ZIP_COUNTY_092021.csv
	gawk -f scripts/add_county_to_retailers.awk

# calculate the actual change in number of people on SNAP for each two year period
SNAP_DATA/DELTAS/*: SNAP_DATA/SNAP-FNS388a-10/JAN_*
	python3 scripts/calculate_delta_by_years.py SNAP_DATA/SNAP-FNS388a-10/JAN_ SNAP_DATA/DELTAS/

# STEP 3: CALCULATE EXPECTED NUMBER OF JOBS CREATED PER COUNTY PER YEAR BASED ON RETAIL STORE OPENINGS
# generate file of store types found in retailers data
SNAP_DATA/store_type: SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv
	cat SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv | cut -d "|" -f 3 | sort | uniq >SNAP_DATA/store_type

# create employment model to estimate number of jobs created by each store type
SNAP_DATA/employment_model: SNAP_DATA/store_type
	python3 scripts/make_employment_model.py SNAP_DATA/store_type >SNAP_DATA/employment_model

# find out how many jobs are expected to be created each year based on how many stores of which type opened
SNAP_DATA/county_store_count: SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv 
	python3 scripts/count_store_types.py SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv >SNAP_DATA/county_store_count

# calculate the single year with the greatest expected job openings, and therefore expected decrease in ppl on SNAP for each county
SNAP_DATA/greatest_expected_delta_year_by_county: SNAP_DATA/county_store_count SNAP_DATA/employment_model
	python3 scripts/greatest_expected_delta_year_by_county.py SNAP_DATA/county_store_count SNAP_DATA/employment_model >SNAP_DATA/greatest_expected_delta_year_by_county

# STEP 4: PLOT DATA
# generate file with county, expected number of jobs created, and actual change in people on SNAP
SNAP_DATA/county_expected_actual: SNAP_DATA/greatest_expected_delta_year_by_county SNAP_DATA/DELTAS/*
	python3 scripts/actual_delta_greatest_expected_year.py SNAP_DATA/greatest_expected_delta_year_by_county SNAP_DATA/DELTAS/ >SNAP_DATA/county_expected_actual

# tag each county in the data that will be graphed with an income classification using classifications generated earlier
SNAP_DATA/final_data: SNAP_DATA/county_expected_actual SNAP_DATA/counties_incomes_classified
	python3 scripts/classify_retail_incomes.py SNAP_DATA/county_expected_actual SNAP_DATA/counties_incomes_classified >SNAP_DATA/final_data

# generate pdf of plot of the data
plot.pdf: SNAP_DATA/final_data
	python3 scripts/plot_data.py SNAP_DATA/final_data

# remove all intermediate files
clean:
	rm SNAP_DATA/county_pop SNAP_DATA/counties_incomes_classified SNAP_DATA/Historical_SNAP_Retailer_Locator_counties.csv SNAP_DATA/DELTAS/* SNAP_DATA/store_type SNAP_DATA/employment_model SNAP_DATA/county_store_count SNAP_DATA/greatest_expected_delta_year_by_county SNAP_DATA/county_expected_actual SNAP_DATA/final_data plot.pdf
