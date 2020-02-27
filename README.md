# GMM Image Quality
Objective and repeatable image quality assessment with Gaussian mixture models

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3688733.svg)](https://doi.org/10.5281/zenodo.3688733)

Quantifying image quality enables objective optimisation of imaging protocols. Signal-to-noise ratio (SNR) and contrast-to-noise ratio (CNR) measure visibility of features in relation to the image noise. Conventional SNR and CNR measurement is performed by user selection of regions in the image representing each material, which is not repeatable and impractical for large numbers of 3D datasets. Here, a semi-automated, objective and repeatable method of calculating SNR and CNR is presented which does not require user definition of regions-of-interest. This method utilises Gaussian mixture models to separate materials in the specimen based on the grey value distribution of the image. This tool is available as a graphical user interface for Fiji/ImageJ users, and as importable libraries for Python users under the GNU General Public License v3.0.

Have a look at our documentation here for installation and user guides: 

[![Documentation Status](https://readthedocs.org/projects/gmm-image-quality/badge/?version=latest)](https://gmm-image-quality.readthedocs.io/en/latest/?badge=latest)

Report bugs and request features by raising an issue at on the [issue tracker](https://github.com/elainehoml/GMM_Image_Quality/issues "Issue Tracker")

If you found this helpful, please cite us:

Elaine Ming Li Ho, Charalambos Rossides, Orestis Katsamenis, Peter M. Lackie, & Philipp Schneider. (2020, February 26). Objective and repeatable image quality assessment with Gaussian mixture models (Version v1.0.0). Zenodo. http://doi.org/10.5281/zenodo.3688733
