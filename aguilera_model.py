import numpy as np
from multiprocessing import Pool

def calculate_neighborhood_average(house_grid, x, y, r):
    """
    Calculate the average house value in the square neighborhood of radius r around (x, y).
    """
    n, m = house_grid.shape    
    neighborhood_sum = 0
    count = 0
    
    x_min, y_min = max(0,x-r), max(0,y-r)
    x_max, y_max = min(n,x+r), min(m,y+r)
    
    # Iterate over the neighborhood within the radius
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            # Add the neighbor's value to the sum
            neighborhood_sum += house_grid[i, j]
            count += 1

    # Calculate the average value of the neighborhood
    neighborhood_average = neighborhood_sum / count
    return neighborhood_average

def house_price_update_step(point, house_grid, affluence_grid, lambda_, r):
    x, y = point
    neighborhood_avg = calculate_neighborhood_average(house_grid, x, y, r)
    return affluence_grid[x,y] + lambda_ * neighborhood_avg

def update_values(affluence_grid, house_grid, lambda_, r):
    """
    Update house values based on the affluence and neighborhood average.
    """
    m, n = house_grid.shape
    grid_pts = [(x,y) for x in range(m) for y in range(n)]
    with Pool(8) as p:
        new_house_grid = p.map(lambda pt: house_price_update_step(pt, house_grid, affluence_grid, lambda_, r), grid_pts)

    new_house_grid = new_house_grid.reshape((m,n))

    return new_house_grid

