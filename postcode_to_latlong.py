import pgeocode
import pandas as pd

# PROBLEM: ARE ALL OF THESE HOUSES COMPARABLE? e.g. is a 3 bed flat sold for 300k actually more expensive than a 2 bed sold for 200k??

# get clean postcodes and prices
ediProperties = pd.read_csv("ediPropertyVals.csv")
postcodes = ediProperties.Address.str.extract(r"(EH.*)")
postcodes = postcodes[0].to_list()
prices = ediProperties.Price.str.extract("(£[0-9]+,[0-9]+)").replace("[£,]", "", regex = True)
prices = pd.to_numeric(prices[0])

# convert postcode to lat and long
nomi = pgeocode.Nominatim('gb')
postcode_queryresults = [nomi.query_postal_code(pc) for pc in postcodes]
lats = [qr.latitude for qr in postcode_queryresults]
longs = [qr.longitude for qr in postcode_queryresults]

# save output
clean_house_data = pd.DataFrame({'latitude': lats, 'longitude': longs, 'price': prices})
clean_house_data.to_csv("clean_edi_house_data.csv")