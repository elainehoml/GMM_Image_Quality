from skimage import io 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
sns.set()
plt.close('all')
import os

def replace_GV(mask_fname, mu_phantom, sigma_phantom):
    """ Replaces grey values in mask with random numbers from normal dist defined with mu_phantom and sigma_phantom
    Parameters
    ----------
    mask_fname : str
        Either "Air.tif", "Wax.tif" or "Tissue.tif"
    mu_phantom : float
        Random float for the mean of the normal distribution to be assigned
    sigma_phantom : float
        Random float for the standard deviation of the normal distribution to be assigned
    Returns
    -------
    I_phantom
        Phantom image of same dimension of original mask with grey values replaced
    """
    I = io.imread(os.path.join(os.getcwd(), "test", mask_fname))
    I_phantom = I.flatten() # take grey values of image as a 1D array
    I_idx = np.isnan(I_phantom) # de-select background
    random_dist = np.random.normal(mu_phantom, sigma_phantom, (I_idx == False).sum())
    # random_dist is an array of normally distributed random values with mu_phantom and sigma_phantom which is the same size
    # as number of pixels in the mask which are not background
    idx = np.where(I_idx.flatten() == False)
    I_phantom[idx] = random_dist # replace pixels within mask with random normal distribution
    I_phantom[np.isnan(I_phantom)] = 0 # replace pixels outside mask with 0
    I_phantom = I_phantom.reshape(I.shape) # reshape to original dimensions

    return I_phantom

def create_phantom(mu_phantom, sigma_phantom, img_dir):
    """ Creates phantom image with known grey value distributions generated randomly
    Takes the masks 'Air.tif', 'Wax.tif', 'Tissue.tif' segmented from a micro-CT 3D image dataset and assigns
    random values from normal distributions with mu_phantom and sigma_phantom to the grey values of each mask.
    The masks are then combined to create a phantom image which has a histogram made up of 3 peaks.
    Parameters
    ----------
    mu_phantom : list of float
        List of size 3 containing float values of means between 0-255 (8-bit)
    sigma_phantom : list of float
        List of size 3 containing float values of standard deviations ('sensible' values)
    img_dir : str
        Directory where test images are stored
    Returns
    -------
    I_phantom
        Combined masks with grey values replaced    
    """
    I_air = replace_GV(os.path.join(img_dir, "Air.tif"), mu_phantom[0], sigma_phantom[0])
    I_wax = replace_GV(os.path.join(img_dir, "Wax.tif"), mu_phantom[1], sigma_phantom[1])
    I_tissue = replace_GV(os.path.join(img_dir, "Tissue.tif"), mu_phantom[2], sigma_phantom[2])
    I_phantom = I_air + I_wax + I_tissue # Combine masks to get a full image
    I_phantom = I_phantom.reshape(I_air.shape) # Make sure to keep original dimensions

    print("Phantom means are {}".format(mu_phantom))
    print("Phantom standard deviations are {}".format(sigma_phantom))
    print("Phantom successfully created")

    return I_phantom

def show_phantom(I_phantom):
    """ Shows first slice of phantom image and histogram
    Parameters
    ----------
    I_phantom : np array
        Numpy array of phantom image created by create_phantom
    Returns
    -------
    None
    """
    plt.figure(figsize = [15.,5.])
    
    # Show image
    plt.subplot(1, 2, 1)
    plt.imshow(I_phantom[0], cmap = "gray") # first slice only
    plt.colorbar(label = "Grey Values")
    plt.axis("off")
    plt.title("Phantom Image")

    # Show histogram of grey values
    plt.subplot(1, 2, 2)
    I_phantom_histo = I_phantom[I_phantom != 0] # ignore pixels not in any mask
    plt.hist(I_phantom_histo.flatten(), bins = 256, density = True, linewidth = 0)
    plt.xlabel("Grey Values")
    plt.ylabel("Probability Density")
    plt.title("Phantom Grey Values")

    plt.tight_layout()
    plt.show()

def save_phantom(I_phantom, fname):
    """ Saves phantom image as tiff with given fname

    Parameters
    ----------
    I_phantom : np array
        Numpy array of phantom image created by create_phantom
    fname : str
        Filename to save I_phantom in, including file extension. .tiff recommended.
    
    Returns
    -------
    None
    """

    io.imsave(fname, I_phantom)
    