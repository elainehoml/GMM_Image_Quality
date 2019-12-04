import os
import sys
import numpy as np
import random
sys.path.append(os.path.join(os.getcwd(), "main"))
import unittest
import QM_runner
import QM_load
import QM_fit
import QM_calc
import create_phantom

print("Tests to ensure fitted values are correct \n")

mu_phantom = [40, 100, 160] # 3 example means in 8-bit range
sigma_phantom = [5, 15, 20] # 3 example standard deviations
I_phantom = create_phantom.create_phantom(mu_phantom, sigma_phantom) # Create phantom to test with
mu_fitted, sigma_fitted = QM_fit.QM_fit(I_phantom, 3, img_fname = "NA", save_results = False)
SNR_CNR_df = QM_calc.QM_calc(mu_fitted, sigma_fitted, out_dir = "NA", save_results = False)

def calc_difference(a, b):
    """ Calculate the pct difference between floats a and b
    Parameters
    ----------
    a : float
        First value to compare
    b : float
        Value to compare a against
    Returns
    -------
    bool
        Returns True if int(percentage difference) between a and b > 5%
    """
    pct_diff = 100. * (np.abs(a - b) / a)
    if int(pct_diff) > 5:
        return True 
    else:
        return False

def phantom_SNR(i, j):
    """ Calculates difference between SNR of Gaussians A and B for fitted and phantom
    Parameters
    ----------
    i : int
        Gaussian A, i != j
    j : int 
        Gaussian B, i != j
    Returns
    -------
    bool
        Returns true if pct difference in SNR is > 5%
    """
    SNR_phantom = mu_phantom[i] / sigma_phantom[j]
    SNR_fitted = mu_fitted[i] / sigma_fitted[j]

    SNR_diff = 100 * (np.abs(SNR_phantom - SNR_fitted)/SNR_phantom)
    if int(SNR_diff) > 5:
        return True
    else:
        return False

def phantom_CNR(i, j):
    """ Calculates difference between CNR of Gaussians A and B for fitted and phantom
    Parameters
    ----------
    i : int
        Gaussian A, i != j
    j : int 
        Gaussian B, i != j
    Returns
    -------
    bool
        Returns true if pct difference in CNR is > 5%
    """
    CNR_phantom = np.abs(mu_phantom[i] - mu_phantom[j]) / np.sqrt(sigma_phantom[i]**2 + sigma_phantom[j]**2)
    CNR_fitted = np.abs(mu_fitted[i] - mu_fitted[j]) / np.sqrt(sigma_fitted[i]**2 + sigma_fitted[j]**2)

    CNR_diff = 100 * (np.abs(CNR_phantom - CNR_fitted)/CNR_phantom)
    if int(CNR_diff) > 5:
        return True
    else:
        return False

class Phantom_Validation(unittest.TestCase):
    def test_mu(self):
        """ Compare mu_fitted with mu_phantom to see if they are close to each other
        Raises
        ------
        AssertionError
            If difference between mu_fitted and mu_phantom > 5%
        """
        mu_difference = list(map(calc_difference, mu_fitted, mu_phantom))
        for i in range(len(mu_difference)):
            self.assertFalse(mu_difference[i], "Percentage difference between mu_fitted and mu_phantom > 5%")

    def test_sigma(self):
        """ Compare sigma_fitted with sigma_phantom to see if they are close to each other
        Raises
        ------
        AssertionError
            If difference between sigma_fitted and sigma_phantom > 5%
        """
        sigma_difference = list(map(calc_difference, sigma_fitted, sigma_phantom))
        for i in range(len(sigma_difference)):
            self.assertFalse(sigma_difference[i], "Percentage difference between sigma_fitted and sigma_phantom > 5%")

    def test_SNR_CNR(self):
        """ Compare SNR and CNR from phantom and fitted between randomly chosen Gaussians to see if they are close to each other
        Raises
        ------
        AssertionError
            If difference between SNR phantom and fitted > 2%
        """
        (i, j) = random.sample(range(len(mu_fitted)), 2) # choose two random numbers to compare
        self.assertFalse(phantom_SNR(i, j), "Percentage difference in SNR between fitted and phantom > 5%")
        self.assertFalse(phantom_CNR(i, j), "Percentage difference in CNR between fitted and phantom > 5%")       


suite = unittest.TestLoader().loadTestsFromTestCase(Phantom_Validation)
unittest.TextTestRunner(verbosity = 2).run(suite)