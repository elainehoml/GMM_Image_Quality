def QM_fit(img, n_gaussians, out_dir):
    """ Fits Gaussian mixture model to grey value histogram of img

    Parameters
    ----------
    img : numpy array
        3D numpy array of image, output from QM_load.py
    n_gaussians : int
        Number of Gaussian components to fit to histogram, usually equals number of material components in specimen
    out_dir : str
        Path to results directory
    
    Returns
    -------
    mu
        Numpy 1-D array of size = n_gaussians with the mean(s) of fitted Gaussian component(s) as floats. Also written to .csv
    sigma
        Numpy 1-D array of size = n_gaussians with the standard deviation(s) of fitted Gaussian component(s) as floats. Also written to .csv
    """

    # Fit Gaussian mixture model --------------------------------------------------------------------------------------------------
    
    start = time.time()

    img_1d = img.flatten() # flatten 3D img array

    GMM = sklearn.mixture.GaussianMixture(n_components = n_gaussians, random_state = 3) # fix random state for predictability
    GMMfit = GMM.fit(img_1d.reshape(-1,1))
    
    end = time.time()

    sys.stdout.write("GMM fit complete, time elapsed = {0:.2f} s\n".format((end-start)))

    # Plot histogram ---------------------------------------------------------------------------------------------------------------
    
    fig = plt.figure()
    ax = plt.subplot(111)
    bins = int(0.25 * np.sqrt(len(img_1d)))
    histo = plt.hist(img_1d, bins = bins, density = True, linewidth = 0)

    # Extract mu and sigma from fitted model ---------------------------------------------------------------------------------------

    mu_fitted = GMM.means_.reshape([n_gaussians]) # extract means
    sigma_fitted = np.sqrt(GMM.covariances_.reshape([n_gaussians])) # standard deviation = sqrt(variance)
    weights_fitted = GMM.weights_.reshape([n_gaussians]) # extract weights

    sort_ind = np.argsort(mu) # list of indices sorted in ascending order of mu
    mu_fitted = mu_fitted[sort_ind]
    sigma_fitted = sigma_fitted[sort_ind]
    weights_fitted = weights_fitted[sort_ind]
    norm_mat = np.zeros([len(histo[1]), len(mu_fitted)]) # store y-coordinates of normal distribution to be plotted

    # Plot fitted Gaussians and save to out_dir ---------------------------------------------------------------------------------------
    
    for i in range(0, len(mu)): # plot normal distributions with fitted mu and sigma, scaled with corresponding weights
        y = norm.pdf(histo[1], mu_fitted[i], sigma_fitted[i]) # generate normal distribution
        norm_mat[:,i] = y*weights[i] # scale by weight, write y-coordinates to norm_mat
        gauss = plt.plot(histo[1], y, label = "Gaussian {}, $\mu$ = {0:.2f}, $\sigma$ = {0:.2f}".format(i, mu_fitted[i], sigma_fitted[i], weights_fitted[i]))
        
        x_mu = np.full([2,], mu_fitted[i]) # x-coord of vertical line marking mean of Gaussian
        y_mu = [0., np.max(y)] # y-coords of vertical line marking mean of Gaussian
        plt.plot(x_mu, y_mu, color = gauss[0]._color)
        plt.text(mu_fitted[i], y_mu[1], "{}".format(i), horizontalalignment = "center")
    
    plt.plot(histo[1], np.sum(norm_mat, axis = 1), "k--", label = "Sum of fitted Gaussians") # Plot sum of fitted Gaussians
    plt.xlabel("Grey Values")
    plt.ylabel("Probability Density")
    ax.legend(bbox_to_anchor = (0.8, -0.2))
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "histo.png"))
    plt.show()
    sys.stdout.write("Histogram plotted and saved to {}".format(out_dir))

    # Write mu and sigma to csv -----------------------------------------------------------------------------------------------------

    with open(os.path.join(out_dir, "fitted_results.csv"), "w", newline = "") as csv_file:
        w = csv.writer(csv_file, delimiter = ",")
        csv_file.write("# Image filename = {}".format(img_fname))
        csv_file.write("# Fitted Gaussians")
        csv_file.write("# Mean, Standard Deviation, Weight")
        for i in range(len(mu_fitted)):
            to_write = [mu_fitted[i], sigma_fitted[i], weights_fitted[i]]
            w.writerow(to_write) # writes mu, sigma and weight of each fitted Gaussian as a new row
    
    return mu_fitted, sigma_fitted