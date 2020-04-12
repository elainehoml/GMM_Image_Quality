# Script for bokeh visualisation of GMM results

# Imports and housekeeping
import os
import numpy as np
from scipy.stats import norm
from bokeh.layouts import row
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Set2, Greys
from PIL import Image
import QM_load

# Functions

def bokeh_plot(img_fname):
    """ Generates Bokeh plot of img histogram and fitted GMM results
    Parameters
    ----------

    Returns
    -------

    """
    # Create plot
    basename = os.path.splitext(os.path.basename(img_fname))[0]
    p = figure(title="Image: {}, click on legend entries to hide".format(basename))
    #TODO[Elaine]: Figure out hover to show mu and sigma
    #TODO[Elaine]: Figure out how to use ColumnDataSource
    #TODO[Elaine]: Choose image from file input to view

    # Import image and generate histogram CDS
    img = QM_load.QM_load(img_fname)
    hist, edges = np.histogram(img, density=True, bins=int(0.25 * np.sqrt(len(img))))
    bin_width = edges[1] - edges[0]
    bin_midpoint = edges[:-1] + bin_width
    
    # Histogram
    p.vbar(x=bin_midpoint, top=hist, bottom=0, width=bin_width, alpha=0.5, legend_label="Image histogram")
    p.xaxis.axis_label = "Grey values"
    p.yaxis.axis_label = "Probability Density"

    # GMM results
    results_dir = "{}_results".format(os.path.splitext(img_fname)[0])
    GMM_results = np.loadtxt(os.path.join(results_dir, "fitted_results.csv"), delimiter=",")
    norm_mat = np.zeros([len(bin_midpoint), len(GMM_results)])
    colours = (Set2[8])
    for i in range(len(GMM_results)): # for each Gaussian
        mu = GMM_results[i,0]
        sigma = GMM_results[i,1]
        weight = GMM_results[i,2]
        y_norm = norm.pdf(bin_midpoint, mu, sigma) # y coordinates if area under dist = 1
        norm_mat[:,i] = y_norm * weight # y coordinates if weights are applied
        p.varea(x=bin_midpoint, y1=np.zeros(len(bin_midpoint)), y2=y_norm, alpha=0.3, color=colours[i], legend_label="Gaussian {}".format(str(i)))
        p.line(x=bin_midpoint, y=y_norm, line_color=colours[i], legend_label="Gaussian {}".format(str(i)))
    p.line(x=bin_midpoint, y=np.sum(norm_mat, axis=1), line_color="black", line_dash="dashed", legend_label="Sum of fitted Gaussians") # Sum of fitted Gaussians

    # Legend
    p.legend.click_policy = "hide"

    # Get image and open to central slice
    I = Image.open(img_fname)
    I.seek(int(I.n_frames/2))
    img_np = np.array(I)
    img_p_tooltips = [("x","$x"), ("y","$y"), ("grey value","@image")]
    img_p = figure(title=os.path.basename(img_fname), tooltips=img_p_tooltips)
    img_p.image(image=[img_np], x=0, y=0, dw=10, dh=10, palette=Greys[9], level="image")
    img_p.xgrid.visible = False
    img_p.ygrid.visible = False

    # Show
    output_file(os.path.join(results_dir, "{}_GMM_vis.html".format(basename)), title="{} GMM fit".format(basename))
    show(row(p, img_p))
    
    return p

# Main
if __name__ == "__main__": 
    test_fname = os.path.join(os.path.dirname(os.getcwd()), "test", "test.tif")
    img_basename = os.path.basename(test_fname)
    p = bokeh_plot(test_fname)
