import os, csv
import QM_runner, QM_get_params

user_params = QM_get_params.QM_get_params()

img, mu, sigma, SNR_CNR_df = QM_runner.QM_runner(img_fname = user_params['img_fname'], n_gaussians = user_params['n_gaussians'], pct_stack_import = user_params['pct_stack_import'])

print('done')

# TODO(Elaine): Enable min/max grey value limits in QM_runner.QM_runner