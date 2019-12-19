import os, csv

def QM_get_params():
    """ Gets user parameters output from QM_fiji.py

    Parameters
    ----------
    None

    Returns
    -------
    dict
        Dict containing user parameters
        - min_gv: minimum grey value (optional), defaults to 0
        - max_gv: maximum grey value (optional), defaults to 255
        - pct_stack_import: % of stack to import
        - img_fname: image filename to import
        - n_gaussians: number of Gaussians to fit
        - specify_gv: if True, limit grey values to min_gv, max_gv
    """
    # Find users_params.txt
    f = open(os.path.join(os.getcwd(), "main", "temp_user_dir.txt"), "r")
    user_params_fname = f.readlines()[0]
    f.close()
    print(user_params_fname)
    
    # Open users_params.txt
    with open(user_params_fname, "r") as f:
        reader = csv.reader(f, delimiter = ",")
        for i, row in enumerate(reader):
            if i == 0:
                keys = row
            if i == 1:
                vals = row
    user_params = dict(zip(keys, vals))

    # Format values properly
    user_params['max_gv'] = float(user_params['max_gv'])
    user_params['min_gv'] = float(user_params['min_gv'])
    user_params['pct_stack_import'] = float(user_params['pct_stack_import'])
    user_params['n_gaussians'] = int(user_params['n_gaussians'])
    user_params['specify_gv'] = user_params['specify_gv'] == "True"
    
    return user_params