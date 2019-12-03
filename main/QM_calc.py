import numpy as np
import sys
import pandas as pd
import os

def QM_calc(mu, sigma, out_dir):
    """ Given mu and sigma, calculate SNR and CNR of all possible combinations

    SNR = mu_A / sigma_B
    CNR = (mu_A - mu_B) / sqrt(sigma_A**2 + sigma_B**2)

    Parameters
    ----------
    mu : numpy array
        Numpy 1-D array of means of fitted Gaussians as floats
    sigma : numpy array
        Numpy 1-D array of standard deviations of fitted Gaussians as floats
    out_dir : str
        Filepath to save results to
    
    Returns
    -------
    SNR_CNR_df : pandas DataFrame
        Pandas DataFame of Gaussian A, Gaussian B, SNR and CNR
    """

    SNR_all = [] # initialise lists to append to
    CNR_all = []
    gaussian_A = []
    gaussian_B = []

    # Calculate SNR and CNR ------------------------------------------------------------------------------------------------------------

    for i in range(len(mu)):
        for j in range(len(mu)):
            if(i != j):
                SNR = mu[i] / sigma[j] # calculate SNR
                CNR = np.abs(mu[i] - mu[j]) / np.sqrt(sigma[i]**2 + sigma[j]**2) # calculate CNR
                SNR_all.append(SNR)
                CNR_all.append(CNR)
                gaussian_A.append(i)
                gaussian_B.append(j)
                sys.stdout.write("SNR = {0:.2f} and CNR = {1:.2f} with Gaussian A = {2} and Gaussian B = {3} \n".format(SNR, CNR, i, j))

    # Output as pd df to send to .csv --------------------------------------------------------------------------------------------------

    columns = ["Gaussian_A", "Gaussian_B", "SNR", "CNR"]
    SNR_CNR_df = pd.DataFrame(list(zip(gaussian_A, gaussian_B, SNR_all, CNR_all)), columns = columns)
    SNR_CNR_df = SNR_CNR_df.set_index("Gaussian_A")
    SNR_CNR_df.to_csv(os.path.join(out_dir, "SNR_CNR_Results.csv"))

    return SNR_CNR_df