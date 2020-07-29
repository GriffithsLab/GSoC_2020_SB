# -*- coding: utf-8 -*-
"""Unit test for two neural power spectrum models in order to compare them by computing the correlation coefficient. 
Two types of score are avaiable: CorrelationScore or FloatScore"""

import fooof
import sciunit
import numpy as np
from FOOOF_unit.capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum
from scores.score_correlation import CorrelationScore
from sciunit.scores import FloatScore
from sciunit.tests import TestM2M

class Correlation2Spectrum(sciunit.TestM2M):
  """Test the similarity between two neural power spectra models by computing the correlation coefficient"""

  required_capabilities = (ProducesPowerSpectrum,)
  score_type = CorrelationScore

  def generate_prediction(self, model):
    res = model.produce_power_spectrum()
    frequency = res[0]
    spectrum = res[1]
    freq_range = res[2]

    from fooof import FOOOF #Note FOOOF package needs to be installed before-hand
    fm = FOOOF()
    fm.fit(frequency,spectrum,freq_range)
    prediction = spectrum
    return prediction

  def compute_score(self, prediction1, prediction2):
    score = self.score_type(float(np.corrcoef(prediction1, prediction2)[0,1]))
    return score
  
class Correlation2SpectrumFloat(Correlation2Spectrum):
  score_type = FloatScore
  FloatScore._best = 1.0
