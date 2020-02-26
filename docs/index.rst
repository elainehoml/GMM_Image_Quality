.. GMM_Image_Quality documentation master file, created by
   sphinx-quickstart on Wed Feb  5 14:47:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

******************
GMM Image Quality
******************

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3688733.svg
   :target: https://doi.org/10.5281/zenodo.3688733

The GMM Image Quality tool provides a semi-automated tool for calculating signal-to-noise ratio (SNR)
and contrast-to-noise ratio (CNR) from X-ray microcomputed tomography (microCT) datasets.

Features
--------
* Repeatable, objective measurement of SNR and CNR
* Graphical user interface provided as a Jython plugin for Fiji/ImageJ
* Automatic saving of results in .csv files for further analysis
* Importable Python libraries for scripting

Background
----------

SNR and CNR are image quality metrics describing the clarity of a feature in relation to the
image noise. SNR and CNR are typically determined by comparing intensities of user-defined regions
containing the feature of interest and the background. However, this method is tedious and impractical
when comparing between many 3D image datasets.

Reiter_ et al. proposed a region-of-interest (ROI) independent method of determining CNR from image 
intensity distributions of microCT datasets. MicroCT intensities are proportional to material-dependent
X-ray attenuation, so it is assumed that the overall image intensity for multi-material specimens
is the sum of individual Gaussian distributions for each material.

This tool presents a semi-automated tool for determining SNR and CNR from microCT data using
Gaussian Mixture Models (GMMs_). GMMs estimate the mean, variance and weight of a user-specified
number of Gaussian components from the image intensity distribution. These properties are then used 
to calculate SNR and CNR between any combination of the Gaussian components, even for low contrast 
image with overlapping distributions.

.. _Reiter: https://pdfs.semanticscholar.org/ae77/9e665006f34229a900ab9817ce888a1ea4ae.pdf
.. _GMMs: https://scikit-learn.org/stable/modules/mixture.html

Availability
------------
This software tool is available from https://github.com/elainehoml/GMM_Image_Quality under the 
GNU General Public License v3.0.

For issues/suggestions, feel free to contact me at eml.ho@soton.ac.uk. 

This work was completed with support from the Engineering and Physical Sciences Research Council (EPSRC), Institute for Life Sciences, University of Southampton during a doctoral research studentship from the Faculty of Engineering and the Environment, University of Southampton.

Authors
-------
E.M.L. Ho [1], C. Rossides [1,2], O. Katsamenis [3], P. Lackie [2,4], P. Schneider [1,3]

1. Bioengineering Science Research Group, Faculty of Engineering and Physical Sciences, University of Southampton, UK.
2. School of Clinical and Experimental Sciences, Faculty of Medicine, University of Southampton, UK.
3. :math:`\mu`-VIS X-ray Imaging Centre, Faculty of Engineering and Physical Sciences, University of Southampton, UK.
4. Biomedical Imaging Unit, Clinical & Experimental Sciences, Faculty of Medicine, University of Southampton, UK.

Citation
--------

If you found this helpful, please cite us:

Elaine Ming Li Ho, Charalambos Rossides, Orestis Katsamenis, Peter M. Lackie, & Philipp Schneider. (2020, February 26). Objective and repeatable image quality assessment with Gaussian mixture models (Version v1.0.0). Zenodo. http://doi.org/10.5281/zenodo.3688733

Get Started
------------
.. toctree::
   :maxdepth: 2
   
   installation.rst
   userguide.rst
   examples.rst
