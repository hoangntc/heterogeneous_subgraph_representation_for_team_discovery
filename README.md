# Learning Heterogeneous Subgraph Representations for Team Discovery

## Directory structure
```
.
|   README.md
|   installation.txt
|   pygnn.yml
|
|--- experiments
|   1_prepare_data_DBLP.ipynb
|   2_prepare_data_IMDB.ipynb
|   3_predict_expert.ipynb
|
|--- prepare_dataset: preprocess source code
|--- src: model source code
|   

```

## Model Architecture

![Model architecture](/figure/overview.png)

## Installation

For installation, please follow the instruction in the file `installation.txt`


## Reproduction
1. Data preprocessing: Run `experiments/1_prepare_data_DBLP.ipynb` or `experiments/2_prepare_data_IMDB.ipynb`
2. Model training: `sh script/train.sh`
3. Team representation inference: Run `experiments/3_predict.ipynb`
3. Team discovery: Run `experiments/4_predict_expert.ipynb`
