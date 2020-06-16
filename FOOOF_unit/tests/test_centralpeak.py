# -*- coding: utf-8 -*-
"""Unit test for neural power spectrum model to determine
if a peak is present within a specific frequency range using FOOOF
to parametrize the power spectrum
"""
import sciunit
from fooof import FOOOF
from sciunit.scores import BooleanScore
import numpy as np
from capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum

class CentralPeak(sciunit.Test):
  """Test for models only if a peak is present within a specific frequency range of the power spectrum"""

  def __init__(self, name=None, min_peak=0.0, band=None):
    super().__init__(None, name=name)
    self.min_peak = min_peak
    self.band = band

  required_capabilities = (ProducesPowerSpectrum,) # The one capability required for a model to take this test.
  score_type = BooleanScore # This test's 'judge' method will return a BooleanScore.

  def validate_observation(self, observation):
    assert observation is None

  def generate_prediction(self, model):
    res = model.produce_power_spectrum()
    frequency = res[0]
    spectrum = res[1]
    freq_range = res[2]

    prediction = {'freqs': frequency, 'powers': spectrum, 'freq_range': freq_range}
    return prediction

  def compute_score(self, observation, prediction):
    fm = FOOOF(min_peak_height=self.min_peak)
    fm.fit(prediction['freqs'], prediction['powers'], prediction['freq_range'])
    pred_cfs = fm.get_params('peak_params', 'CF')

    score = self.score_type(bool(((pred_cfs >= self.band[0]) & (pred_cfs <= self.band[-1])).any())) # Returns a BooleanScore.
    return score
