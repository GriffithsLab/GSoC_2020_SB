# -*- coding: utf-8 -*-
"""Unit test for a band by band comparison between a neural power spectrum model
and an observation using FOOOF tools"""

import sciunit
import numpy as np
from fooof import FOOOF
from fooof.bands import Bands
from fooof.analysis import get_band_peak_fm
from fooof.utils import trim_spectrum
from sciunit.scores import FloatScore
from FOOOF_unit.capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum

    
class _Band_by_Band(sciunit.Test):
  """Test comparing the power of detected peaks or of frequency band ranges of the observation and the prediction model  """

  def __init__(self, observation=None, name=None, band=None):
    super().__init__(observation=observation, name=name, band=band)
    self.band = band

  required_capabilities = (ProducesPowerSpectrum,)
  score_type = FloatScore
    
  def compare(self, fm1, fm2, band_def):
    """Implemented in the subclasses"""
    return NotImplementedError()
    
  def generate_prediction(self, model):
    res = model.produce_power_spectrum()
    frequency = res[0]
    spectrum = res[1]
    freq_range = res[2]

    prediction = {'freqs': frequency, 'powers': spectrum, 'freq_range': freq_range}
    return prediction

  def compute_score(self, observation, prediction):
    fm_obs = FOOOF()
    fm_obs.fit(observation['freqs'], observation['powers'], observation['freq_range'])
    fm_pred = FOOOF()
    fm_pred.fit(prediction['freqs'], prediction['powers'], prediction['freq_range'])

    bands = Bands(self.band)
    for label, definition in bands:
      score = self.score_type((self.compare(fm_pred, fm_obs, definition)))
    return score


class PeakPower(_Band_by_Band):

  def compare(self, fm1, fm2, band_def):
    """Compare the power of detected peaks."""

    pw1 = get_band_peak_fm(fm1, band_def)[1]
    pw2 = get_band_peak_fm(fm2, band_def)[1]

    return pw1 - pw2


class BandPower(_Band_by_Band):

  def compare(self, fm1, fm2, band_def):
    """Compare the power of frequency band ranges."""

    pw1 = np.mean(trim_spectrum(fm1.freqs, fm1.power_spectrum, band_def)[1])
    pw2 = np.mean(trim_spectrum(fm1.freqs, fm2.power_spectrum, band_def)[1])

    return pw1 - pw2
