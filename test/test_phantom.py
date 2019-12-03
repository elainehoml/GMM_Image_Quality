import os
import sys
sys.path.append(os.path.join(os.getcwd(), "main"))
import unittest
import QM_runner
import QM_load
import QM_fit
import QM_calc
import create_phantom

print("Tests to ensure fitted values are correct \n")

I_phantom, mu_phantom, sigma_phantom = create_phantom.create_phantom() # Create phantom to test with
mu_fitted, sigma_fitted = QM_fit.QM_fit(I_phantom, 3, img_fname = "NA", save_results = False)
SNR_CNR_df = QM_calc.QM_calc(mu_fitted, sigma_fitted, out_dir = "NA", save_results = False)

# class Phantom_Validation(unittest.TestCase):
    