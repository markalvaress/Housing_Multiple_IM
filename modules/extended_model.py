import numpy as np
import random
import modules.aguilera_model as am

def initialise_house_and_demog_grids(city_grid, affluence_levels, p_affluence, p_ethnicity):
    """Initialises house price and demographics grids based on the city grid.

    Args:
        city_grid (np.ndarray): City grid, with 1s for houses and everything else is not a house
        affluence_levels (dict): A dictionary containing affluence levels for "rich", "middle", and "poor"
        p_affluence (list): A list or array of proportion of the population that is rich, middle, or poor respectively
        p_ethnicity (list): A list or array with the proportion of the population in different ethnic groups. The length of this list defines the number of ethnicities

    Returns:
        affluence_grid, house_grid, politics_grid, religion_grid, ethnicity_grid (np.ndarray): The relevant matrices.
    """
    rho = 0.3 # this should be an argument to the function
    n, m = city_grid.shape
    noise = np.random.rand(n, m)
    ethnicity_choices = np.arange(len(p_ethnicity)) + 1 # so if there are 6 ethnicities this will be 1,...,6

    affluence_grid = -1*np.ones((n, m), dtype=float)
    house_grid = -1*np.ones((n, m), dtype=float)
    politics_grid = -1*np.ones((n, m), dtype = float)
    continuous_political_grid = -1*np.ones((n, m), dtype = float)
    religion_grid = -1*np.ones((n, m), dtype = float)
    ethnicity_grid = -1*np.ones((n, m), dtype = float)
    for i in range(n):
        for j in range(m):
            if city_grid[i, j] == 1:  # 1 is our value for houses
                affluence_grid[i, j] = np.random.choice(
                    [affluence_levels["rich"], affluence_levels["middle"], affluence_levels["poor"]],
                    p = p_affluence
                )
                continuous_political_grid[i,j] = rho * affluence_grid[i,j] + (1- rho) * noise[i,j]
                if continuous_political_grid[i,j] < 0.33:
                    politics_grid[i,j] = 0
                elif 0.33 <= continuous_political_grid[i,j] < 0.66:
                    politics_grid[i,j] = 0.5
                else:
                    politics_grid[i,j] = 1
                religion_grid[i,j] = np.random.choice([1,0])
                ethnicity_grid[i, j] = np.random.choice(ethnicity_choices, p = p_ethnicity)
                house_grid[i, j] = np.random.uniform(0,1)  # Mark as a house

    return affluence_grid, house_grid, politics_grid, religion_grid, ethnicity_grid


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
                continue

            if ethnicity_grid[i,j] != -1:
                total += 1
                if ethnicity_grid[i,j] == target_ethnicity:
                    count += 1

    if total == 0:
        return 0
    else:
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

def calculate_neighborhood_average(grid, x, y, r):
    """
    Calculate the average value of the grid in the square neighborhood of radius r around (x, y).
    """
    n, m = grid.shape
    weighted_sum = 0
    total_weight = 0
    x_min, y_min = max(0,x-r), max(0,y-r)
    x_max, y_max = min(n,x+r), min(m,y+r)
    
    # Iterate over the neighborhood within the radius
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            if grid[x, y] == -1:
                break
            if grid[i, j] >= 0:
                # Calculate the distance from (x, y)
                dx, dy = x - i, y - j
                distance_squared = dx**2 + dy**2
                # Avoid division by zero by setting a minimum distance
                if distance_squared == 0:
                    weight = 0
                else:
                    weight = 1 / distance_squared
                weighted_sum += grid[i, j] * weight
                total_weight += weight

    # Check if total_weight is zero to avoid division by zero
    if total_weight == 0:
        return 0  # or return None, depending on your requirements
    # Calculate the weighted average of the neighborhood
    weighted_average = weighted_sum / total_weight
    return weighted_average

def calculate_delta_ordered(demographic_grid, x1, y1, x2, y2, r):
    P_x1, P_x2 = demographic_grid[x1, y1], demographic_grid[x2, y2]
    P_nbhd_x1, P_nbhd_x2 = calculate_neighborhood_average(demographic_grid, x1, y1, r), calculate_neighborhood_average(demographic_grid, x2, y2, r)
    delta = (P_x1 - P_nbhd_x1)**2 + (P_x2 - P_nbhd_x2)**2 - (P_x1 - P_nbhd_x2)**2 - (P_x2 - P_nbhd_x1)**2 
    return delta

def make_swap(affluence_grid, house_grid, politics_grid, religion_grid, ethnicity_grid, pol_weight, rel_weight, eth_weight, r):
    """
    Keep picking two agents until delta > 0, and then swap them.
    """
    delta = -1
    swap_attempt = 0
    n_tries = 1000 # to avoid an infinite loop

    # keep trying to swap until you actually get a delta > 0, or until you've tried n_tries times
    while delta <= 0 & swap_attempt < n_tries:
        swap_attempt += 1
        x1, y1, x2, y2 = am.choose_two_houses_rand(house_grid)        

        delta_econ = am.calculate_delta_econ(affluence_grid, house_grid, x1, y1, x2, y2)
        delta_pol = calculate_delta_ordered(politics_grid, x1, y1, x2, y2, r)
        delta_religion = calculate_delta_ordered(religion_grid, x1, y1, x2, y2, r)
        delta_eth = calculate_ethnic_delta(ethnicity_grid, x1, y1, x2, y2, r)

        delta = delta_econ + pol_weight*delta_pol + rel_weight*delta_religion + eth_weight*delta_eth     

        if delta > 0:
            # Swap the two agents
            affluence_grid[x1, y1], affluence_grid[x2, y2] = affluence_grid[x2, y2], affluence_grid[x1, y1]
            politics_grid[x1, y1], politics_grid[x2, y2] = politics_grid[x2, y2], politics_grid[x1, y1]
            religion_grid[x1, y1], religion_grid[x2, y2] = religion_grid[x2, y2], religion_grid[x1, y1]
            ethnicity_grid[x1, y1], ethnicity_grid[x2, y2] = ethnicity_grid[x2, y2], ethnicity_grid[x1, y1]

    return


   