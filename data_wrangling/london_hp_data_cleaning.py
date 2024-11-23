import pandas as pd
import os

# maybe multiply older prices by HPI?
paid_price_mthly = pd.read_csv("pp-monthly-update-new-version.csv", header = None)

paid_price_mthly.columns = paid_price_mthly.columns.astype(str)
paid_price_mthly.columns.values[1] = "price"
paid_price_mthly.columns.values[11] = "city"
paid_price_mthly.columns.values[13] = "region"
paid_price_mthly.columns.values[3] = "postcode"
paid_price_mthly_ldn = paid_price_mthly[paid_price_mthly.city == "LONDON"]

paid_price_mthly_ldn = paid_price_mthly_ldn[["postcode", "price"]]

pcodes_e = pd.read_csv("e.csv", header = None)
pcodes_ec = pd.read_csv("ec.csv", header = None)
pcodes_n = pd.read_csv("n.csv", header = None)
pcodes_nw = pd.read_csv("nw.csv", header = None)
pcodes_se = pd.read_csv("se.csv", header = None)
pcodes_sw = pd.read_csv("sw.csv", header = None)
pcodes_w = pd.read_csv("w.csv", header = None)
pcodes_wc = pd.read_csv("wc.csv", header = None)

pcodes_lookup = pd.concat([pcodes_e, pcodes_ec, pcodes_n, pcodes_nw, pcodes_se, pcodes_sw, pcodes_w, pcodes_wc], axis = 0)
pcodes_lookup.columns = pcodes_lookup.columns.astype('str')
pcodes_lookup.columns.values[0] = 'postcode'
pcodes_lookup.columns.values[2] = 'easting'
pcodes_lookup.columns.values[3] = 'northing'
pcodes_lookup = pcodes_lookup[['postcode', 'easting', 'northing']]

clean_house_data = paid_price_mthly_ldn.set_index('postcode').join(pcodes_lookup.set_index('postcode')).reset_index()
clean_house_data.to_csv("clean_ldn_house_data.csv", index = False)
