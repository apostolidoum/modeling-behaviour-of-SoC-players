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

