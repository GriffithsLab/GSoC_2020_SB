# SB_GSoC_2020
Project repo for Sorenza Bastiaens' GSoC 2020 work

(In progress)

## FOOOF_unit

A python package for running validation tests on models generating a neural power spectrum using the SciUnit-framework and FOOOF tool to parameterize the spectrum.

## About SciUnit

[SciUnit](https://scidash.org/sciunit.html) is an easy-to-use framework for developing data-driven “model validation tests”. Each test generates and statistically validates predictions from a model against one relevant feature of empirical data to produce a score indicating agreement between the model and the data. These tests can be used to clearly identify the merits and limitations of existing models and developmental progress on new models. NeuronUnit was then developed, a library that builds on SciUnit to make neuron model validation as easy as possible. With the growing field of computational neuroscience, more and more complex brain models are emerging which are focused on large-scale brain network dynamics. The Python package we have develped, `FOOOF_unit`, implements `SciUnit` tests for several features of neural power spectra, as computed from either empirical or simulated neural time series using the `FOOOF` library. We have focused here on empirical M/EEG and neural mass modeel simulations using The Virtual Brain (TVB) simulator, but the methodology is quite generic and can be easily applied to other modalities and simulators. Our `FOOOF_unit` tests build upon the formalized validation scheme of the SciUnit package. SciUnit is based on the design, documentation, and implementation of classes in Python. Four different types of classes have been written: `capabilities`, `models`, `scores` and `tests`. 

## About FOOOF 

[FOOOF](https://fooof-tools.github.io/fooof/index.html) is a tool parametrizing neural power spectra by breaking it into an aperiodic component reflecting 1/f characteristics and a number of periodic components defined as a set of peaks parametrized by a Gaussian function. The FOOOF tool also gives the option to generate power spectra with aperiodic and periodic components of our choice for testing purposes. 
In each test the neural power spectrum of the model is parametrized with FOOOF as follows:

```python
fm = FOOOF()
fm.fit(prediction['freqs'], prediction['powers'], prediction['freq_range'])
```

From the `fm` object created, information of interest can be easily retrieved with specific functions such as `fm.get_params('peak_params', 'CF')`, which gives the central frequency of each peak detected. 

The following three images represents a time-series, the corresponding power spectrum and the parametrized result with FOOOF:

![image](https://user-images.githubusercontent.com/62792658/91423729-36f54b00-e859-11ea-90f6-72f4a1a4364e.png)

## Description

The current tests available validate features observed in the neural power spectrum. The simulated neural power spectrum tested is wrapped in a model class, `NeuralPowerSpectra`, which implements the capability class `ProducesPowerSpectrum`. The frequency, spectrum and frequency range values of the neural power spectrum of interest is required. Each unit test correspond to a different usage of SciUnit. The three tests developed:
1) Determine wether a peak is present within a specific frequency range. This is a model versus feature unit test. The tests checks wether a certain feature is produced by the model.
2) Compare the band power of a model against an observation (also possible to compare the detected peaks power). This corresponds to a model versus empirical data unit test. The model is tested against the data. 
3) Compare two models against each other by computing the correlation coefficient. The final test is a model versus model test. The model is tested against a reference modeL. 
 
Complete [examples](https://github.com/GriffithsLab/GSoC_2020_SB/tree/master/examples) on how to run each tests are presented in the folder ‘examples’ in separate files. All the tests first parametrize the neural power spectrum with the FOOOF tool and compute the score of interest.
 
The folder `FOOOF_unit` contains all the capabilities, models and scores needed to run the tests following the SciUnit framework.

The utils.py file contains a function (`common_fr_bands`) that loads the frequency range values of the most common brain waves: theta, alpha, beta and gamma. 
The io.py file contains functions to load and visualize data used as examples.

## Use Case Example With TVB

In addition to the three simple examples, a use case of the package is presented using models generated with The Virtual Brain. In this example, a code was developed to form a database of the results obtained with CentralPeak test (assess presence of peak within a frequency range) for each simulations obtained with TVB. The power spectrum of the simulations is computed with the function in welch_psd.py which uses Welch's method. 

### About TVB

The Virtual Brain ([TVB](https://docs.thevirtualbrain.org/)) is a neuroinformatics platform and is a framework for the simulation of the dynamics of large-scale brain networks with biologically realistic connectivity. TVB has a collection of neuronal dynamics models where parameters can be varied and adapted. Various neural mass models are available in the repertoire of TheVirtualBrain and define the dynamics of a network node. 
It is also possible to run simulations for Single-Node models which is what is done in this example. We focused on three models: [Generic2DOscillator](http://docs.thevirtualbrain.org/_modules/tvb/simulator/models/oscillator.html), [Wilson-Cowan](http://docs.thevirtualbrain.org/_modules/tvb/simulator/models/wilson_cowan.html#WilsonCowan) and [Jansen-Rit](http://docs.thevirtualbrain.org/_modules/tvb/simulator/models/jansen_rit.html)

### Database

The aim is to create a database for each model of the `CentralPeak` result for different brain waves ranges by performing parameter sweeps. This enables the user to determine which parameters can be used to produce peak of interests. The code used can be found in db folder make_database.py

The code to generate the database for any number of parameters is in the [db](https://github.com/GriffithsLab/GSoC_2020_SB/tree/master/FOOOF_unit/db) folder (make_database.py). As input a json file is required with information on the parameters of interest as well as which model is simulated. An example of the json file required is in data.json. The parameter name and values, the model and the frequency range to run the CentralPeak test are required. 
In addition to the json file, if another filename is given as an argument, the database is saved in a .csv file. The final result will look as following: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/62792658/91425286-3cec2b80-e85b-11ea-8a1d-3f37b28c0607.png" />
</p>

Once the database is made, parameters of interest can be selected and visualized in a heatmap. The influence of each parameter can be assessed. Here, is an example of a parameter sweep for 4 different parameters  of `CentralPeak` test within the alpha frequency range for a generic dynamic system with two state variables (Generic2DOscillator).

![Heatmap](https://user-images.githubusercontent.com/62792658/91424291-ea5e3f80-e859-11ea-9217-5baf558ece04.png)

## Installation
 
Installation is best done using `pip`

The principal non-standard Python dependencies are: `sciunit`, `fooof`, `tvb-library`, `tvb-data`

Install from source with the following on the command line:

```bash
git clone https://github.com/GriffithsLab/GSoC_2020_SB
cd GSoc_2020_SB
pip install -e .
```


## License

This code is licensed under [MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments


