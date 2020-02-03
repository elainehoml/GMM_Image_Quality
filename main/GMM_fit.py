import os
import csv
import time
import numpy as np
import sklearn.mixture
import sys
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.close('all')
from scipy.stats import norm

import QM_load

def GMM_fit(img, n_gaussians):
    """
    Fits Gaussian mixture model to grey value histogram of img

    Parameters
    ----------
    img : numpy array
        3D numpy array of image, output from QM_load.py
    n_gaussians : int
        Number of Gaussian components to fit to histogram, usually equals number of material components in specimen
    
    Returns
    -------
    GMM
        instance of GaussianMixture class
    """

    start = time.time()

    img_1d = img.flatten() # flatten 3D img array

    GMM = sklearn.mixture.GaussianMixture(n_components = n_gaussians, random_state = 3) # fix random state for predictability
    GMMfit = GMM.fit(img_1d.reshape(-1,1))

    end = time.time()
    print("GMM fit complete, time elapsed = {0:.2f} s\n".format((end-start)))

    return GMM

def extract_GMM_results(GMM):
    """
    Extracts means, standard deviations and weights from fitted GMM

    Parameters
    ----------
    GMM : instance of GaussianMixture class
        Output from GaussianMixture from which results are extracted
    
    Returns
    -------
    mu
        Numpy 1-D array of size = n_gaussians with the mean(s) of fitted Gaussian component(s) as floats.
    sigma
        Numpy 1-D array of size = n_gaussians with the standard deviation(s) of fitted Gaussian component(s) as floats.
    weights
        Numpy 1-D array of size = n_gaussians with the weight(s) of fitted Gaussian component(s) as floats.
    """

    mu_fitted = GMM.means_.reshape([len(GMM.means_)])
    sigma_fitted = np.sqrt(GMM.covariances_).reshape([len(GMM.means_)])
    weights_fitted = GMM.weights_.reshape([len(GMM.means_)])

    sort_ind = np.argsort(mu_fitted) # list of indices sorted in ascending order of means
    mu_fitted = mu_fitted[sort_ind]
    sigma_fitted = sigma_fitted[sort_ind]
    weights_fitted = weights_fitted[sort_ind]
    
    return mu_fitted, sigma_fitted, weights_fitted

def save_GMM_results(img_fname, GMM):
    """
    Saves mu, sigma and weights to .csv in created results directory
    
    Parameters
    ----------
    img_fname : str
        Filepath to image name, used to create results directory
    GMM : instance of GaussianMixture class
        Output from GaussianMixture from which results are extracted
    
    Returns
    -------
    fitted_results.csv : csv file
        Saved in results directory
    """
    # Create results directory
    results_dir = "{}_results".format(os.path.splitext(img_fname)[0])
    if os.path.isdir(results_dir) == False:
        os.mkdir(results_dir)
    
    # save to csv
    mu, sigma, weights = extract_GMM_results(GMM)
    with open(os.path.join(results_dir, "fitted_results.csv"), "w", newline = "") as csv_file:
        w = csv.writer(csv_file, delimiter = ",")
        csv_file.write("# Image filename = {} \n".format(img_fname))
        csv_file.write("# Fitted Gaussians \n")
        csv_file.write("# Mean, Standard Deviation, Weight \n")
        for i in range(len(mu)):
            to_write = [mu[i], sigma[i], weights[i]]
            w.writerow(to_write) # writes mu, sigma and weight of each fitted Gaussian as a new row
    print("Results saved to {} \n".format(results_dir))

def plot_GMM_fit(img, GMM, img_fname):
    """
    Plots fitted Gaussian components over grey value histogram from img, saves as png

    Parameters
    ----------
    img : numpy array
        3D numpy array of image, output from QM_load.py
    GMM : instance of GaussianMixture class
        Output from GaussianMixture from which results are extracted
    img_fname : str
        Filepath to image name, used to create results directory
    """
    # Create results directory
    results_dir = "{}_results".format(os.path.splitext(img_fname)[0])
    if os.path.isdir(results_dir) == False:
        os.mkdir(results_dir)

    # Plot grey value histogram
    img_1d = img.flatten()
    fig  = plt.figure()
    ax = plt.subplot(111)
    bins = int(0.25 * np.sqrt(len(img_1d)))
    histo = plt.hist(img_1d, bins = bins, density = True, linewidth = 0)

    # Plot fitted Gaussians
    mu, sigma, weights = extract_GMM_results(GMM)
    norm_mat = np.zeros([len(histo[1]), len(mu)]) # store y-coordinates of normal distribution to be plotted
    for i in range(0, len(mu)):
        y = norm.pdf(histo[1], mu[i], sigma[i]) # generate normal distribution
        norm_mat[:,i] = y * weights[i] # scale by weight, write y-coordinates to norm_mat
        gauss = plt.plot(histo[1], y, label = "Gaussian {0}, $\mu$ = {1:.2f}, $\sigma$ = {2:.2f}, weight = {3:.2f}".format(i, mu[i], sigma[i], weights[i]))
        x_mu = np.full([2,], mu[i]) # x-coord of vertical line marking mean of Gaussian
        y_mu = [0., np.max(y)] # y-coords of vertical line marking mean of Gaussian
        plt.plot(x_mu, y_mu, color = gauss[0]._color)
        plt.text(mu[i], y_mu[1], "{}".format(i), horizontalalignment = "center")
    plt.plot(histo[1], np.sum(norm_mat, axis = 1), "k--", label = "Sum of fitted Gaussians") # Plot sum of fitted Gaussians
    plt.xlabel("Grey Values")
    plt.ylabel("Probability Density")
    ax.legend(bbox_to_anchor = (0.8, -0.2))
    plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, "histo.png"))
    print("Histogram plotted and saved to {} \n".format(results_dir))
    plt.show()

# img_fname = os.path.join(os.getcwd(), "test", "test.tif")
# img = QM_load.QM_load(img_fname)
# GMM = GMM_fit(img, 3)
# mu, sigma, weights = extract_GMM_results(GMM)
# save_GMM_results(img_fname, GMM)
# plot_GMM_fit(img, GMM, img_fname)