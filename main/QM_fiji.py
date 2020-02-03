import os,sys,csv
from fiji.util.gui import GenericDialogPlus
from javax.swing import JFrame, JButton, JList
from java.awt import GridLayout, BorderLayout

# Import Run_CPython
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)
import Run_CPython

# User dialogs -------------------------------------------------------------

def get_user_params(event):
    """ Allows user to select file and user parameters

    Parameters
    ----------
    event : Event
        Waits for get_user_params_JB JButton to be pressed
    
    Returns
    -------
    dict
        Dict containing filename, number of Gaussians to fit,
        % of dataset to import, whether to specify grey value
        limits, minimum grey value and maximum grey value to 
        consider (optional)
    """
    # Open user dialog
    gui = GenericDialogPlus("Define user parameters")
    gui.addFileField("Image filename", "Select image file")
    gui.addNumericField("Number of Gaussians to fit: ", 2, 0)
    gui.addNumericField("Percentage of dataset to import: ", 15, 0)
    gui.addCheckbox("Specify grey value limits?", False)
    gui.addNumericField("Min grey value (optional): ", 0, 0)
    gui.addNumericField("Max grey value (optional): ", 255, 0)
    gui.showDialog()

    # Extract user parameters
    if gui.wasOKed():
        user_params = {} # empty dict
        user_params['img_fname'] = str(gui.getNextString())
        user_params['n_gaussians'] = int(gui.getNextNumber())
        user_params['pct_stack_import'] = float(gui.getNextNumber())
        user_params['specify_gv'] = gui.getNextBoolean()
        user_params['min_gv'] = float(gui.getNextNumber())
        user_params['max_gv'] = float(gui.getNextNumber())
    
    # Create results directory
    results_dir = os.path.splitext(user_params['img_fname'])[0] + "_results"
    if os.path.isdir(results_dir) == False:
        os.mkdir(results_dir)
    print("Results directory: {}".format(results_dir))

    # Write user parameters to text file
    user_params_fname = os.path.join(results_dir, "Users_Params.csv")
    with open(user_params_fname, "wb") as f:
        w = csv.DictWriter(f, user_params.keys())
        w.writeheader()
        w.writerow(user_params)

    # Write directory to look for user params to text file in main/
    temp_user_dir = os.path.join(os.path.dirname(__file__), "temp_user_dir.txt")
    if os.path.isfile(temp_user_dir) == True:
        os.remove(temp_user_dir) # delete temp_user_dir.txt if present
    f = open(temp_user_dir, "w")
    f.write(user_params_fname)
    f.close()

    return user_params

def fit_GMM(event):
    """ Calls QM_fiji_runner.py from cmd to fit GMM
    
    Parameters
    ----------
    event : Event
        Waits for fit_GMM_JB JButton to be pressed
    
    Returns
    -------
    img
        Numpy array containing loaded image
    mu
        Numpy 1-D array of size (n_gaussians,) containing fitted means from Gaussian mixture model
    sigma
        Numpy 1-D array of size (n_gaussians,) containing fitted standard deviations from Gaussian mixture model
    SNR_CNR_df
        Pandas DataFrame containing calculated SNR and CNR for all combinations of Gaussians
    """
    print("Running GMM fit, this might take a while... \n")
    Run_CPython.run_CPython(script_path, "QM_fiji_runner.py")

def main_menu():
    """ Main menu which is always open

    Parameters
    ----------
    None

    Returns
    -------
    JFrame
        Main menu with JButtons calling other functions
    """
    frame = JFrame("GMM Image Quality Calculator")
    frame.setSize(400, 300)
    frame.setLayout(GridLayout(2, 1))

    # Define JButtons
    get_user_params_JB = JButton("Load image and settings", actionPerformed = get_user_params)
    fit_GMM_JB = JButton("Fit Gaussian Mixture Model", actionPerformed = fit_GMM)
    # TODO(Elaine): JButton for fitting GMM
    # TODO(Elaine): JButton for displaying results as a ResultsTable
    # TODO(Elaine): JButton for displaying thresholded images

    # Add JButtons to frame
    frame.add(get_user_params_JB)
    frame.add(fit_GMM_JB)

    frame.setVisible(True)

# Main --------------------------------------------------------------------

main_menu()
    