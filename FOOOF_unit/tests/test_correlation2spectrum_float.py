# -*- coding: utf-8 -*-
import fooof
import sciunit
import numpy as np
from tests.test_correlation2spectrum import Correlation2Spectrum
from capabilities.cap_ProducesPowerSpectrum import ProducesPowerSpectrum
from sciunit.scores import FloatScore
from sciunit.tests import TestM2M

class Correlation2SpectrumFloat(Correlation2Spectrum):
  score_type = FloatScore
