import pandas as pd
import os


paid_price_mthly = pd.read_csv("pp-monthly-update-new-version.csv", header = None)

# get only houses in London purchased after 2021
paid_price_mthly.columns = paid_price_mthly.columns.astype(str)
paid_price_mthly.columns.values[1] = "price"
paid_price_mthly.columns.values[11] = "city"
paid_price_mthly.columns.values[13] = "region"
paid_price_mthly.columns.values[3] = "postcode"
paid_price_mthly_ldn = paid_price_mthly[paid_price_mthly.city == "LONDON"]
paid_price_mthly_ldn = paid_price_mthly_ldn[pd.to_datetime(paid_price_mthly_ldn['2']) > '2021-01-01']
paid_price_mthly_ldn = paid_price_mthly_ldn[["postcode", "price"]]

# get postcode lookup tables for london postcodes and combine
pcodes_e = pd.read_csv("postcode_lookups/e.csv", header = None)
pcodes_ec = pd.read_csv("postcode_lookups/ec.csv", header = None)
pcodes_n = pd.read_csv("postcode_lookups/n.csv", header = None)
pcodes_nw = pd.read_csv("postcode_lookups/nw.csv", header = None)
pcodes_se = pd.read_csv("postcode_lookups/se.csv", header = None)
pcodes_sw = pd.read_csv("postcode_lookups/sw.csv", header = None)
pcodes_w = pd.read_csv("postcode_lookups/w.csv", header = None)
pcodes_wc = pd.read_csv("postcode_lookups/wc.csv", header = None)

pcodes_lookup = pd.concat([pcodes_e, pcodes_ec, pcodes_n, pcodes_nw, pcodes_se, pcodes_sw, pcodes_w, pcodes_wc], axis = 0)
pcodes_lookup.columns = pcodes_lookup.columns.astype('str')
pcodes_lookup.columns.values[0] = 'postcode'
pcodes_lookup.columns.values[2] = 'easting'
pcodes_lookup.columns.values[3] = 'northing'
pcodes_lookup = pcodes_lookup[['postcode', 'easting', 'northing']]

# join postcode lookups to house price data
clean_house_data = paid_price_mthly_ldn.set_index('postcode').join(pcodes_lookup.set_index('postcode')).reset_index()
clean_house_data.to_csv("clean_ldn_house_data.csv", index = False)
