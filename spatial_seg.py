import numpy as np
import scipy as sp

def H_BO(U):
    m, n = U.shape
    assert m == n, "U (the matrix, not you) must be square" # We could maybe generalise to m != n? But then we'd have to compute our own expected_entropy.

    # Get eigenvals of covariance matrix and apply a normalisation
    Q = U.T @ U # we assume U is real so just use the regular transpose
    eigenvals, _ = np.linalg.eig(Q)
    # keep only real parts (evals should be real but sometimes np accidentally gives a tiny imaginary component).
    # sort eigenvals from largest abs value to smallest, then keep only those that are non zero
    eigenvals = np.array(sorted(np.real(eigenvals), key = abs, reverse = True))
    eigenvals = eigenvals[np.abs(eigenvals) > 1e-5] # get rid of eigenvalues that are basically 0
    p_i_denom = sum(np.abs(eigenvals[1:]))
    p = eigenvals / p_i_denom

    # Measure the entropy and subtract from the expected entropy to get the segregation measure
    entropy = -sum(p[1:] * np.log(p[1:]))
    return entropy

def spatial_segregation(U, expected_entropy = None):
    m, n = U.shape
    assert m == n, "U (the matrix, not you) must be square" # We could maybe generalise to m != n? But then we'd have to compute our own expected_entropy.

    # Measure the entropy and subtract from the expected entropy to get the segregation measure
    entropy = H_BO(U)
    if expected_entropy is None:
        expected_entropy = np.log(3/5 * n) # this is given in the text (for a full square grid up to n = 1000). Although they don't specify natural log, this is closest to actual results
    
    S_BO = expected_entropy - entropy

    return S_BO

def theil_index(props):
    """Get the theil index (a measure of inequality) of a vector of n proportions

    Args:
        props (np.ndarray): Proportions (must sum to around 1)

    Returns:
        float: Theil index of given distribution
    """
    assert all(props >= 0), "Proportions should all be non-negative"
    assert np.abs(np.sum(props) - 1) < 1e-5, "Proportions should sum to 1 (modulo some rounding errors)"
    return np.log(len(props)) + np.sum(props * np.log(props))

def generate_unequal_props(eta: float):
    """Generate a vector of 3 proportions using the 1 parameter family 5.1 from Aguilera et al 2007. You can
    then multiply these proportions by your total number of agents to get the desired number of agents in each group.

    Args:
        eta (float): A parameter between 0.5 and 1 (exclusive), used to generate the proportions. A higher eta corresponds to a higher Theil index.

    Returns:
        props: A 3d vector of proportions, proportion poor, middle, and rich (in that order).
        ti: The Theil index corresponding to the above vector
    """
    assert 0.5 < eta < 1, "Eta must be between 0.5 and 1 (exclusive)"

    a = 0.4 # this is the fixed value used throughout section 5 of Aguilera
    props = np.array([eta, (1-a)*(1-eta), a*(1-eta)])
    ti = theil_index(props)

    return props, ti
