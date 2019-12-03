import os
import sys
sys.path.append(os.path.join(os.getcwd(), "main"))
import QM_runner
import unittest
import QM_load
import QM_fit
import QM_calc

def QM_run_test():
    """ Runs example SNR and CNR measurement workflow to test if outputs are in the correct form
    Parameters
    ----------
    None
    Returns
    -------
    img.shape
        Dimensions of the loaded image "test.tif" - should be xxx
    mu
        Numpy 1-D array of size 3 containing means of Gaussians fitted to grey value histogram of "test.tif"
    sigma
        Numpy 1-D array of size 3 containing standard deviations of Gaussians fitted to grey value histogram of "test.tif"
    SNR_CNR_df
        Pandas DataFrame of SNR and CNR calculated from every combination of fitted Gaussians
    """
    print("Tests to ensure outputs are in the correct format \n")
    
    img_fname = os.path.join(os.getcwd(), "test", "test.tif") # test image 'test.tif'
    img, mu, sigma, SNR_CNR_df = QM_runner.QM_runner(img_fname, 3) # run the workflow

    return img.shape, mu, sigma, SNR_CNR_df

img_shape, mu, sigma, SNR_CNR_df = QM_run_test()

class Test_Outputs(unittest.TestCase):
    def test_img_dimensions(self):
        """ Compare image dimensions loaded by QM_load
        Raises
        ------
        AssertionError
            QM_load returns wrong image shape of 'Test.tif'. Should be (5, 345, 418)
        """
        self.assertEqual(img_shape, (5, 345, 418), "Test.tif dimensions should be (5, 345, 418)")

    def test_mu_sigma_shape(self):
        """ Tests if mu and sigma outputs have correct dimensions
        Raises
        ------
        AssertionError
            mu or sigma output should have shape (3,)
        """
        self.assertEqual(mu.shape, (3,), "mu should have shape (3,)")
        self.assertEqual(sigma.shape, (3,), "sigma should have shape (3,)")
    
    def test_SNR_CNR_df_shape(self):
        """ Tests if SNR_CNR_df has correct dimensions
        Raises
        ------
        AssertionError
            SNR_CNR_df should have shape (6,3)
        """
        self.assertEqual(SNR_CNR_df.shape, (6,3), "SNR_CNR_df should have shape (3,)")
    
    def test_results_dir(self):
        """ Tests if results directory is correctly created and populated
        Raises
        ------
        AssertionError
            Results directory should be created in same directory as image, as <img_name>_results
        AssertionError
            Results directory should have 3 files
        """
        out_dir = os.path.join(os.getcwd(), "test", "test_results")
        self.assertTrue(os.path.isdir(out_dir), "Results directory does not exist")
        self.assertEqual(len(os.listdir(out_dir)), 3, "Results directory should have 3 files inside")

# suite = unittest.TestLoader().loadTestsFromTestCase(Test_Outputs)
# unittest.TextTestRunner(verbosity = 2).run(suite)