"Function to get the PSD using Welch's method for simulations "
import pandas as pd
from scipy.signal import welch

def Welch_PSD(varied_param, param_names, simulations, output):
  index_PSD = pd.MultiIndex.from_tuples(varied_param, names=param_names)
  PSD = pd.DataFrame(index=index_PSD, columns = ['freqs', 'spectrum'])
  for param in varied_param:
    Final = simulations.loc[param, output]
    freqs, psd = welch(Final, fs=1/(1*0.001), nperseg=2500)
    PSD.loc[(param, 'freqs')] = freqs
    PSD.loc[(param, 'spectrum')] = psd
  return PSD