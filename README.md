# Integrating Semantics into Domain Translation without Supervision

Official code repository for the paper Integrating Semantics into Domain Translation without Supervision.

Dependencies are provided in `requirement.txt`. A Dockerfile is provided for reproducing the same environment
used to run the experiments.

## Organization

The models are in `src/models`. Every model has 3 files:

`__init__.py`: Defines the specific parameters of the models

`model.py` Defines the architecture of the model

`train.py` Defines the training algorithm of the model

In general, a model can be run by invoking `main.py`, which also contain the general parameters shared among all the
models. The syntax for running a model is as follows:
```
python src/main.py [GENERAL PARAMETERS] [MODEL] [SPECIFIC MODEL PARAMETERS]
```

## Datasets

We presented results on the MNIST-SVHN dataset which can be themselves downloaded by the torchvision library. We also
presented results on the Sketch->Real dataset which are a subset of the DomainNet dataset
(https://arxiv.org/abs/1812.01754).
The sketch dataset can be downloaded as follow:
```bash
./fetch_data.sh sketch
```
Similarly, the real dataset can be downloaded as follows:
```bash
./fetch_data.sh real
```

## Models
This repository is composed of 5 models which are useful for reproducing the results from the paper.
### classifier
This model is used for evaluating the translation MNIST<->SVHN. The classifier is a wide residual network
(https://arxiv.org/abs/1605.07146) and the is  code inspired from inspired from:
https://github.com/szagoruyko/wide-residual-networks.

**Classifying MNIST**
```bash
python src/main.py --exp-name classifier --cuda --run-id mnist --train-batch-size 128 --valid-split 0.2 classifier --dataset mnist
```
**Classifying SVHN**
```bash
python src/main.py --exp-name classifier --cuda --run-id svhn --train-batch-size 128 --valid-split 0.2 classifier --dataset svhn_extra
```
### imsat
Imsat (https://arxiv.org/abs/1605.07146) is a method for clustering using deep neural networks. In this work, we use it
 for clustering MNIST. We use a slighly different version than the one proposed in the original model. We explain the
 the differences in the appendix on the paper. But, the original imsat algorithm, or any other cluster algorithm which
 can cluster MNIST decently well could be used in place.
 
**Clustering MNIST**
```bash
python src/main.py --exp-name cluster --cuda --run-id mnist imsat
```
 
### vmt_cluster
VMT (https://arxiv.org/abs/1905.04215) is an unsupervised domain adaptation method. In this work, we proposed to replace
the ground truth labels of the source domain with the learned cluster on the source domain. `vmt_cluster` is a model
that applies the vmt method on images by considering the learned cluster rather than the ground truth labels.

**Domain adaptation with clustering MNIST-SVHN**
```bash
python src/main.py --exp-name vmt-cluster --cuda --run-id mnist-svhn vmt_cluster --dataset1 mnist --dataset2 svhn --cluster-model-path ./experiments/vrinv/cluster_mnist-None --cluster-model vrinv --dw 0.01 --svw 1 --tvw 0.06 --tcw 0.06 --smw 1 --tmw 0.06
```
### vmtc_repr
We also propose to apply VMT cluster on the representation learned by a representation learning model using the clusters
learned themselves on the representation. In this work, we used the pre-trained MoCO-v2
(https://arxiv.org/abs/2003.04297) model, which can be downloaded as follow
```bash
wget https://dl.fbaipublicfiles.com/moco/moco_checkpoints/moco_v2_800ep/moco_v2_800ep_pretrain.pth.tar
```
We found that using this method for learning cross-domain clustering on sketch-real yielded better results. Learning the
model can be done as follows:

**Domain adaptation with clustering on Sketch-Real**
```bash
python src/main.py --exp-name vmtc-rept --cuda --run-id sketch-real vmtc_repr --dataset-loc1 data/real --dataset-loc2 data/sketch --ss-path moco_v2_800ep_pretrain.pth.tar
```

### i2i
Finally, we propose a image-to-image translation model which can incorporate the learned semantics. This model is inspired
from StarGAN-v2 (https://github.com/clovaai/stargan-v2).

**Domain translation MNIST-SVHN**
```bash

```

**Domain translation Sketch->Real**
```bash

```

## Visualizing the results
We use tensorboard for saving the artefacts. It is possible to view the results by simply invoking tensorboard in the folder where the results were saved
```
tensorboard --logdir .
```
