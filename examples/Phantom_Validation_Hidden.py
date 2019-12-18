""" Script to import functions and libraries for phantom validation tests of GMM image quality measure """

# Import libraries
import os
import sys
from IPython.display import display, display_html
import ipywidgets as widgets
import matplotlib.pyplot as plt
import seaborn as sns
from skimage import io
import numpy as np
import pandas as pd
sns.set()

# Import functions
root_dir = os.path.split(os.getcwd())[0]
test_dir = os.path.join(root_dir, "test")

sys.path.append(os.path.join(root_dir, "main"))
import QM_fit
import QM_calc

sys.path.append(test_dir)
import create_phantom

# Function to calculate percentage differences
def calc_pct_diff(value_1, value_2):
    """ Calculates percentage difference between value_1 and value_2

    % diff = 100 * (value_1 - value_2)/ value_1

    Parameters
    ----------
    value_1 : float
        First value against which percentage difference is normalised (denominator)
    value_2 : float
        Second value to calculate percentage difference
    
    Returns
    -------
    float
        Percentage difference between value_1 and value_2
    """
    pct_diff = 100 * (float(value_1) - float(value_2)) / float(value_1)
    return pct_diff

def plot_pct_diff(xseries, pct_diff, title, xlabel, legend = True):
    """ Plots percentage difference series against xseries

    Parameters
    ----------
    xseries : list or np array
        X-data to be plotted
    pct_diff : list or np array
        Y-data to be plotted (will be converted to np array)
    title : str
        title of plot
    xlabel : str
        x-axis label
    legend : bool
        if True, plot legend
    
    Returns
    -------
    matplotlib object
    """

    # Convert pct_diff to np array
    pct_diff = np.array(pct_diff)
    
    # Plots
    plt.plot(xseries, pct_diff[:,0], label = "Air")
    plt.plot(xseries, pct_diff[:,1], label = "Wax")
    plt.plot(xseries, pct_diff[:,2], label = "Tissue")
    if legend == True:
        plt.legend(fontsize=14)
    plt.xlabel(xlabel, fontsize = 16)
    #plt.ylabel(title, fontsize = 16)
    plt.title(title, fontsize = 15)

def summary_plot(xseries, xlabel, pct_diff_mu_results, pct_diff_sigma_results, CNR):
    """ Wrapper function to plot % diff and CNR against contrast between tissue and wax

    Parameters
    ----------
    xseries : list or array
        Data to plot on x-axis
    xlabel : str
        X-axis label
    pct_diff_mu_results : list or array
        % difference in mu
    pct_diff_sigma_results : list or array
        % difference in sigma
    CNR : list or array
        contrast-to-noise ratio between tissue and wax
    """
    
    plt.figure(figsize = (15,5))
    sns.set_style('white')
    plt.subplot(1,3,1)
    plot_pct_diff(xseries, pct_diff_mu_results, "(a) % Difference in Fitted and Assigned $\mu$", xlabel)
    plt.subplot(1,3,2)
    plot_pct_diff(xseries, pct_diff_sigma_results, "(b) % Difference in Fitted and Assigned $\sigma$", xlabel)
    plt.subplot(1,3,3)
    plt.plot(xseries, CNR)
    plt.title("(c) CNR between wax and tissue", fontsize = 16)
    plt.xlabel(xlabel, fontsize = 16)
    plt.show()
