# Import Libraries

from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn.mixture
from scipy.stats import norm
import time
import os
import sys
import pandas as pd
sns.set()
plt.close('all')

# Import QM functions

import QM_load
import QM_fit
import QM_calc

# Main

img_fname = os.path.join(os.getcwd(), "test", "test.tif")
img = QM_load(img_fname, 10)

out_dir = os.path.join(os.getcwd(), "test", "results") # create out_dir
if os.path.isdir(out_dir) == False:
    os.mkdir(out_dir)
mu, sigma = QM_fit(img, 3, out_dir)