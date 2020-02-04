import time
from PIL import Image
import numpy as np
import sys

import matplotlib.pyplot as plt

def QM_load(img_fname, min_GV = 0, max_GV = 255, specify_gv = False, pct_stack_import = 10.):
    """Loads n slices of a 3D image stack specified by % of stack to import, limits to min and max GV if specify_gv == True

    Parameters
    ----------
    img_fname : str
        Filepath of image to be loaded
    min_GV : float
        Minimum grey value to consider, ignored if specify_gv == False
    max_GV : float
        Maximum grey value to consider, ignored if specify_gv == False
    specify_gv : bool
        If True, discard grey values outside [min_GV, max_GV]
    pct_stack_import : float, default 10.
        Percentage of stack to import. Used to calculate number of slices to import, evenly spaced throughout stack
    
    Returns
    -------
    img
        Flattened 1D numpy array with only n slices imported based on pct_stack_import
    """
    start = time.time()

    I = Image.open(img_fname)
    n_slices = int(I.n_frames * (pct_stack_import/100)) # calculate number of slices to import
    img_list = []
    for i in np.arange(0, n_slices):
        I.seek(int((i+1)*(I.n_frames/(n_slices + 1)))) # evenly spaced slices through stack
        img = np.array(I)
        img_list.append(img)
        img_nparray = np.asarray(img_list)
    
    if specify_gv == True:
        img_flatten = img_nparray.flatten()
        img_thresholded = img_flatten[(img_flatten > min_GV) & (img_flatten < max_GV)]
        img_to_return = img_thresholded
    
    elif specify_gv == False:
        img_to_return = img_nparray.flatten()
    
    end = time.time()
    
    print("Image imported, time elapsed = {0:.2f} s".format((end-start)))
    
    return img_to_return
