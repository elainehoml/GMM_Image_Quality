.. GMM_Image_Quality documentation master file, created by
   sphinx-quickstart on Wed Feb  5 14:47:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

******************
GMM Image Quality
******************

The GMM Image Quality tool provides a semi-automated tool for calculating signal-to-noise ratio (SNR)
and contrast-to-noise ratio (CNR) from X-ray microcomputed tomography (microCT) datasets.

Features
--------
* Repeatable, objective measurement of SNR and CNR
* Graphical user interface provided as a Jython plugin for Fiji/ImageJ
* Automatic saving of results in .csv files for further analysis

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
Apache License 2.0.

For issues/suggestions, feel free to contact me at eml.ho@soton.ac.uk. 

This work was completed with support from the Engineering and Physical Sciences Research Council (EPSRC), Institute for Life Sciences, University of Southampton during a doctoral research studentship from the Faculty of Engineering and the Environment, University of Southampton.

Get Started
------------
.. toctree::
   :maxdepth: 2
   
   installation.rst
   userguide.rst
   examples.rst
