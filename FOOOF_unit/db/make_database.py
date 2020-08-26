"Functions used to create a database for CentralPeak test"

import sciunit
import json
from FOOOF_unit import capabilities, models, scores, tests
from fooof import FOOOF
import os,sys,glob, numpy as np, pandas as pd
from itertools import product
from itertools import groupby
from FOOOF_unit.capabilities import ProducesPowerSpectrum
from FOOOF_unit.models import NeuralPowerSpectra
from FOOOF_unit.tests import CentralPeak
from FOOOF_unit.utils import common_fr_bands
from FOOOF_unit.welch_psd import Welch_PSD
from tvb.simulator import models
from scipy.signal import welch



class Single_Node_TVB:

  def __init__(self, fixed_param, option):
    self.fixed_param = fixed_param
    self.option = option

  def simulation(self, n_step, dt, initial):
    n_step = n_step
    dt = dt

    # Parameters for the model passed
    fixed_params = self.fixed_param
    fixed_params = {k: np.array(v) for k,v in fixed_params.items()}

    # Initialize model instance with fixed params for Generic2DOscillator, Wilson-Cowan or Jansen-Rit
    if (self.option=='Wilson-Cowan'):
      initconds = initial
      mod = models.WilsonCowan(**fixed_params)

      # Execute single-node simulation run
      time,dat = mod.stationary_trajectory(n_step=n_step,dt=dt, initial_conditions=initconds)
        
      # Output from TVB sims is always a 4D array. Reorganize into a 2D pandas dataframe      
      E_dat = np.squeeze(dat[:,0,:,:])
      I_dat = np.squeeze(dat[:,1,:,:])  
      return E_dat

    elif (self.option=='Jansen-Rit'):
      #initial = np.array([0.5,0.5,0.5,0.5,0.5,0.5])[:,np.newaxis]
      initconds = initial
      mod = models.JansenRit(**fixed_params)
      
      time,dat = mod.stationary_trajectory(n_step=n_step, dt=dt, initial_conditions=initconds)
      
      #Uncomment if want to return other variables of the Jansen-Rit model
      y0_dat = np.squeeze(dat[:,0,:,:])
      #y1_dat = np.squeeze(dat[:,1,:,:])
      #y2_dat = np.squeeze(dat[:,2,:,:])
      #y3_dat = np.squeeze(dat[:,3,:,:])
      #4_dat = np.squeeze(dat[:,4,:,:])
      #y5_dat = np.squeeze(dat[:,5,:,:])
      return y0_dat
      # Define simulation details

    else:
      initconds = initial
      mod = models.Generic2dOscillator(**fixed_params)

      time,dat = mod.stationary_trajectory(n_step=n_step,dt=dt,
                                          initial_conditions=initconds)    
      V_dat = np.squeeze(dat[:,0,:,:])
      W_dat = np.squeeze(dat[:,1,:,:])  
      return V_dat
      
      
def TVB_database(model, parameters, names, fr_range, outfile=None):
  #model:string, parameters: tuple with all parameters, fr_range: string('alpha', 'beta', 'theat' or 'gamma')

  varied_params = list(product(*parameters))
  param_names = names
  if (model=='Generic2DOscillator'):
        data_name = 'V'
        default = dict(d = 0.075 ,  tau = 3.0, I = -0.4,
                    f = 1/3, e = 0.0, beta = 0.8,  a = 0.7, alpha=1.0, c=0.0, b=-1.0, g=0.0)        
  elif (model=='Wilson-Cowan'):
        data_name = 'E'
        default = dict(alpha_i=1.0, alpha_e=1.0, c_e=1.0, c_i=1.0, Q=0, P=1.25, b_e=4.0, b_i=3.7,
                          a_e=1.3, a_i=2.0, tau_e=10.0, tau_i=10.0, r_e=1.00, r_i=1.00,
                          k_e=1.00, k_i=1.00, c_ee=16.0, c_ei= 12.0, c_ie = 16.0, c_ii=11.0)
  elif (model=='Jansen-Rit'):
        data_name = 'y0'
        default = dict(J = 135.0, A= 3.25, B=22.0, mu = 0.22)

  sim_param = default.copy()
  simulation_param = {}
  for j in range(0, len(varied_params)):
    for i in range(0, len(param_names)):
      sim_param[param_names[i]] = varied_params[j][i]
      simulation_param[varied_params[j]]= sim_param
    sim_param = default.copy()
    
  n_step = 50000    #Simulation time can be changed
  dt = 0.1
  arr = np.linspace(0.0, n_step*dt, int((n_step*dt)+1))
  time = arr.tolist()
  index_multi = list(product(*parameters, time))
  index = pd.MultiIndex.from_tuples(index_multi, names=[*names, 'time'])
  simulations = pd.DataFrame(index=index, columns = [data_name], dtype='float64')

  for params in varied_params:
    if (model=='Generic2DOscillator'):
        initial = np.array([-3.,-3.])[:,np.newaxis]
    elif (model=='Wilson-Cowan'):
        initial = np.array([0.,0.])[:,np.newaxis]
    elif (model=='Jansen-Rit'):
        initial = np.array([0.5,0.5,0.5,0.5,0.5,0.5])[:,np.newaxis]

    fixed_param = simulation_param[params]
    TVB_obj = Single_Node_TVB(fixed_param, model)
    data = TVB_obj.simulation(n_step, dt, initial)
    simulations.loc[params, data_name] = data

  PSD = Welch_PSD(varied_params, param_names, simulations, data_name)

  model_t = {}
  t=0
  for param in varied_params:
    model_t[t] = NeuralPowerSpectra(PSD.loc[param, 'freqs'], PSD.loc[param, 'spectrum'], [1,50], name="Model = %s" %(param,))
    t = t+1

  bands = common_fr_bands(fr_range)
  band_tests = [CentralPeak(name=key, min_peak=0.8, band=value)
          for key, value in bands.items()]
  band_suite = sciunit.TestSuite(band_tests)

  model_tot = list(model_t.values())
  res_tot = band_suite.judge(model_tot)

  df = res_tot.score
  iterables = [*parameters]
  multiindex = pd.MultiIndex.from_product(iterables, names=param_names)
  df.index = np.array(multiindex)
  new_result = df.reindex(multiindex)
  df = new_result
  df.columns = ['result '+fr_range]

  if (model=='Generic2DOscillator'):
    new_res = df.copy()
    all_param_names = ['d','tau', 'I', 'f', 'e', 'beta', 'a', 'c', 'b', 'alpha', 'g']
    for key, value in default.items():
      if (key not in sorted(new_res.index.names)):
        new_res[key] = value
        new_res.set_index(key, append=True, inplace=True)
    new_res = new_res.reorder_levels(all_param_names)
    
    if (outfile!=None):
      new_res = new_res.sort_index()
      new_res.to_csv(outfile)
    else:
      pass
    
  else:
    if (outfile!=None):
      new_res = df.sort_index()
      new_res.to_csv(outfile)
    else:
      pass
      
  return new_res

def load_json(filename):
    with open(filename, 'r') as fp:
      data = json.load(fp)
    return data

def main(params_file,out_file):
    data = load_json(params_file)
    p_names = []
    all_params = []
    for key, values in (data['parameters'].items()):
      all_params.append(values)
      p_names.append(key)
    all_params = tuple(all_params)
    
    res_alpha = TVB_database(data['model'], all_params, p_names, data['fr_range'],out_file)
    
if __name__ == "__main__":
    """
    Usage: 

    python make_database.py params_file.json outfile.csv
    
    """

    params_file = sys.argv[1]
    out_file = sys.argv[2]

    main(params_file,out_file)
