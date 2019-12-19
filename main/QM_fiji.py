import os, csv
from fiji.util.gui import GenericDialogPlus
from javax.swing import JFrame, JButton, JList
from java.awt import GridLayout, BorderLayout

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
    print("Results directory:", results_dir)

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
    print(temp_user_dir)

    return user_params

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
    frame.setLayout(GridLayout(1, 1))

    # Define JButtons
    get_user_params_JB = JButton("Load image and settings", actionPerformed = get_user_params)
    # TODO(Elaine): JButton for displaying results as a ResultsTable
    # TODO(Elaine): JButton for displaying thresholded images

    # Add JButtons to frame
    frame.add(get_user_params_JB)

    frame.setVisible(True)

# Main --------------------------------------------------------------------

main_menu()
    