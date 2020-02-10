""" Create phantoms of known SNR and CNR, compare ground-truth with conventional and GMM SNR and CNR calculation """

# Import libraries
import os, sys
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set()

# Import functions
root_dir = os.path.split(os.path.abspath(os.path.dirname(sys.argv[0])))[0]
test_dir = os.path.join(root_dir, "test")

sys.path.append(os.path.join(root_dir, "main"))
import QM_load
import GMM_fit
import QM_calc

sys.path.append(test_dir)
import create_phantom

# create phantom directory
phantom_dir = "examples/benchmarking_phantoms"
if os.path.isdir(phantom_dir) == False:
    os.mkdir(phantom_dir)

# Create phantom images with known SNR and CNR
""" SNR and CNR are altered by scaling the sigma values for the phantom image, where original
mu and sigma values were derived from the original image before reassigning GV """

def generate_mu_sigma_values():
    """ Calculate mu and sigma for phantom images and corresponding SNR and CNR, save to csv

    Parameters
    ----------
    None

    Returns
    -------
    Pandas Dataframe
        Contains mu and sigma values assigned to each phantom, and phantom_name to identify phantoms
    """

    mu_original = np.array([8, 35, 82]) # air, wax and tissue
    sigma_original = np.array([7, 6, 16]) # air, wax and tissue
    sigma_scaling_factor = [0.1, 0.2, 0.5, 1.0, 2.0, 4.0]
    mu_phantom = np.zeros([6,3])
    sigma_phantom = np.zeros([6,3])
    for i in range(len(sigma_scaling_factor)):
        mu_phantom[i,:] = mu_original
        sigma_phantom[i,:] = sigma_original*sigma_scaling_factor[i]
    output = np.concatenate((mu_phantom, sigma_phantom), axis = 1) # join for output to csv
    phantom_name_df = pd.DataFrame({"phantom_name": ["P1", "P2", "P3", "P4", "P5", "P6"]})
    output_df = pd.DataFrame(output)
    output_df.columns = ["mu_air", "mu_wax", "mu_tissue", "sigma_air", "sigma_wax", "sigma_tissue"]
    output_df = phantom_name_df.join(output_df)
    output_df.to_csv("{}/mu_sigma_GT.csv".format(phantom_dir), index = None)

    return output_df

def create_phantoms_varied(GT):
    """ Creates phantoms with mu and sigma values from mu_sigma_GT, saves as .tif with phantom_name

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue.
    
    Returns
    -------
    list
        Contains filenames where phantoms are stored as .tifs
    """    
    # create and save phantoms
    for index, row in GT.iterrows():
        mu_phantom = [row["mu_air"], row["mu_wax"], row["mu_tissue"]]
        sigma_phantom = [row["sigma_air"], row["sigma_wax"], row["sigma_tissue"]]
        phantom_fname = "{}/{}.tif".format(phantom_dir, row["phantom_name"])
        I = create_phantom.create_phantom(mu_phantom, sigma_phantom, test_dir)
        create_phantom.save_phantom(I, phantom_fname)

# Calculate ground truth SNR and CNR

def GT_SNR_CNR(GT):
    """ Calculates ground truth SNR and CNR and saves as .csv

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue.

    Returns
    -------
    None
    """

    for index, row in GT.iterrows():
        mu = np.array([row["mu_air"], row["mu_wax"], row["mu_tissue"]])
        sigma = np.array([row["sigma_air"], row["sigma_wax"], row["sigma_tissue"]])
        output_fname = "{}/{}_GT.csv".format(phantom_dir, row["phantom_name"])
        output_df = QM_calc.QM_calc(mu, sigma, results_dir = "NA", save_results = False, verbose = False) # will save results manually
        output_df.to_csv(output_fname)

# Fit GMMs, calculate SNR and CNR

def GMM_SNR_CNR(GT):
    """ Fits GMMs and calculates SNR and CNR for phantoms, save SNR and CNR as csv

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue. Used only to get filenames for phantom images.
    
    Returns
    -------
    None
    """

    for index, row in GT.iterrows():
        phantom_fname = "{}/{}.tif".format(phantom_dir, row["phantom_name"])
        I = QM_load.QM_load(phantom_fname)
        GMM = GMM_fit.GMM_fit(I, 3)
        mu_fitted, sigma_fitted, weights_fitted = GMM_fit.extract_GMM_results(GMM)
        GMM_fit.save_GMM_results(phantom_fname, GMM)
        GMM_fit.plot_GMM_fit(I, GMM, phantom_fname)
        plt.close()
        output_fname = "{}/{}_fitted.csv".format(phantom_dir, row["phantom_name"])
        output_df = QM_calc.QM_calc(mu_fitted, sigma_fitted, results_dir = "NA", save_results = False, verbose = False)
        output_df.to_csv(output_fname)

mu_sigma_GT = generate_mu_sigma_values()
create_phantoms_varied(mu_sigma_GT)
GT_SNR_CNR(mu_sigma_GT)
GMM_SNR_CNR(mu_sigma_GT)
