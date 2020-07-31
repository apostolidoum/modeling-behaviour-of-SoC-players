## Modeling the behaviour of players in *Settlers of Catan* games 

This repository contains the code implemented during work on my diploma thesis for the Technical University of Crete, department of Electrical and Computer Engineering, titled 
**Exploiting linguistic data for modeling players’ behaviour instrategic board games**.

### Thesis Abstract

Certain games exhibit social aspects realized often via natural
language exchanges. Unfortunately few attempts have been made to
take into account both actions and linguistic information for
modeling agents. In this thesis the goal is to
leverage both types of information in order to create a model that is
capable of emulating players' actions taking into account 
actions performed by all players in the past as well as their previous linguistic
exchanges. Recent advances in neural network architectures and more
precisely recurrent models allow to sequentially update
representations of the game state or linguistic data as well as
sharing of parameters between disparate representations. Thus the aim
is to use combined representations both for the game state and for
the linguistic exchanges in order to model the actions of the players.

Data collected in the context of the ERC Advanced Grant project STAC were used for this work. 
As a first step the raw data were processed to form a Dataset suitable for use in machine learning projects.
This step entailed a novel modeling of the way in which information about a game of Settlers of Catan is represented.
Then linguistic and gameplay information from the created Dataset was exploited by neural networks to predict the players' actions.
Architectures of Feed Forward Neural Networks, Recurrent Neural Networks (such as LSTMs) as well as combined architectures of the two were investigated in the context of this thesis.

### Setting up the environment

- Create a new conda environment using 

`conda create --name <env_name> --file requirements.txt`

- Activate the environment using

`conda activate <env_name>`

### Creating a SoC dataset

- Transfer the .soclog files in `soclogsData_NoResources` 

    - If you are repeating the process with the same files used in this thesis, unzip `soclogs.zip` in `soclogsData_NoResources` 

    - If you are using new .soclog files make sure you adjust filenames and/or directory names accordingly. (code applicable for .soclog files from jSettlers v.1)

- Run `python turn.py`

- Run `python reduced_logs.py`

- Run `python collectfeatures.py`


### Preprocessing the data

- In this thesis we used the Glove Embeddings. Download them from [here](http://nlp.stanford.edu/data/glove.6B.zip) and unzip in `NNarchitecture/embeddings/`

- Run `python GamestatesOHE.py`

- Run `python datapreprocessing.py`

### Train the networks


You can now run any of the modules `gamestatesFF.py`, `gamestatesLSTM.py`, `chatsLSTM.py`, `combinedFFLSTM.py`, `combinedLSTMLSTM.py` to train the models.


*NOTE THAT :* This project requires a lot of disk space to run since the networks are deep and the training spans over many epochs. Make sure that you have enough space and that your system does not overheat during the training process. Try testing the training for a small number of epochs or smaller networks before getting deeper to make sure that you do not damage your system.

Other than that feel free to tweak any parameters or even try the network configurations tested in this thesis and see what results you get!

*DISCLAIMER :* The precision, recall and F1 score have been removed from Keras since version 2.0, because those metrics are global metrics whereas Keras works in batches.
As a result they might be more misleading than helpful. It is advised both by the Keras community and the author that they be interpreted with caution. The F1 score is printed when running the training of the models but has not been included in the dissertation due to its unreliability.



Enjoy!























