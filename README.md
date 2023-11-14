
# PyCom

Python Library (both local and remote!) & REST API for accessing the PyCom Database.

PyCom is an open-source, queryable database of Protein Residue-Residue Contacts (Coevolution Matrices) and annotation data derived from UniProt (Swiss-Prot to be precise!) using HHBlits/HHFilter/CCmpred.

More information can be found at: https://pycom.brunel.ac.uk/

## Installation

Install the PyCom library with:

`pip install git+https://github.com/scdantu/pycom`

Requirements:
- Python 3.8+
- numpy / pandas / h5py / requests, installed automatically

## Downloads

Get the `pycom.db` and `pycom.mat` files (**115 GB** total) from:

https://pycom.brunel.ac.uk/downloads/

**Not necessary** for remote use.


## Examples / Tutorials

### Local Use

Examples can be found in [pycom_example_local.ipynb](https://github.com/scdantu/pycom/blob/main/tutorials/pycom_example_local.ipynb).
This requires the `pycom.db` and `pycom.mat` files.

### Remote Library

The library can be used remotely without downloading the `pycom.db` and `pycom.mat` files.
A tutorial can be found in [pycom_example_remote.ipynb](https://github.com/scdantu/pycom/blob/main/tutorials/pycom_example_remote.ipynb).

### API

It is also possible to call the REST API directly.
**Documentation** (Swagger): https://pycom.brunel.ac.uk/api/spec/
**Endpoint**: https://pycom.brunel.ac.uk/api/
**Mini Tutorial**: [03_WebAPI.ipynb](https://github.com/scdantu/pycom/blob/main/tutorials/jp_notebooks/getting_started/03_WebAPI.ipynb)

## Contributions

The [PyComDB database creation](https://github.com/cemiu/pycom_generator) and HPC deployment was largely done by [Philipp Bibik](https://github.com/cemiu) under scientific advisement from [Sarath Dantu](https://github.com/scdantu).

The Python interface and REST API (this repo) was primary written by Philipp Bibik, with contributions from Sarath Dantu.

Tutorials and documentation were created by Sarath Dantu and Philipp Bibik.

Sarath Dantu served as the PI for this project. Without additional support from Alessandro Pandini, this project would not have been possible.