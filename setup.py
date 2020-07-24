import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FOOOF_unit", 
    version="0.0.1",
    author="Sorenza Bastiaens",
    author_email="sorenza.bastiaens@gmail.com",
    description="A SciUnit library to test features of simulated neural power spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GriffithsLab/GSoC_2020_SB",  #Need to fill in
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
