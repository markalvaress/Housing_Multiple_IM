import numpy as np
import scipy.signal

def calculate_num_neighbours(house_grid, r):
    """Assumes house_grid has -1s for non-houses. Uses that rather than 0 to allow for houses that actually have 0 value."""
    # split into 1 for has house there and 0 for doesn't
    house_grid_binary = np.copy(house_grid)
    house_grid_binary = np.where(house_grid_binary == -1, 0, 1)
    kernel = np.ones((2*r + 1, 2*r + 1))
    num_neighbours = scipy.signal.convolve2d(house_grid_binary, kernel, mode='same', boundary="symm")
    return num_neighbours

def calculate_new_house_values_conv(house_grid, affluence_grid, r, lambda_, calc_num_neighbours = False):
    """Calculates new house values using a convolution.

    Args:
        house_grid (np.ndarray): 
        affluence_grid (np.ndarray): 
        r (int): Neighbourhood radius
        lambda_ (float): Modeling parameter
        calc_num_neighbours (bool, optional): Whether to calculate number of neighbours or to just use kernel size. When the 
        grid is full (as in the toy model), we can set this to false as there are always the same number of neighbours. Defaults to False.

    Returns:
        np.ndarray: The new house values
    """
    house_grid_zeroed = np.copy(house_grid)
    house_grid_zeroed = np.where(house_grid_zeroed == -1, 0, house_grid_zeroed)

    # I think we include the house itself in the nbhd calculation?
    kernel = np.ones((2*r + 1, 2*r + 1))

    if calc_num_neighbours:
        num_neighbours = calculate_num_neighbours(house_grid, r)
    else:
        num_neighbours = kernel.size
    # idk if symmetric bdary conditions is the right thing to do
    nbhd_average = scipy.signal.convolve2d(house_grid_zeroed, kernel, mode='same', boundary="symm") / num_neighbours
    V_tplus1 = affluence_grid + lambda_*nbhd_average
    V_tplus1 = np.where(house_grid == -1, -1, V_tplus1) # make sure to keep gaps from before

    return V_tplus1

def initialise_affluence_and_house_grids(city_grid, affluence_levels, p):
    """
    Initialises affluence and house grids based on the generated city grid.
    Houses receive random affluence levels and value levels, while roads remain at -1.
    """
    m,n = city_grid.shape
    affluence_grid = -1*np.ones((m,n), dtype=float)
    house_grid = -1*np.ones((m,n), dtype=float)

    for i in range(m):
        for j in range(n):
            if city_grid[i, j] == 1:  # 1 is our value for houses
                affluence_grid[i, j] = np.random.choice(
                    [affluence_levels["rich"], affluence_levels["middle"], affluence_levels["poor"]],
                    p=p
                )
                house_grid[i, j] = np.random.uniform(0,1)  # Mark as a house

    return affluence_grid, house_grid