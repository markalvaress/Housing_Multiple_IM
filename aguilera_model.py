import numpy as np
import scipy.signal

def calculate_new_house_values_conv(house_grid, affluence_grid, r, lambda_):
    '''
    Uses a convolution to calculate new house values.
    '''
    house_grid_zeroed = np.copy(house_grid)
    house_grid_zeroed = np.where(house_grid_zeroed == -1, 0, house_grid_zeroed)

    # I think we include the house itself in the nbhd calculation?
    kernel = np.ones((2*r + 1, 2*r + 1))

    # idk if symmetric bdary conditions is the right thing to do
    nbhd_average = scipy.signal.convolve2d(house_grid_zeroed, kernel, mode='same', boundary="symm") / kernel.size
    V_tplus1 = affluence_grid + lambda_*nbhd_average

    return V_tplus1

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

# def update_values(affluence_grid, house_grid, lambda_, r):
#     """
#     Update house values based on the affluence and neighborhood average.
#     """
#     m, n = house_grid.shape
#     grid_pts = [(x,y) for x in range(m) for y in range(n)]
#     with Pool(8) as p:
#         new_house_grid = p.map(lambda pt: house_price_update_step(pt, house_grid, affluence_grid, lambda_, r), grid_pts)

#     new_house_grid = new_house_grid.reshape((m,n))

#     return new_house_grid

