from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fp:
    install_requires = fp.read().splitlines()

setup(
    name="FOOOF_unit", 
    version="0.0.1",
    author="Sorenza Bastiaens",
    author_email="sorenza.bastiaens@gmail.com",
    description="A SciUnit library to validate features of simulated neural power spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = install_requires,
    url='git@github.com:GriffithsLab/fooof-unit.git',  #Need to fill in
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
