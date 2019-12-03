# Import libraries
import os

# Import QM functions

from QM_load import QM_load
from QM_fit import QM_fit
from QM_calc import QM_calc

# Main

if __name__ == "__main__":
    img_fname = os.path.join(os.getcwd(), "test", "test.tif")
    img = QM_load(img_fname, 10)

    out_dir = os.path.join(os.getcwd(), "test", "results") # create out_dir
    if os.path.isdir(out_dir) == False:
        os.mkdir(out_dir)
    mu, sigma = QM_fit(img, 3, out_dir, img_fname)
    SNR_CNR_df = QM_calc(mu, sigma, out_dir)