import numpy as np

def calculate_ethnicity_average(ethnicity_grid, x, y, target_ethnicity, r):
    """Calculate the proportion of agents around the point x,y (square radius r) that have the target ethnicity.

    Args:
        ethnicity_grid (np.ndarray): 
        x (int): x-coordinate of house I may move to
        y (int): y-coordinate of house I may move to
        target_ethnicity (int): The ethnicity I'm trying to calculate a proportion for
        r (int): Neighbourhood radius

    Returns:
        float: Proportion with target ethnicity
    """
    # instantly jump out if I've been fed an empty space (road)
    if ethnicity_grid[x, y] == -1:
        return 0

    n, m = ethnicity_grid.shape
    x_min, y_min = max(0,x-r), max(0,y-r)
    x_max, y_max = min(n,x+r), min(m,y+r)
    count = 0
    total = 0

    # Go through neighbourhood and count number of occupied houses and how many are of the target ethnicity
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            # don't include the house itself in the proportion, because we're either living there (so we don't include ourselves)
            # or we want to move there, in which case we'd be swapping with (x,y) so it shouldn't be included in the count
            if i == x and j == y:
                break

            if ethnicity_grid[i,j] != -1:
                total += 1
                if ethnicity_grid[i,j] == target_ethnicity:
                    count += 1

    return count / total

def calculate_ethnic_delta(ethnicity_grid: np.ndarray, x1: int, y1: int, x2: int, y2: int, r) -> float:
    """Calculate ethnicity delta of the two points (x1,y1), (x2,y2).

    Args:
        ethnicity_grid (np.ndarray): 
        x1 (int): 
        y1 (int): 
        x2 (int): 
        y2 (int): 

    Returns:
        float: The ethnicity delta
    """
    # proportions matching ethnicity in current locations
    p1_current_eth_prop = calculate_ethnicity_average(ethnicity_grid, x1, y1, ethnicity_grid[x1,y1], r)
    p2_current_eth_prop = calculate_ethnicity_average(ethnicity_grid, x2, y2, ethnicity_grid[x2,y2], r)

    # proportions matching ethnicity if they were to swap
    p1_swapped_eth_prop = calculate_ethnicity_average(ethnicity_grid, x2, y2, ethnicity_grid[x1,y1], r)
    p2_swapped_eth_prop = calculate_ethnicity_average(ethnicity_grid, x1, y1, ethnicity_grid[x2,y2], r)

    # this will be positive if swapping would increase the matching ethnic proportion for both agents
    # (or e.g. increases lots for one agent decreases a bit for the other)
    delta_eth = (p1_swapped_eth_prop - p1_current_eth_prop) + (p2_swapped_eth_prop - p2_current_eth_prop)

    return delta_eth

# Testing -------------------
# You can use the code below to see ethnicities cluster together

# def make_swap(eth_grid, r):
#     m, n = eth_grid.shape
#     swapped = False

#     while not swapped:
#         x1, x2 = np.random.choice(m, 2)
#         y1, y2 = np.random.choice(n, 2)
#         delta_eth = calculate_ethnic_delta(ethnicity_grid, x1, y1, x2, y2, r)
#         if delta_eth > 0:
#             eth_grid[x1, y1], eth_grid[x2, y2] = eth_grid[x2, y2], eth_grid[x1, y1]
#             swapped = True

#     return

# import matplotlib.pyplot as plt

# ethnicity_grid = np.random.choice(6, (100,100))
# plt.imshow(ethnicity_grid)

# for i in range(20000):
#     make_swap(ethnicity_grid, 2)

# plt.imshow(ethnicity_grid)


   