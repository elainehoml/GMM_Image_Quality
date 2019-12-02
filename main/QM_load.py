def QM_load(img_fname, pct_stack_import = 10.):
    """Loads n slices of a 3D image stack specified by percentage of stack to import

    Parameters
    ----------
    img_fname : str
        Filepath of image to be loaded
    pct_stack_import : float, default 10.
        Percentage of stack to import. Used to calculate number of slices to import, evenly spaced throughout stack
    
    Returns
    -------
    img
        3D numpy array with only n slices imported based on pct_stack_import
    """
    start = time.time()

    I = Image.open(img_fname)
    n_slices = int(I.n_frames * (pct_stack_import/100)) # calculate number of slices to import
    img_list = []
    for i in np.arange(0, n_slices):
        I.seek(int((i+1)*(I.n_frames/(n_slices + 1)))) # evenly spaced slices through stack
        img = np.array(I)
        img_list.append(img)
    
    end = time.time()
    
    sys.stdout.write("Image imported, time elapsed = {0:.2f} s\n".format((end-start)))
    
    return np.asarray(img_list)