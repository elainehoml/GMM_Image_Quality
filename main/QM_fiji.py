import os,sys,csv
from fiji.util.gui import GenericDialogPlus
from javax.swing import JFrame, JButton, JList
from java.awt import GridLayout, BorderLayout

# Import Run_CPython
#script_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(script_path)
import Run_CPython
import User_Dialogs

# User dialogs -------------------------------------------------------------

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
    nButtons = 4
    frame.setSize(100 * nButtons, 300)
    frame.setLayout(GridLayout(nButtons, 1))

    # Define JButtons
    get_user_params_JB = JButton("Load image and settings", actionPerformed = User_Dialogs.get_user_params)
    fit_GMM_JB = JButton("Fit Gaussian Mixture Model", actionPerformed = User_Dialogs.fit_GMM)
    show_as_RT_JB = JButton("Show SNR and CNR as Results Table", actionPerformed = User_Dialogs.show_as_RT)
    show_thresholded_JB = JButton("Show thresholded stack", actionPerformed = User_Dialogs.show_thresholded)

    # Add JButtons to frame
    frame.add(get_user_params_JB)
    frame.add(fit_GMM_JB)
    frame.add(show_as_RT_JB)
    frame.add(show_thresholded_JB)
    frame.setVisible(True)

# Main --------------------------------------------------------------------

main_menu()
    