# MalConv-Pytorch
A Pytorch adaptation of MalConv for Android apks

---
## Desciprtion

This is the adaptation of MalConv proposed in [Malware Detection by Eating a Whole EXE](https://arxiv.org/abs/1710.09435) for Android apks 

## Dependency

- numpy
- pytorch
- pandas


## Setup

#### Preparing data

- Place all malware and benign apks under `raw-data` folder.
- Run `python3 prepare-data.py`

All files will be placed under data folder

Labels will be stored in `train.csv` and `valid.csv`

#### Training
```
python3 train.py -x <experiment number>
Example : python3 train.py -x 0
```

## Parameters & Model Options

For parameters and options available: `python3 main.py -h`
