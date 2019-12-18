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
