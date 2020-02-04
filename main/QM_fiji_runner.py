import os, csv
import QM_runner, QM_get_params

user_params = QM_get_params.QM_get_params()

img, mu, sigma, SNR_CNR_df = QM_runner.QM_runner(img_fname = user_params['img_fname'], \
    n_gaussians = user_params['n_gaussians'], min_GV = user_params['min_gv'], max_GV = user_params['max_gv'], \
        specify_gv = user_params['specify_gv'], pct_stack_import = user_params['pct_stack_import'])

print('done')
