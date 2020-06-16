# -*- coding: utf-8 -*-
"""SciUnit capability: Produces Power Spectrum"""

import sciunit

class ProducesPowerSpectrum(sciunit.Capability):
  """Capability for producing a power spectrum"""

  def produce_power_spectrum(self):
    """The implementation of this method should return a power spectrum."""
    raise NotImplementedError("Must implement produce_power_spectrum.")
