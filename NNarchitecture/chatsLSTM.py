#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:31:03 2020

@author: maria

LSTM Neural Network Architecture
using the chats only as input
"""

from keras.models import Sequential
from keras.layers import Embedding,Dense,LSTM
from keras.optimizers import Adam
from keras.initializers import RandomNormal, Zeros
import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
from metrics import recall_m, precision_m, f1_m
from keras.callbacks import ModelCheckpoint, LambdaCallback, EarlyStopping
from keras import backend as K
import numpy as np
import pickle
import csv


# load data
#X_train,X_test,y_train,y_test,embedding_matrix, vocab_size,
#              max_doc_len): 
x_train = np.load('./traindata/chats.npy')
y_train = np.load('./traindata/labels.npy')
x_test = np.load('./testdata/chats.npy')
y_test = np.load('./testdata/labels.npy')   

# load embeddings and their params
embedding_matrix = np.load('./embedding_matrix.npy')
vocab_size, max_doc_len = pickle.load(open('embeddingparams.pkl','rb'))

        
# define keras model
model = Sequential()
# input length = longest doc length
e =  Embedding(vocab_size,100,weights=[embedding_matrix],
               input_length=max_doc_len,trainable=False, mask_zero = True)

# add embedding layer
model.add(e)
  
# lstm
# inpute shape = (timesteps, features)
model.add(LSTM(32))

# nn
model.add(Dense(10, activation='sigmoid'))


# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', 
              metrics=['accuracy',recall_m,precision_m,f1_m])

# add checkpoints
filepath="./models/chatsLSTM/weights-improvement-{epoch:02d}-{val_acc:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

# SOS REMEMBER TO CLOSE f
# log the weights to check if they get updated during training
f = open('./models/chatsLSTM/weights.csv','w')
writer = csv.writer(f, delimiter='|')
print_weights = LambdaCallback(on_epoch_end=lambda batch, 
                               logs: writer.writerow(model.get_weights()))

# This callback will stop the training when there is no improvement in  
# the validation loss for 5 consecutive epochs.  
early_stop = EarlyStopping(monitor='val_loss',min_delta =0.01,
                           patience=5, mode='min')

callbacks_list = [checkpoint,print_weights,early_stop]

# train
history = model.fit(x_train,y_train, validation_data=(x_test,y_test),
                    callbacks=callbacks_list,epochs=50,batch_size=100,
                    verbose=0)

f.close()

# plot performance-learning curves
# summarize history for accuracy
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()
plt.savefig('./pics/chatsLSTM/accuracy.png',bbox_inches='tight',dpi=300)



# summarize history for loss
plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()
plt.savefig('./pics/chatsLSTM/loss.png',bbox_inches='tight',dpi=300)


# summarize history for precision
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_precision_m'])
plt.title('model accuracy')
plt.ylabel('precision')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/chatsLSTM/precision.png',bbox_inches='tight',dpi=300)


# summarize history for recall
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_recall_m'])
plt.title('model accuracy')
plt.ylabel('recall')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    ]
plt.savefig('./pics/chatsLSTM/recall.png',bbox_inches='tight',dpi=300)


# summarize history for f1
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_f1_m'])
plt.title('model accuracy')
plt.ylabel('f1 score')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/chatsLSTM/f1score.png',bbox_inches='tight',dpi=300)

#print(model.summary())
plot_model(model, to_file='./pics/chatsLSTM/model_summaryplot.png',
           show_shapes=True, show_layer_names=False)

# save trained model
#model.save('multilabel_class.h5')

# release memory after done
K.clear_session()

# allso possible options to try: del model, gc.collect()
