#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 16:33:29 2020

@author: maria

Feed Forward - LSTM Neural Network Architecture
using both gamestates and chats as inputs
"""

from keras.models import Model
from keras.layers import Dense, LSTM, Input, Embedding
from keras.layers import concatenate
from keras.initializers import RandomNormal, Zeros
import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
from metrics import recall_m, precision_m, f1_m
from keras.callbacks import ModelCheckpoint, LambdaCallback, EarlyStopping
from keras import backend as K
import gc # garbage collector
import csv
import numpy as np
import pickle
from pathlib import Path

# load the data
gamestates_train = np.load('./traindata/gamestates.npy')
chats_train = np.load('./traindata/chats.npy')
y_train = np.load('./traindata/labels.npy')
gamestates_test = np.load('./testdata/gamestates.npy')
chats_test = np.load('./testdata/chats.npy') 
y_test = np.load('./testdata/labels.npy') 

# load embeddings and their params
embedding_matrix = np.load('./embedding_matrix.npy')
vocab_size, max_doc_len = pickle.load(open('embeddingparams.pkl','rb'))

# make directories to save the results
models_dir = Path.cwd() / "models/combinedFFLSTM" 
models_dir.mkdir(parents=True, exist_ok=True)

pics_dir = Path.cwd() / "pics/combinedFFLSTM" 
pics_dir.mkdir(parents=True, exist_ok=True)


# design the model
# with multiple inputs

inputGamestates = Input(shape=(8036,))
inputChats = Input(shape=(max_doc_len,))

# gamestates branch
x = Dense(8036,activation='sigmoid',
          kernel_initializer = RandomNormal(stddev=10),
          bias_initializer=Zeros())(inputGamestates)
x = Dense(1000,activation='sigmoid',
          kernel_initializer = RandomNormal(stddev=10),
          bias_initializer=Zeros())(x)
x = Dense(10,activation='sigmoid',
          kernel_initializer = RandomNormal(stddev=10),
          bias_initializer=Zeros())(x)
x = Model(inputs=inputGamestates, outputs=x)

# chats branch
y = Embedding(vocab_size,100,weights=[embedding_matrix],
               input_length=max_doc_len,trainable=False, mask_zero = True)(inputChats)
y = LSTM(32)(y)
y = Model(inputs=inputChats, outputs=y)

# combine the inputs
combined = concatenate([x.output,y.output])

# ff prediction layer
z = Dense(10,activation='sigmoid')(combined)

# complete model
model = Model(inputs=[x.input, y.input], outputs=z)

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', 
              metrics=['accuracy',recall_m,precision_m,f1_m])

# add checkpoints
filepath="./models/combinedFFLSTM/weights-improvement-{epoch:02d}-{val_accuracy:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')

# SOS REMEMBER TO CLOSE f
# log the weights to check if they get updated during training
f = open('./models/combinedFFLSTM/weights.csv','w')
writer = csv.writer(f, delimiter='|')
print_weights = LambdaCallback(on_epoch_end=lambda batch, 
                               logs: writer.writerow(model.get_weights()))

# This callback will stop the training when there is no improvement in  
# the validation loss for 5 consecutive epochs.  
early_stop = EarlyStopping(monitor='val_loss', min_delta =0.01,
                           patience=10, mode='min')

callbacks_list = [checkpoint,print_weights,early_stop]

# train
history = model.fit([gamestates_train,chats_train],y_train, 
                    validation_data=([gamestates_test,chats_test],y_test),
                    callbacks=callbacks_list,epochs=50,batch_size=10,
                    verbose=0)

f.close()

# plot performance-learning curves
# summarize history for accuracy
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()
plt.savefig('./pics/combinedFFLSTM/accuracy.png',bbox_inches='tight',dpi=300)



# summarize history for loss
plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()
plt.savefig('./pics/combinedFFLSTM/loss.png',bbox_inches='tight',dpi=300)


# summarize history for precision
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_precision_m'])
plt.title('model accuracy')
plt.ylabel('precision')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/combinedFFLSTM/precision.png',bbox_inches='tight',dpi=300)


# summarize history for recall
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_recall_m'])
plt.title('model accuracy')
plt.ylabel('recall')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    ]
plt.savefig('./pics/combinedFFLSTM/recall.png',bbox_inches='tight',dpi=300)


# summarize history for f1
plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_f1_m'])
plt.title('model accuracy')
plt.ylabel('f1 score')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/combinedFFLSTM/f1score.png',bbox_inches='tight',dpi=300)

#print(model.summary())
plot_model(model, to_file='./pics/combinedFFLSTM/model_summaryplot.png',
           show_shapes=True, show_layer_names=False)
