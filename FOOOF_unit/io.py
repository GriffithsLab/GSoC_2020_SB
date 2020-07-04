"""Functions to load MEG data .mat and visualize them all in one plot"""

def load_data_mat(f):
    
  from scipy.io import loadmat
  import pandas as pd
  mat = loadmat(f,struct_as_record=False,squeeze_me=True)['freq']
  hcp_ps = pd.DataFrame(mat.powspctrm,columns=mat.freq,index=mat.label).T
  hcp_ps = hcp_ps.loc[3:45]
  hcp_ps_norm = hcp_ps / hcp_ps.sum(axis=0)
  mean_psd = hcp_ps_norm.mean(axis=1)

  frequency = mean_psd.index.values
  spectrum = mean_psd.values
  freq_range = [0,45]
  observation = {'freqs': frequency, 'powers': spectrum, 'freq_range': freq_range}
  return observation, hcp_ps_norm


def visualize_multiple_data(all_ps):
  
  import pandas as pd
  from matplotlib import pyplot as plt

  df_all_ps = pd.concat(all_ps,sort=False)
  fig, ax = plt.subplots(ncols=2,figsize=(12,3))
  df_all_ps.mean(axis=1).unstack().T.loc[:30].plot(ax=ax[0])
  df_all_ps.mean(axis=1).unstack().T.loc[:30].plot(ax=ax[1],logx=True)
  plt.tight_layout()