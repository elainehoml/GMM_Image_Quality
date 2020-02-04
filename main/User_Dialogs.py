import os,sys,csv
from fiji.util.gui import GenericDialogPlus
from javax.swing import JFrame, JButton, JList
from java.awt import GridLayout, BorderLayout
from ij.measure import ResultsTable
from ij import IJ, ImagePlus

# Import Run_CPython
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)
import Run_CPython

# Misc utilities
def get_results_dir():
    """ Gets results directory of current GMM fit from temp_user_dir.txt

    Parameters
    ----------
    None

    Returns
    -------
    str
        Results directory filepath
    """
    # Get results_dir from temp_user_dir where Users_Params.csv filepath is stored
    temp_user_dir = os.path.join(script_path, "temp_user_dir.txt")
    f = open(temp_user_dir, "r")
    results_dir = f.read().strip("Users_Params.csv")
    f.close()

    return results_dir

# User Dialog Functions
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

def show_as_RT(event):
    """ Shows calculated SNR and CNR as a Results Table, read from saved csv
    Parameters
    ----------
    event : Event
        Waits for show_as_RT_JB JButton to be pressed
    
    Returns
    -------
    ResultsTable
        Contains calculated SNR and CNR for each combination of Gaussians
    """

    # Open SNR_CNR_Results.csv as a ResultsTable
    SNR_CNR_fname = os.path.join(get_results_dir(), "SNR_CNR_Results.csv")
    SNR_CNR_RT = ResultsTable.open2(SNR_CNR_fname)
    SNR_CNR_RT.show("SNR and CNR")

    return SNR_CNR_RT

def show_thresholded(event):
    """ Show virtual stack of image thresholded to mu +/- 1x sigma of each Gaussian component

    Parameters
    ----------
    event : Event
        Waits for show_thresholded_JB JButton to be pressed

    Returns
    -------
    None
    """

    # Get image filename
    results_dir = get_results_dir()
    with open(os.path.join(results_dir, "Users_Params.csv")) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            img_fname = row['img_fname']
            n_gaussians = int(row['n_gaussians'])
    print("Displaying image {} with {} Gaussians fitted".format(img_fname, n_gaussians))
   
    # Read mu and sigma from results directory
    with open(os.path.join(results_dir, "fitted_results.csv")) as csv_file:
        reader = csv.reader(csv_file)
        results = [] # list containing lines in fitted_results.csv
        for row in reader:
            results.append(row)
    mu_all = []
    sigma_all = []
    for i in range(3, len(results)):
        mu_all.append(float(results[i][0]))
        sigma_all.append(float(results[i][1]))

    # Calculate values for thresholding (mu +/- 1x sigma)
    lower_threshold = map(lambda mu, sigma: mu - sigma, mu_all, sigma_all)
    upper_threshold = map(lambda mu, sigma: mu + sigma, mu_all, sigma_all)

    # Display each slice thresholded with the Gaussian number in title
    for gaussian in range(n_gaussians):
        imp = IJ.openVirtual(img_fname)
        imp.setTitle("Gaussian {}".format(gaussian))
        imp.show()
        IJ.setThreshold(imp, lower_threshold[gaussian], upper_threshold[gaussian])
        print("Gaussian {} threshold values [{} - {}]".format(gaussian, lower_threshold[gaussian], upper_threshold[gaussian]))
