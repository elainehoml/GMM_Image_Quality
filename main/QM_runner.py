# Import libraries
import os

# Import QM functions

from QM_load import QM_load
from QM_calc import QM_calc
import GMM_fit

def QM_runner(img_fname, n_gaussians, min_GV = 0, max_GV = 255, specify_gv = False, pct_stack_import = 10.):
    """ Basic workflow returning SNR and CNR
    Parameters
    ----------
    img_fname : str
        Filepath of image to load
    n_gaussians : int
        Number of Gaussians to fit
    min_GV : float
        Minimum grey value to consider, ignored if specify_gv == False
    max_GV : float
        Maximum grey value to consider, ignored if specify_gv == False
    specify_gv : bool
        If True, discard grey values outside [min_GV, max_GV]
    pct_stack_import : float
        Percentage of stack to import, defaults to 10.
    Returns
    -------
    img
        Numpy array containing loaded image
    mu
        Numpy 1-D array of size (n_gaussians,) containing fitted means from Gaussian mixture model
    sigma
        Numpy 1-D array of size (n_gaussians,) containing fitted standard deviations from Gaussian mixture model
    weights
        Numpy 1-D array of size (n_gaussians,) containing fitted weights from Gaussian mixture model
    SNR_CNR_df
        Pandas DataFrame containing calculated SNR and CNR for all combinations of Gaussians
    """
    print("GMM Fitting \n===========")
    img = QM_load(img_fname, min_GV, max_GV, specify_gv, pct_stack_import) # import image from img_fname
    GMM = GMM_fit.GMM_fit(img, n_gaussians)
    mu, sigma, weights = GMM_fit.extract_GMM_results(GMM)
    out_dir = "{}_results".format(os.path.splitext(img_fname)[0])
    GMM_fit.save_GMM_results(img_fname, GMM)
    GMM_fit.plot_GMM_fit(img, GMM, img_fname)
    SNR_CNR_df = QM_calc(mu, sigma, out_dir)

    return img, mu, sigma, SNR_CNR_df

# Main

if __name__ == "__main__":
    img_fname = os.path.join(os.getcwd(), "test", "test.tif") # edit to match image filename
    QM_runner(img_fname, 3)