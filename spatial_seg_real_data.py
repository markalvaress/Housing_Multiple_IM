import pandas as pd
import spatial_seg as spseg
import numpy as np
import matplotlib.pyplot as plt
# import os

# os.chdir("Housing_Multiple_IM")

hp_data = pd.read_csv("clean_house_data/clean_ldn_house_data.csv", dtype = {'easting': 'float64','northing': 'float64','price': 'int64'})

# remove and then rescale values to between 1 and 100
hp_data = hp_data[(~hp_data.easting.isna()) & (~hp_data.northing.isna())]

# Use these values for edinburgh data
# rescaled_easting = (hp_data.easting.to_numpy() - 309120) / 247
# rescaled_northing = (hp_data.northing.to_numpy() - 663604) / 149
rescaled_easting = (hp_data.easting.to_numpy() - 515029) / 334
rescaled_northing = (hp_data.northing.to_numpy() - 167017) / 312

# fill in a matrix by taking the average of house prices within that region. We initialise an empty matrix (price -1)
m, n = 101, 101

hp_matrix = -1 * np.ones((m, n))
num_houses_there = np.zeros((m, n))

# stick the sum of house prices into the relevant slots in the matrix
for i, price in enumerate(hp_data['price'].to_list()):
    price=np.log(price) # to make for a better graph, we won't necessarily do this in the end
    north = int(rescaled_northing[i])
    east = int(rescaled_easting[i])

    if hp_matrix[north, east] == -1:
        hp_matrix[north, east] = price
        num_houses_there[north, east] = 1
    else:
        hp_matrix[north, east] += price
        num_houses_there[north, east] += 1

# make the house prices the average in that region
for i in range(m):
    for j in range(n):
        if num_houses_there[i, j] != 0:
            hp_matrix[i,j] = hp_matrix[i,j] / num_houses_there[i,j]

plt.imshow(hp_matrix)
plt.colorbar()
plt.show()

# save an array of just the locations where there are houses in our london dataset. Matches Nathan's city generator.
london_map = np.where(hp_matrix == -1, 0, 1)
np.savetxt("london_map_array.txt", london_map)

# this poops the bed because non-house values are set to -1
#spseg.spatial_segregation(hp_matrix)