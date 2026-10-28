# Analysis of Circumpolar Cross-Frontal Exchange in the Southern Ocean
*Created by Justin Cooke, Postdoctoral Fellow at the University of Rhode Island, Graduate School of Oceanography


## Highlights

Main functions of this repository:

- argo_fetcher.py: Script to fetch and save Argo float data as a 2d array, for a user defined region, depth range, and time range. 
- seir_validation.ipynb: Notebook to validate the code against published results from Johnson Exley et al. 2025

## Overview

This repository contains the necessary scripts and notebooks to gather Argo profile data and conduct an analysis of along streamline cross-frontal exchange.

### Required modules

```bash
pip install argopy numpy xarray matplotlib ipykernel jupyter bash_kernel
```

### Setting up kernel for use with jupyter notebook

After installing the modules, you need to set up a kernel within your virtual environment to run with jupyter notebook.

```bash
ipython kernel install --user --name=myenv
```

Replace myenv with the name of your environment.

Install the bash_kernel next

```bash
python -m bash_kernel.install
```

Run your Jupyter Notebook. If using VSCode, you can run the following:

```bash
jupyter-notebook --no-browser --ip=0.0.0.0 --port 8888
```

Copy the url, it will look something like:

```bash
http://compute-node-name-00:8888/tree?token=randomtoken
```

Select your kernel, choose existing jupyter server and copy the url.