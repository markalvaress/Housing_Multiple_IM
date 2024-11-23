import pandas as pd

# PROBLEM: ARE ALL OF THESE HOUSES COMPARABLE? e.g. is a 3 bed flat sold for 300k actually more expensive than a 2 bed sold for 200k??

# get clean postcodes and prices
ediProperties = pd.read_csv("ediPropertyVals.csv")
postcodes = ediProperties.Address.str.extract(r"(EH.*)")
postcodes_df = pd.DataFrame({'postcode': postcodes[0].to_list()}) # i have no idea how to use pandas
prices = ediProperties.Price.str.extract("(£[0-9]+,[0-9]+)").replace("[£,]", "", regex = True)
prices = pd.to_numeric(prices[0])

# convert postcode to lat and long
postcode_lookup = pd.read_csv("eh_pc_mapping.csv", header = None)
postcode_lookup.columns = postcode_lookup.columns.astype('str')
postcode_lookup.columns.values[0] = 'postcode'
postcode_lookup.columns.values[2] = 'easting'
postcode_lookup.columns.values[3] = 'northing'
postcode_lookup = postcode_lookup[['postcode', 'easting', 'northing']]

clean_house_data = postcodes_df.set_index('postcode').join(postcode_lookup.set_index('postcode')).reset_index()
clean_house_data['price'] = prices

# save output
clean_house_data.to_csv("clean_edi_house_data.csv", index = False)