#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:44:13 2020

@author: maria

Feed Forward Neural Network Architecture
using the gamestates only as input
"""

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import Adam
from keras.initializers import RandomNormal, Zeros
import matplotlib.pyplot as plt
from keras.utils.vis_utils import plot_model
from metrics import recall_m, precision_m, f1_m
from keras.callbacks import ModelCheckpoint, LambdaCallback, EarlyStopping
from keras import backend as K
import gc # garbage collector
import csv
import numpy as np

x_train = np.load('./traindata/gamestates.npy')
y_train = np.load('./traindata/labels.npy')
x_test = np.load('./testdata/gamestates.npy')
y_test = np.load('./testdata/labels.npy')

# reshape the data
# the input to every LSTM layer must be 3-dim
# reshape to (samples, timesteps,features)
x_train = x_train.reshape(3368,1,8036)
x_test = x_test.reshape(843,1,8036)

# define keras model
model = Sequential()
  

# lstm
# inpute shape = (timesteps, features)
model.add(LSTM(10,input_shape=(1,8036),activation='sigmoid',
               kernel_initializer=RandomNormal(stddev=10),
               bias_initializer=Zeros()))


# nn
model.add(Dense(10, activation='sigmoid'))

# adam optimizer configuration
opt = Adam(lr=0.0001)

# compile the model
model.compile(optimizer=opt, loss='binary_crossentropy', 
              metrics=['accuracy',recall_m,precision_m,f1_m])

# add checkpoints
filepath="./models/gamestatesLSTM/weights-improvement-{epoch:02d}-{val_acc:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

# SOS REMEMBER TO CLOSE f
# log the weights to check if they get updated during training
f = open('./models/gamestatesLSTM/weights.csv','w')
writer = csv.writer(f, delimiter='|')
print_weights = LambdaCallback(on_epoch_end=lambda batch, 
                               logs: writer.writerow(model.get_weights()))

# This callback will stop the training when there is no improvement in  
# the validation loss for 5 consecutive epochs.  
early_stop = EarlyStopping(monitor='val_loss',min_delta =0.01,
                           patience=10,mode='min')

callbacks_list = [checkpoint,print_weights,early_stop]

# train
history = model.fit(x_train,y_train, validation_data=(x_test,y_test),
                    callbacks=callbacks_list,epochs=30,batch_size=100,
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
plt.savefig('./pics/gamestatesLSTM/accuracy.png',bbox_inches='tight',dpi=300)



# summarize history for loss
plt.figure()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()
plt.savefig('./pics/gamestatesLSTM/loss.png',bbox_inches='tight',dpi=300)


# summarize history for precision
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_precision_m'])
plt.title('model accuracy')
plt.ylabel('precision')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/gamestatesLSTM/precision.png',bbox_inches='tight',dpi=300)


# summarize history for recall
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_recall_m'])
plt.title('model accuracy')
plt.ylabel('recall')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    ]
plt.savefig('./pics/gamestatesLSTM/recall.png',bbox_inches='tight',dpi=300)


# summarize history for f1
plt.figure()
plt.plot(history.history['acc'])
plt.plot(history.history['val_f1_m'])
plt.title('model accuracy')
plt.ylabel('f1 score')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
#plt.show()    
plt.savefig('./pics/gamestatesLSTM/f1score.png',bbox_inches='tight',dpi=300)

#print(model.summary())
plot_model(model, to_file='./pics/gamestatesLSTM/model_summaryplot.png',
           show_shapes=True, show_layer_names=False)

# save trained model
#model.save('multilabel_class.h5')

# release memory after done
K.clear_session()

# allso possible options to try: del model, gc.collect()
