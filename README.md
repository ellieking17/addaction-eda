# Addaction exploratory data analysis
> Notebooks containing the code for the exploratory data analysis


# Installing / Getting started

Clone this repo and then set up your python 3.6.2 virtual environment

## Python version
Python 3.6.2

## Virtual environment
Create a new python 3.6.2 virtual environment using your favourite virtual environment manager (you may need pyenv to specify python version).

All commands here are executed in the terminal

### Environment variable
- Set the environment variable DATADIR in the .env file to be the path in which the unzipped csv files are saved.
- Source the environment variable from the .env `source .env`.
- You can check it's loaded using `echo $DATADIR` or `printenv`.


### Python packages
Then install required python packages:

`pip install -r requirements.txt`

### Run notebooks
Run a jupyter session

either `jupyter notebook`

or `pip install jupyterlab`
`jupyter lab`

