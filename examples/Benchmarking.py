""" Create phantoms of known SNR and CNR, compare ground-truth with conventional and GMM SNR and CNR calculation """

# Import libraries
import os, sys
import numpy as np
from scipy import stats
from skimage import io
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set()
sns.set_style("white")
font = {'size' : 12}
plt.rc('figure', figsize=(8.27, 11.69)) # sets all plot to a4 portrait
plt.rc('font', **font)

# Import functions
root_dir = os.path.split(os.path.abspath(os.path.dirname(sys.argv[0])))[0]
test_dir = os.path.join(root_dir, "test")

sys.path.append(os.path.join(root_dir, "main"))
import QM_load
import GMM_fit
import QM_calc

sys.path.append(test_dir)
import create_phantom

# create phantom directory
phantom_dir = "examples/benchmarking_phantoms"
if os.path.isdir(phantom_dir) == False:
    os.mkdir(phantom_dir)

# Create phantom images with known SNR and CNR
""" SNR and CNR are altered by scaling the sigma values for the phantom image, where original
mu and sigma values were derived from the original image before reassigning GV """

def generate_mu_sigma_values():
    """ Calculate mu and sigma for phantom images and corresponding SNR and CNR, save to csv

    Parameters
    ----------
    None

    Returns
    -------
    Pandas Dataframe
        Contains mu and sigma values assigned to each phantom, and phantom_name to identify phantoms
    """

    mu_original = np.array([8, 35, 82]) # air, wax and tissue
    sigma_original = np.array([7, 6, 16]) # air, wax and tissue
    sigma_scaling_factor = [0.1, 0.2, 0.5, 1.0, 2.0, 4.0]
    mu_phantom = np.zeros([6,3])
    sigma_phantom = np.zeros([6,3])
    for i in range(len(sigma_scaling_factor)):
        mu_phantom[i,:] = mu_original
        sigma_phantom[i,:] = sigma_original*sigma_scaling_factor[i]
    output = np.concatenate((mu_phantom, sigma_phantom), axis = 1) # join for output to csv
    phantom_name_df = pd.DataFrame({"phantom_name": ["P1", "P2", "P3", "P4", "P5", "P6"]})
    output_df = pd.DataFrame(output)
    output_df.columns = ["mu_air", "mu_wax", "mu_tissue", "sigma_air", "sigma_wax", "sigma_tissue"]
    output_df = phantom_name_df.join(output_df)
    output_df.to_csv("{}/mu_sigma_GT.csv".format(phantom_dir), index = None)

    return output_df

def create_phantoms_varied(GT):
    """ Creates phantoms with mu and sigma values from mu_sigma_GT, saves as .tif with phantom_name

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue.
    
    Returns
    -------
    list
        Contains filenames where phantoms are stored as .tifs
    """    
    # create and save phantoms
    for index, row in GT.iterrows():
        mu_phantom = [row["mu_air"], row["mu_wax"], row["mu_tissue"]]
        sigma_phantom = [row["sigma_air"], row["sigma_wax"], row["sigma_tissue"]]
        phantom_fname = "{}/{}.tif".format(phantom_dir, row["phantom_name"])
        I = create_phantom.create_phantom(mu_phantom, sigma_phantom, test_dir)
        create_phantom.save_phantom(I, phantom_fname)

# Calculate ground truth SNR and CNR

def GT_SNR_CNR(GT):
    """ Calculates ground truth SNR and CNR and saves as .csv

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue.

    Returns
    -------
    None
    """

    for index, row in GT.iterrows():
        mu = np.array([row["mu_air"], row["mu_wax"], row["mu_tissue"]])
        sigma = np.array([row["sigma_air"], row["sigma_wax"], row["sigma_tissue"]])
        output_fname = "{}/{}_GT.csv".format(phantom_dir, row["phantom_name"])
        output_df = QM_calc.QM_calc(mu, sigma, results_dir = "NA", save_results = False, verbose = False) # will save results manually
        output_df.to_csv(output_fname)

# Fit GMMs, calculate SNR and CNR

def GMM_SNR_CNR(GT):
    """ Fits GMMs and calculates SNR and CNR for phantoms, save SNR and CNR as csv

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue. Used only to get filenames for phantom images.
    
    Returns
    -------
    None
    """

    for index, row in GT.iterrows():
        phantom_fname = "{}/{}.tif".format(phantom_dir, row["phantom_name"])
        I = QM_load.QM_load(phantom_fname)
        GMM = GMM_fit.GMM_fit(I, 3)
        mu_fitted, sigma_fitted, weights_fitted = GMM_fit.extract_GMM_results(GMM)
        GMM_fit.save_GMM_results(phantom_fname, GMM)
        GMM_fit.plot_GMM_fit(I, GMM, phantom_fname)
        plt.close()
        output_fname = "{}/{}_fitted.csv".format(phantom_dir, row["phantom_name"])
        output_df = QM_calc.QM_calc(mu_fitted, sigma_fitted, results_dir = "NA", save_results = False, verbose = False)
        output_df.to_csv(output_fname)

# Calculate SNR and CNR using conventional user-defined ROIs method

def SNR_CNR_conv(GT):
    """ Calculates SNR and CNR from average mu and sigma across 5 ROIs for each material, saves as .csv

    Parameters
    ----------
    GT : Pandas DataFrame
        Output from generate_mu_sigma_values which contains phantom_name, mu_air, mu_wax, mu_tissue, 
        sigma_air, sigma_wax, sigma_tissue. Used only to get filenames for phantom images.
    
    Returns
    -------
    None
    """

    for index, row in GT.iterrows():
        mu_conv = [] # 1-D list mu for air, wax, tissue for one phantom image
        sigma_conv = []
        materials = ["air", "wax", "tissue"]
        for material in materials:
            input_csv_fname = "{}/{}_results/{}_{}_mu_sigma.csv".format(phantom_dir, row["phantom_name"], row["phantom_name"], material)
            mu_sigma_conv = np.loadtxt(input_csv_fname, delimiter = ",", skiprows = 1, usecols = (1,2))
            mu_sigma_avg = np.mean(mu_sigma_conv, axis = 0)
            mu_conv.append(mu_sigma_avg[0])
            sigma_conv.append(mu_sigma_avg[1])
        output_fname = "{}/{}_conv.csv".format(phantom_dir, row["phantom_name"])
        output_df = QM_calc.QM_calc(mu_conv, sigma_conv, results_dir = "NA", save_results = False, verbose = False)
        output_df.to_csv(output_fname)
    
def r2_val(x, y):
    """ Calculate r**2 value """
    slope, intercept, rval, pval, stderr = stats.linregress(x, y)
    return rval**2

def summary_plots():
    """ Plots summary plots comparing conventional, GMM fitted and ground truth SNR and CNR """
    # Import data
    phantoms = ["P1", "P2", "P3", "P4", "P5", "P6"]
    conv = {} # empty dict for conventional SNR and CNR summary
    GMM = {} # empty dict for GMM SNR and CNR summary
    GT = {} # empty dict for GT SNR and CNR summary
    Gaussians_compared = np.loadtxt("{}/{}_conv.csv".format(phantom_dir, "P1"), delimiter = ",", skiprows = 1, usecols = (0,1))

    def prep_df(dict_name, csv_name):
        """ Reads .csv SNR and CNR files and creates summary .csv and df """
        # insert Gaussians to be compared
        dict_name["Gaussian_A"] = Gaussians_compared[:,0]
        dict_name["Gaussian_B"] = Gaussians_compared[:,1]

        # insert SNR and CNR values
        for phantom in phantoms:
            input_csv = np.loadtxt("{}/{}_{}.csv".format(phantom_dir, phantom, csv_name), delimiter = ",", skiprows = 1)
            dict_name["{}_SNR".format(phantom)] = input_csv[:,2]
            dict_name["{}_CNR".format(phantom)] = input_csv[:,3]
        
        df = pd.DataFrame.from_dict(dict_name)
        df.to_csv("{}/{}_summary.csv".format(phantom_dir, csv_name), index = None)
        
        return pd.DataFrame.from_dict(dict_name)

    conv_df = prep_df(conv, "conv")
    GMM_df = prep_df(GMM, "fitted")
    GT_df = prep_df(GT, "GT")
    
    def conv_gmm_gt_comp(cols, CNR_or_SNR):
        """ fill this in """
        titles = ["Air-Wax", "Air-Tissue", "Wax-Air", "Wax-Tissue", "Tissue-Air", "Tissue-Wax"]
        fig = plt.figure()
        sns.set_style("white")
        for i in range(6):
            xvals = GT_df.iloc[i,cols]
            conv_yvals = conv_df.iloc[i,cols]
            GMM_yvals = GMM_df.iloc[i,cols]
            ax = plt.subplot(3,2,i+1)
            # r2_conv = r2_val(xvals, conv_yvals) # calculate r^2 value for conv
            # r2_GMM = r2_val(xvals, GMM_yvals) # calculate r^2 value for GMM
            plt.plot(xvals, xvals, "k--", label = "Ground Truth", alpha = 0.8)
            plt.plot(xvals, conv_yvals, "^", label = "Conventional", alpha = 0.8)
            plt.plot(xvals, GMM_yvals, "o", label = "GMM", alpha = 0.8)
            plt.yscale("log")
            plt.xscale("log")
            plt.title(titles[i])
            plt.tight_layout()
            plt.xlabel("Ground Truth {}".format(CNR_or_SNR))
            plt.ylabel("Measured {}".format(CNR_or_SNR))
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc = "lower center", ncol = 3)
        plt.tight_layout()
        fig.subplots_adjust(top=0.961,bottom=0.117,left=0.077,right=0.971,hspace=0.426,wspace=0.273)
        plt.savefig("examples/benchmarking_plots/{}_comparison.png".format(CNR_or_SNR))
    
    def sns_lin_reg(cols, CNR_or_SNR):
        """ Plots linear regression of GMM and conv vs GT, along with residuals

        Parameters
        ----------
        cols : list
            List of column numbers to take from df
            [2,4,6,8,10,12] for SNR, [3,5,7,9,11,13] for CNR
        CNR_or_SNR : str
            Choose between "CNR" or "SNR" for axes labels
        """
        # Arrange data
        xvals = []
        GMM_yvals = []
        conv_yvals = []
        for i in range(6):
            xvals.append(GT_df.iloc[i, cols].values)
            GMM_yvals.append(GMM_df.iloc[i, cols].values)
            conv_yvals.append(conv_df.iloc[i, cols].values)
        xvals_flat = np.array(xvals).flatten()
        GMM_flat = np.array(GMM_yvals).flatten()
        conv_flat = np.array(conv_yvals).flatten()

        # Linear regression plots
        plt.figure()
        sns.set_style("white")
        plt.subplot(211)
        sns.regplot(xvals_flat, GMM_flat)
        plt.xlabel("Ground Truth {}".format(CNR_or_SNR))
        plt.ylabel("GMM {}".format(CNR_or_SNR))
        plt.subplot(212)
        sns.regplot(xvals_flat, conv_flat)
        plt.xlabel("Ground Truth {}".format(CNR_or_SNR))
        plt.ylabel("Conventional {}".format(CNR_or_SNR))
        plt.savefig("examples/benchmarking_plots/{}_linreg.png".format(CNR_or_SNR))

        # Residual plots
        plt.figure()
        sns.set_style("white")
        plt.subplot(211)
        plt.xlabel("Ground Truth {}".format(CNR_or_SNR))
        plt.ylabel("GMM Residuals")
        sns.residplot(xvals_flat, GMM_flat)
        plt.subplot(212)
        sns.residplot(xvals_flat, conv_flat)
        plt.xlabel("Ground Truth {}".format(CNR_or_SNR))
        plt.ylabel("Conventional Residuals")
        plt.savefig("examples/benchmarking_plots/{}_residuals.png".format(CNR_or_SNR))


    # scatter plot of conv and gmm vs gt
    # SNR
    cols = [2,4,6,8,10,12]
    # conv_gmm_gt_comp(cols, "SNR")
    sns_lin_reg(cols, "SNR")
    #TODO[Elaine]: Show r^2 values maybe?

    # CNR
    cols = [3,5,7,9,11,13]
    # conv_gmm_gt_comp(cols, "CNR")
    sns_lin_reg(cols, "CNR")

    # print("Ground Truth")
    # print(GT_df)
    # print("Conventional")
    # print(conv_df)
    # print("GMM")
    # print(GMM_df)

# Main ---------------------------------------------------------------------------------------------------
mu_sigma_GT = generate_mu_sigma_values()
# create_phantoms_varied(mu_sigma_GT)
# GT_SNR_CNR(mu_sigma_GT) # calculate ground truth snr and cnr
# GMM_SNR_CNR(mu_sigma_GT) # calculate gmm snr and cnr

# Once ROIs have been selected using Conventional_SNR_CNR.ijm in Fiji,
# SNR_CNR_conv(mu_sigma_GT) # calculate conventional snr and cnr
summary_plots()

