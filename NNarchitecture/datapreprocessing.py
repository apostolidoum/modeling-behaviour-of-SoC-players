#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preprocessing of the chat, gamestate and labels data

@author: maria
"""
import pandas as pd
import os
import numpy as np
from numpy import asarray
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pickle

# Disambiguation:
# game = pkl file name e.g. pilot01_chats.pkl
# gamename = pilot01

# list of all the chat dataframes
# hold tuple (game,df)
chat_dfs = list()

# list of all the chat dataframes with concatenated chat of each gameturn
# holds tuples (game,df)
concatchat_dfs = list()

# holds tuples (game, df)
labels_dfs = list()

# hold tuples (gamename,duration in turns)
gamefileinfo = list()

# load all the chats data tables
for pkl_file in os.listdir('../soclogsData_NoResources/DataTables/pilot'):
    if "_chats.pkl" in pkl_file:
        #print(pkl_file)
        chats = pd.read_pickle("../soclogsData_NoResources/DataTables/pilot/"+pkl_file)
        #to check for consistency, turns must be the same 
        #chat_turns = chats.iloc[-1]['Turn']
        #gameinfo.append((pkl_file,chat_turns))
        chat_dfs.append(("pilot/"+pkl_file,chats))
    if "_labels.pkl" in pkl_file:
        labels = pd.read_pickle("../soclogsData_NoResources/DataTables/pilot/"+pkl_file)
        label_turns = labels.iloc[-1]['Turn']
        gamefileinfo.append(("pilot/"+pkl_file,label_turns))
        labels_dfs.append(("pilot/"+pkl_file,labels))
        
for pkl_file in os.listdir('../soclogsData_NoResources/DataTables/season1'):
    if "_chats.pkl" in pkl_file:
        #print(pkl_file)
        chats = pd.read_pickle("../soclogsData_NoResources/DataTables/season1/"+pkl_file)
        #to check for consistency, turns must be the same 
        #chat_turns = chats.iloc[-1]['Turn']
        #gameinfo.append((pkl_file,chat_turns))
        chat_dfs.append(("season1/"+pkl_file,chats))
    if "_labels.pkl" in pkl_file:
        labels = pd.read_pickle("../soclogsData_NoResources/DataTables/season1/"+pkl_file)
        label_turns = labels.iloc[-1]['Turn']
        gamefileinfo.append(("season1/"+pkl_file,label_turns))
        labels_dfs.append(("season1/"+pkl_file,labels))
        

for pkl_file in os.listdir('../soclogsData_NoResources/DataTables/season2'):
    if "_chats.pkl" in pkl_file:
        #print(pkl_file)
        chats = pd.read_pickle("../soclogsData_NoResources/DataTables/season2/"+pkl_file)
        #to check for consistency, turns must be the same 
        #chat_turns = chats.iloc[-1]['Turn']
        #gameinfo.append((pkl_file,chat_turns))
        chat_dfs.append(("season2/"+pkl_file,chats))
    if "_labels.pkl" in pkl_file:
        labels = pd.read_pickle("../soclogsData_NoResources/DataTables/season2/"+pkl_file)
        label_turns = labels.iloc[-1]['Turn']
        gamefileinfo.append(("season2/"+pkl_file,label_turns))
        labels_dfs.append(("season2/"+pkl_file,labels))


# keep only the name of the game (discard _labels.pkl)
# save that to gameinfo dictionary
gameinfo = list()

for (game,turns) in gamefileinfo:
    gamename = game.split('_labels.pkl')[0]
    gameinfo.append((gamename,turns)) 
    
# convert gameinfo list to dictionary
gameinfo_dic = dict(gameinfo)

# concatenate texts   
concatchat_df = pd.DataFrame(columns=['Turn','text'])   
for (game,df) in chat_dfs:
    concatchat_df = df.groupby(['Turn'])['text'].apply(','.join).reset_index()
    concatchat_dfs.append((game,concatchat_df))
     
     
paddedchats_dfs = list() 
      
## add empty chat boxes for gameturns where noone spoke
for (game,df) in concatchat_dfs:
    #find game duration from game info :-)
    gamename = game.split('_chats.pkl')[0]
    gameturns = gameinfo_dic[gamename]
    #print(game,gameturns)
    for turn in range(gameturns+1):
        # check that there exist chat for this turn
        if df.loc[df['Turn']==turn].empty:
           # print('missing')
           # append the missing data at the end of the dataframe
           missingchat =  pd.DataFrame(data={'Turn':[turn],'text':['']})
           df = df.append(missingchat,ignore_index=True)
        else:
            # print('exists')
            pass
    # sort according to turn
    df = df.sort_values(by=['Turn'])
    paddedchats_dfs.append((gamename,df)) 
    
# now that everything is the same size, create a DF of pure data for the nn
#   
# combine labels and chats to one large dataframe each
# make sure you copy data in the same order, i.e. append labelsDF and 
# chatsDF in parallel, in the same loop
    
# copy the dataframe structure, i.e. columns
labelsDF = pd.DataFrame(columns=labels_dfs[0][1].columns)  
chatsDF = pd.DataFrame(columns = ['Turn','text'])    
# gamestates are saved directly to np array because they have 
# already been converted 
# initialize size
totalgameturns = sum(x[1]+1 for x in gameinfo)
#print(totalgameturns)
gamestates = np.empty((totalgameturns,8036)) 
# tuples to dic
# these dictionaries have as key the gamename (make so for labels as well)
labels_dfs_dic = dict([ (game.split('_labels.pkl')[0],df) for (game,df) in labels_dfs ])
chats_dfs_dic =  dict([(gamename,df) for (gamename,df) in paddedchats_dfs])
for game in gameinfo:
    # game is a tuple (gamename,no.turns)
    # gamename is the first element in the tuple 
    gamename = game[0]
    turns = game[1]
    #print(gamename)
    # copy data from labels
    labelsDF = labelsDF.append(labels_dfs_dic[gamename],sort=False,ignore_index=True)
    # copy data from padded chats
    chatsDF = chatsDF.append(chats_dfs_dic[gamename],sort=False,ignore_index=True)
    # here make a DF of gamestates
    layout = np.load('./OHEdata/'+gamename+'/layout.npy')
    robber = np.load('./OHEdata/'+gamename+'/robber.npy')
    pl0builds = np.load('./OHEdata/'+gamename+'/pl0builds.npy')
    pl0devcards = np.load('./OHEdata/'+gamename+'/pl0devcards.npy')
    pl1builds = np.load('./OHEdata/'+gamename+'/pl1builds.npy')
    pl1devcards = np.load('./OHEdata/'+gamename+'/pl1devcards.npy')
    pl2builds = np.load('./OHEdata/'+gamename+'/pl2builds.npy')
    pl2devcards = np.load('./OHEdata/'+gamename+'/pl2devcards.npy')
    pl3builds = np.load('./OHEdata/'+gamename+'/pl3builds.npy')
    pl3devcards = np.load('./OHEdata/'+gamename+'/pl3devcards.npy')
    
    # check that no.turns is same as npy array turns, i.e. rows
    # carefull with turns and shape +-1
    assert turns == robber.shape[0]-1
    # repeat the layout for every gameturn
    l = np.tile(layout,(turns+1,1))
    
    gamedata = np.hstack((l,robber,
                          pl0builds,pl0devcards,
                          pl1builds,pl1devcards,
                          pl2builds,pl2devcards,
                          pl3builds,pl3devcards))
    np.append(gamestates,gamedata,axis=0)
       
        
# drop the  turn column
# convert from dataframe to np array
# X needs to be a list of str -> use vstack
text = chatsDF.drop(columns=['Turn'])
X = text.values.tolist()
X = [x[0] for x in X ]
        
# convert True False label to 0 and 1
# convert from dataframe to np array
Y = labelsDF.drop(columns=['Turn'])
Y = Y.astype(float)
Y = Y.to_numpy()        


# convert text to sequences of number
# prepare tokenizer
# the tokenizer of keras by default lower cases the text
t = Tokenizer()
t.fit_on_texts(X)
vocab_size = len(t.word_index) + 1
# print(vocab_size)

# word index must contain all the words seen in the corpus
#print('word index ',t.word_index)

# integer encode the text 
# go from sequences of text to sequences of integers
encoded_docs = t.texts_to_sequences(X)
        
# pad to max length of sequence in docs
# find max length sentence
# NOTE check inputs after tokenizer
#      otherwise the len is the no. of characters, not words
max_doc_len = 0
for seq in encoded_docs:
    if len(seq) > max_doc_len :
        max_doc_len = len(seq)
print('longest doc len : ',max_doc_len)

# padding sequences
padded_docs = pad_sequences(encoded_docs, maxlen=max_doc_len, padding='post')
#print(padded_docs)

#
# load the embedding into memory, in a dictionary 
# load the whole embedding into memory
embeddings_index = dict()
with open('embeddings/glove.6B/glove.6B.100d.txt') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

print('Loaded %s word vectors.' % len(embeddings_index))



# create a weight matrix for words in training docs
embedding_matrix = np.zeros((vocab_size, 100))
# t.word_index is basicly a dictionary of our vocabulary
#   word:index
# then at position index of the embedding matrix we store the 
# embedding vector of the word with index index
for word, i in t.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
        
# Save the Data, Labels and the Embedding matrix
        
# split to train and test sets
# join data arrays
# so that there is the same correspondence to labels
data = np.hstack((gamestates,padded_docs))
x_train,x_test,y_train,y_test = train_test_split(data,Y,test_size = 0.2)

# disjoin the data arrays
gamestates_train = x_train[:,0:8036]
gamestates_test = x_test[:,0:8036]
chats_train = x_train[:,8036:]
chats_test = x_test[:,8036:]        
        
np.save('./traindata/gamestates',gamestates_train)
np.save('./testdata/gamestates',gamestates_test)
np.save('./traindata/chats',chats_train)
np.save('./testdata/chats',chats_test)
np.save('./traindata/labels.npy',y_train)
np.save('./testdata/labels',y_test)

np.save('embedding_matrix.npy',embedding_matrix)

# Also needed for the embedding layer
# vocab size and input length
with open('embeddingparams.pkl','wb') as f:
    pickle.dump([vocab_size, max_doc_len],f)

        
