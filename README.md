# SB_GSoC_2020
Project repo for Sorenza Bastiaens' GSoC 2020 work

(In progress)

## FOOOF_unit

A python package for running validation tests on models generating a neural power spectrum using the SciUnit-framework and FOOOF tool to parameterize the spectrum.

## Description

The current tests available validate features observed in the neural power spectrum. The simulated neural power spectrum tested is wrapped in a model class (NeuralPowerSpectra). The frequency, spectrum and frequency range values of the neural power spectrum of interest is required.  The tests developed are able to:
1) Determine if a peak is present in specific brain waves frequency range (or any frequency range)
2) Compare the band power of a model against an observation (also possible to compare the detected peaks power)
3) Compare two models against each other by computing the correlation coefficient
 
Examples on how to run each tests are presented in the folder ‘examples’ in separate files. All the tests first parametrize the neural power spectrum with the FOOOF tool and compute the score of interest.
 
The folder FOOOF_unit contains all the capabilities, models and scores needed to run the tests following the SciUnit framework.

The utils.py file contains a function (common_fr_bands) that loads the frequency range values of the most common brain waves: theta, alpha, beta and gamma. 
The io.py file contains functions to load and visualize data used as examples.

## Installation
 
Dependant packages:
- SciUnit (pip install sciunit)
- FOOOF (pip install fooof)

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments

