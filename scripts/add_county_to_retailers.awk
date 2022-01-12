# THE PURPOSE OF THIS SCRIPT IS TO MAP RETAILERS TO COUNTIES BASED ON ZIP CODES

BEGIN{
    path = "SNAP_DATA/"
    county = path "ZIP_COUNTY_092021.csv"
    retailers = path "HistoricalSNAPRetailerLocatorDataTab.tsv"

    # create array of congressional districts and zipcodes
    load_county_dict(county)

    # add column of congressional districts to retail data
    add_county(retailers, county_dict)

}

# create a dictionary where key=zipcode and data=congressional district
function load_county_dict(county){
    FS=","
    
    while ((getline <county)>0){
	county_dict[$1]=$2
    }
}

# add county to retailers file
function add_county(retailers, county){
    # want output file to be pipe delimited
    FS = "\t"
    OFS = "|"

    output_file = path "Historical_SNAP_Retailer_Locator_counties.csv"
    while ((getline <retailers)>0){

	# if there is county to map to, output it
	# don't just print $0 because want to change to pipe delimited file
	if ($9 in county_dict){
	    print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15, county_dict[$9] >output_file
	}

	# otherwise, note in output that zip did not have corresponding county
	else{
	    print $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15, "NO_COUNTY_DATA" >output_file
	}
    }
}
