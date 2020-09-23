# -*- coding: utf-8 -*-
"""Neural Power Spectra SciUnit data class"""

import sciunit
from fooofunit.capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum


class DataModel(sciunit.Model,ProducesPowerSpectrum):
  """Model that creates a frozen data trace of the neural power spectrum of the data."""
  def __init__(self, freqs, powers, freq_range, name=None):
        self.freqs = freqs
        self.powers = powers
        self.freq_range = freq_range
        super(DataModel, self).__init__(name=name, freqs=freqs, powers=powers, freq_range=freq_range)

  def produce_power_spectrum(self):
        return (self.freqs, self.powers, self.freq_range)
