# -*- coding: utf-8 -*-
"""Neural Power Spectra SciUnit model class"""

import sciunit
from capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum


class NeuralPowerSpectra(sciunit.Model, ProducesPowerSpectrum):
    """A model that produces a neural power spectrum as output. Requires frequency, power values and frequency range of interest."""
    def __init__(self, freqs, powers, freq_range, name=None):
        self.freqs = freqs
        self.powers = powers
        self.freq_range = freq_range
        super(NeuralPowerSpectra, self).__init__(name=name, freqs=freqs, powers=powers, freq_range=freq_range)

    def produce_power_spectrum(self):
        return (self.freqs, self.powers, self.freq_range)
