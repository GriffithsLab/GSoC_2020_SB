"Functions used to create a database for CentralPeak test"

#Import all modules and libraries of interest
import sciunit
import json
from fooofunit import capabilities, models, scores, tests
from fooof import FOOOF
import os,sys,glob, numpy as np, pandas as pd
from itertools import product
from itertools import groupby
from fooofunit.capabilities import ProducesPowerSpectrum
from fooofunit.models import NeuralPowerSpectra
from fooofunit.tests import CentralPeak
from fooofunit.utils import common_fr_bands
from fooofunit.welch_psd import Welch_PSD
from tvb.simulator import models
from scipy.signal import welch
from p_tqdm import p_map
import multiprocessing
from functools import partial


class Single_Node_TVB:
  """Class to execute Single-Node simulations for three TVB model: Generic2DOcillator, Wilson-Cowan and Jansen-Rit"""

  # Initialize class model type (Generic2DOcillator, Wilson-Cowan and Jansen-Rit) and their corresponding parameter values
  def __init__(self, fixed_param, option):
    self.fixed_param = fixed_param
    self.option = option

  # Function to run single-node simulation on the model initialized with parameters of interest.
  def simulation(self, n_step, dt, initial):

    # Length and step size of the simulation
    n_step = n_step
    dt = dt

    # Parameters of the model passed
    fixed_params = self.fixed_param
    fixed_params = {k: np.array(v) for k,v in fixed_params.items()}

    # Run simulation for a Wilson-Cowan model
    if (self.option=='Wilson-Cowan'):

      # Initial conditions. Example: np.array([0.,0.])[:,np.newaxis]
      initconds = initial

      mod = models.WilsonCowan(**fixed_params)

      # Execute single-node simulation run
      time,dat = mod.stationary_trajectory(n_step=n_step,dt=dt, initial_conditions=initconds)

      # Output from TVB sims is always a 4D array. Reorganize into a 2D pandas dataframe. Wilson-Cowan has two state variable. E_dat represent activity of
      # excitatory cells and I_dat inhibitory cells. Uncomment to obtain I_dat
      E_dat = np.squeeze(dat[:,0,:,:])
      # I_dat = np.squeeze(dat[:,1,:,:])
      return E_dat

    # Run simulation for a Jansen-Rit model
    elif (self.option=='Jansen-Rit'):


      # Initial Conditions. Example: np.array([0.5,0.5,0.5,0.5,0.5,0.5])[:,np.newaxis]
      initconds = initial
      mod = models.JansenRit(**fixed_params)

      # Execute single-node simulation run
      time,dat = mod.stationary_trajectory(n_step=n_step, dt=dt, initial_conditions=initconds)

      # Uncomment if want to return other variables of the Jansen-Rit model. Each correspond to a different state-variable.
      y0_dat = np.squeeze(dat[:,0,:,:])
      #y1_dat = np.squeeze(dat[:,1,:,:])
      #y2_dat = np.squeeze(dat[:,2,:,:])
      #y3_dat = np.squeeze(dat[:,3,:,:])
      #4_dat = np.squeeze(dat[:,4,:,:])
      #y5_dat = np.squeeze(dat[:,5,:,:])
      return y0_dat

    # Run simulation for a Generic2DOscillator model
    else:

      # Initial conditions. Example: np.array([-3.,-3.])[:,np.newaxis]
      initconds = initial
      mod = models.Generic2dOscillator(**fixed_params)

      time,dat = mod.stationary_trajectory(n_step=n_step,dt=dt,
                                          initial_conditions=initconds)
      # Generic2DOscillator has two state variables. V_dat represents a function of the neuron's membrane potential, such as the firing rate and
      # W_dat is a recovery variable. Uncomment fort W_dat.
      V_dat = np.squeeze(dat[:,0,:,:])
      #W_dat = np.squeeze(dat[:,1,:,:])
      return V_dat


def TVB_database(model, varied_params, names, fr_range):
  """ Function to generate a database with CentralPeak test results of three TVB models (Generic2DOscillator, Wilson-Cowan and Jansen-Rit) for different
    parameter combinations (parameter sweep)"""

  param_names = names
    
  if (type(varied_params) == tuple):
      print('yes')
      parameters = varied_params
      varied_params = list(product(*parameters))
  else:
      #Obtain arrays for each parameter with their corresponding values
      parameters = []
      print('no')
      for i in range(len(param_names)):
         parameters.append([elem[i] for elem in varied_params])
      parameters = [list(dict.fromkeys(i)) for i in parameters]
      parameters = tuple(parameters)

  # Default values of each models
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

  # Dictionary with simulation parameters for each parameter combination
  sim_param = default.copy()
  simulation_param = {}
  for j in range(0, len(varied_params)):
    for i in range(0, len(param_names)):
      sim_param[param_names[i]] = varied_params[j][i]
      simulation_param[varied_params[j]]= sim_param
    sim_param = default.copy()

  # Initialize DataFrame with all simulation results
  n_step = 50000    #Simulation time can be changed
  dt = 0.1
  arr = np.linspace(0.0, n_step*dt, int((n_step*dt)+1))
  time = arr.tolist()
  index_multi = list(product(*parameters, time))
  index = pd.MultiIndex.from_tuples(index_multi, names=[*names, 'time'])
  simulations = pd.DataFrame(index=index, columns = [data_name], dtype='float64')

  # Execute single-node simulation for each model
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

  # Obtain Neural Power Spectrum of each TVB simulation with Welch's method. PSD is a dataframe with all the neural power spectra.
  PSD = Welch_PSD(varied_params, param_names, simulations, data_name)

  # Instantiate NeuralPowerSpectra model class with each TVB simulation neural power spectum.
  model_t = {}
  t=0
  for param in varied_params:
    model_t[t] = NeuralPowerSpectra(PSD.loc[param, 'freqs'], PSD.loc[param, 'spectrum'], [1,50], name="Model = %s" %(param,))
    t = t+1

  # Instantiate CentralPeak test class with frequency range of interest. fr_range is a string corresponding to the brain wave of interest: 'theta', 'alpha', 'beta' or 'gamma'
  bands = common_fr_bands(fr_range)
  band_tests = [CentralPeak(name=key, min_peak=0.8, band=value)
          for key, value in bands.items()]
  band_suite = sciunit.TestSuite(band_tests)

  # Test executed with judge method. A boolean score is returned: 'Pass' if a peak is present in the frequency range, 'Fail' otherwise.
  model_tot = list(model_t.values())
  res_tot = band_suite.judge(model_tot)

  # Rearrange the score matrix
  df = res_tot.score
  iterables = [*parameters]
  multiindex = pd.MultiIndex.from_product(iterables, names=param_names)
  df.index = np.array(multiindex)
  new_result = df.reindex(multiindex)
  new_result.columns = ['result '+fr_range]

  if (model=='Generic2DOscillator'):
     all_param_names = ['d','tau', 'I', 'f', 'e', 'beta', 'a', 'c', 'b', 'alpha', 'g']
     for key, value in default.items():
       if (key not in sorted(new_result.index.names)):
         new_result[key] = value
         new_result.set_index(key, append=True, inplace=True)
     new_result = new_result.reorder_levels(all_param_names)
  else:
      pass

  return new_result


def csv_file(result_dataframe, fr_range, filename):
#Function to create .csv file and save result
    if (os.path.isfile('./'+filename)==True):
      database = pd.read_csv(filename, index_col=list(range(len(result_dataframe.index.names))))
      if ('result '+fr_range in sorted(database)):
        new = pd.DataFrame(database['result '+fr_range])
        total = new.append(result_dataframe)
        sort = total.sort_index()
        new_database = sort[~sort.index.duplicated(keep='last')]
        del database['result '+fr_range]
        result = pd.concat([database, new_database], axis=1)
      else:
        total = pd.concat([database,result_dataframe], axis=1)
        sort = total.sort_index()
        result = sort[~sort.index.duplicated(keep='last')]
      result.to_csv(filename)
    else:
      result_dataframe= result_dataframe.sort_index()
      result_dataframe.to_csv(filename)
    print('File Saved')


def load_json(filename):
    """Function to load json file with information on the parameters of interest"""

    with open(filename, 'r') as fp:
      data = json.load(fp)
    return data


def _sbfoo(params, model, names, range):
    """Function to run TVB_database (used for multiprocessing purposes)"""

    res_alpha = TVB_database(model, params, names, range)
    return res_alpha


if __name__ == '__main__':

    #Load json file with information on model, parameter values and frequency range
    data = load_json('data_test.json')

    #Get all parameter values and their names
    p_names = []
    all_params = []
    for key, values in (data['parameters'].items()):
      all_params.append(values)
      p_names.append(key)
    all_params = tuple(all_params)

    #Make list with all parameter combinations
    all_varied_params = list(product(*all_params))

    #Separate the list into sub-lists
    chunk_size = int((len(all_varied_params)/(multiprocessing.cpu_count())))
    new_list = [all_varied_params[i:i+chunk_size] for i in range(0, len(all_varied_params), chunk_size)]

    #Create p_map for multiprocessing with non-iterable arguments. Iterable arguments is the list with sub lists
    non_itargs = partial(_sbfoo, model=data['model'], names=p_names, range=data['fr_range'])
    res = p_map(non_itargs, new_list)

    #All p_map results are concacenated together
    dataframe_res = (pd.concat(res))

    #Function to create .csv file with the result
    csv_file(dataframe_res, data['fr_range'], 'G_multi.csv')
