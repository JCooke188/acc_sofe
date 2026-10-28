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
pip install argopy numpy xarray matplotlib
```