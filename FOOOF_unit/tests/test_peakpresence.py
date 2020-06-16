# -*- coding: utf-8 -*-
"""Unit test for neural power spectrum model to determine
if a peak is present within a specific frequency range for
the model and an observation
"""

import sciunit
from fooof import FOOOF
from sciunit.scores import BooleanScore
import numpy as np
from capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum

class PeakPresence(sciunit.Test):
  """Test if a peak is present within a specific frequency range of the power spectrum for the prediction and the observation"""

    def __init__(self, observation=None, name=None, min_peak = 0.0, band=None):
      super().__init__(observation=observation, name=name)
      self.min_peak = min_peak
      self.band = band

    required_capabilities = (ProducesPowerSpectrum,)
    score_type = BooleanScore

    def validate_observation(self, observation):
      assert isinstance(observation, dict)
      for key in ['freqs', 'powers']:
        assert key in observation
      assert isinstance(observation['freqs'], np.ndarray)
      if 'freq_range' not in observation:
        fr = observation['freqs']
        observation['freq_range'] = [fr[0], fr[-1]]

    def generate_prediction(self,model):
      res = model.produce_power_spectrum()
      frequency = res[0]
      spectrum = res[1]
      freq_range = res[2]

      prediction = {'freqs': frequency, 'powers': spectrum, 'freq_range': freq_range}
      return prediction

    def compute_score(self,observation,prediction):
      fm_pred = FOOOF(min_peak_height=self.min_peak)
      fm_pred.fit(prediction['freqs'], prediction['powers'], prediction['freq_range'])
      pred_cfs = fm_pred.get_params('peak_params', 'CF')
      score = self.score_type(bool(((pred_cfs >= self.band[0]) & (pred_cfs <= self.band[-1])).any()))
      return score

    def _bind_score(self, score, model, observation, prediction):
      fm_obs = FOOOF()
      fm_obs.fit(observation['freqs'], observation['powers'], observation['freq_range'])
      obs_cfs = fm_obs.get_params('peak_params', 'CF')

      obs_score = self.score_type(bool(((obs_cfs >= self.band[0]) & (obs_cfs <= self.band[-1])).any()))
      score.related_data = obs_score
      score.observation = obs_score
