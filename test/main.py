# Import libraries
import os
import unittest

# Import test scripts
import test_outputs
# import test_phantom

if __name__ == "__main__":
    
    # Test if outputs are correct
    suite = unittest.TestLoader().loadTestsFromTestCase(test_outputs.Test_Outputs)
    unittest.TextTestRunner(verbosity = 2).run(suite)
    
    # Phantom validation
    # I_phantom, mu_phantom, sigma_phantom = create_phantom.create_phantom()
    # create_phantom.show_phantom(I_phantom)