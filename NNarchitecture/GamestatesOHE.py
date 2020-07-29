#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transform the gamestate data to onehot vectors
"""

from sklearn.preprocessing import OneHotEncoder,LabelEncoder
import pandas as pd 
import numpy as np
import re
import os
from pathlib import Path


# settlements and cities are built on node coordinates
# roads are built on edge coordinates
# nodes are named after an adjacent rode
# hence the set of node coords is a subset of the edge coords
# Additionally, no nodes close to the sea are needed...
# these are inaccessible for building

# edge_coordinates contains the edge coordinates on which a player
# could actually built
# len(edge_coordinates) = 72 
edge_coordinates = ['0x27','0x38','0x49','0x5a','0x6b','0x7c',
                    '0x26','0x48','0x6a','0x8c',
                    '0x25','0x36','0x47','0x58','0x69','0x7a','0x8b','0x9c',
                    '0x24','0x46','0x68','0x8a','0xac',
                    '0x23','0x34','0x45','0x56','0x67','0x78','0x89','0x9a','0xab','0xbc',
                    '0x22','0x44','0x66','0x88','0xaa','0xcc',
                    '0x32','0x43','0x54','0x65','0x76','0x87','0x98','0xa9','0xba','0xcb',
                    '0x42','0x64','0x86','0xa8','0xca',
                    '0x52','0x63','0x74','0x85','0x96','0xa7','0xb8', '0xc9',
                    '0x62','0x84','0xa6','0xc8',
                    '0x72','0x83','0x94','0xa5','0xb6','0xc7']

# additional node coordinates
# (that are not in the accessible edge_coordinates list)
# the ones on the right side of the land that are named after
# sea edge nodes
node_coordinates = ['0x8d', '0xad','0xcd','0xdc','0xda','0xd8']

# all the coordinates of the table that a player can build on
# plus the none value for when the player has not built 
# len(build_coords) = 79
build_coords = edge_coordinates + node_coordinates + ['None']

################################
# encoding the build coordinates
################################


np_build_coords = np.array(build_coords)
label_encoder = LabelEncoder()
integer_encoded_build_coords = label_encoder.fit_transform(np_build_coords)
#print(label_encoder.transform(np.array(['0x69'])))
######################
# for debugging use:
######################
#print('building coordinates label encoding')
#for x in build_coords:
#    print('coordinate ' + str(x) + ' : '+str(label_encoder.transform(np.ravel(x))))
#print('-----------------------------------')
#building coordinates label encoding
#coordinate 0x27 : [5]
#coordinate 0x38 : [9]
#coordinate 0x49 : [17]
#coordinate 0x5a : [22]
#coordinate 0x6b : [32]
#coordinate 0x7c : [38]
#coordinate 0x26 : [4]
#coordinate 0x48 : [16]
#coordinate 0x6a : [31]
#coordinate 0x8c : [48]
#coordinate 0x25 : [3]
#coordinate 0x36 : [8]
#coordinate 0x47 : [15]
#coordinate 0x58 : [21]
#coordinate 0x69 : [30]
#coordinate 0x7a : [37]
#coordinate 0x8b : [47]
#coordinate 0x9c : [54]
#coordinate 0x24 : [2]
#coordinate 0x46 : [14]
#coordinate 0x68 : [29]
#coordinate 0x8a : [46]
#coordinate 0xac : [62]
#coordinate 0x23 : [1]
#coordinate 0x34 : [7]
#coordinate 0x45 : [13]
#coordinate 0x56 : [20]
#coordinate 0x67 : [28]
#coordinate 0x78 : [36]
#coordinate 0x89 : [45]
#coordinate 0x9a : [53]
#coordinate 0xab : [61]
#coordinate 0xbc : [67]
#coordinate 0x22 : [0]
#coordinate 0x44 : [12]
#coordinate 0x66 : [27]
#coordinate 0x88 : [44]
#coordinate 0xaa : [60]
#coordinate 0xcc : [73]
#coordinate 0x32 : [6]
#coordinate 0x43 : [11]
#coordinate 0x54 : [19]
#coordinate 0x65 : [26]
#coordinate 0x76 : [35]
#coordinate 0x87 : [43]
#coordinate 0x98 : [52]
#coordinate 0xa9 : [59]
#coordinate 0xba : [66]
#coordinate 0xcb : [72]
#coordinate 0x42 : [10]
#coordinate 0x64 : [25]
#coordinate 0x86 : [42]
#coordinate 0xa8 : [58]
#coordinate 0xca : [71]
#coordinate 0x52 : [18]
#coordinate 0x63 : [24]
#coordinate 0x74 : [34]
#coordinate 0x85 : [41]
#coordinate 0x96 : [51]
#coordinate 0xa7 : [57]
#coordinate 0xb8 : [65]
#coordinate 0xc9 : [70]
#coordinate 0x62 : [23]
#coordinate 0x84 : [40]
#coordinate 0xa6 : [56]
#coordinate 0xc8 : [69]
#coordinate 0x72 : [33]
#coordinate 0x83 : [39]
#coordinate 0x94 : [50]
#coordinate 0xa5 : [55]
#coordinate 0xb6 : [64]
#coordinate 0xc7 : [68]
#coordinate 0x8d : [49]
#coordinate 0xad : [63]
#coordinate 0xcd : [74]
#coordinate 0xdc : [77]
#coordinate 0xda : [76]
#coordinate 0xd8 : [75]
#coordinate None : [78]

# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded_build_coords = integer_encoded_build_coords.reshape(len(integer_encoded_build_coords), 1)
onehot_encoded_build_coords = onehot_encoder.fit_transform(integer_encoded_build_coords)
#print(onehot_encoded_build_coords)

##############################################
# Testing
##############################################
# test label transform  ['0x69' '0x89' 'None']
#print('Testing the build coordinates')
#y = gamestates.iloc[2,6:9]
#values = np.array(y)
#print(values)
#integer_encoded = label_encoder.transform(np.ravel(values))
#print(integer_encoded)
#integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
#onehot_encoded = onehot_encoder.transform(integer_encoded)
#print(onehot_encoded)
#print('eotesting build coordinates')

# robber can be placed on land hexes (19)
land_coords = ['0x37','0x59','0x7b',
               '0x35','0x57','0x79','0x9b',
               '0x33','0x55','0x77','0x99','0xbb',
               '0x53','0x75','0x97','0xb9',
               '0x73','0x95','0xb7'
               ]
################################
# encoding the land coordinates
# aka robber coordinates
################################
np_rob_coords = np.array(land_coords)
rob_label_encoder = LabelEncoder()
integer_encoded_rob_coords = rob_label_encoder.fit_transform(np_rob_coords)
# print(integer_encoded_rob_coords)
# [ 2  6 11  1  5 10 15  0  4  9 14 18  3  8 13 17  7 12 16]
# binary encode
rob_onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded_rob_coords = integer_encoded_rob_coords.reshape(len(integer_encoded_rob_coords), 1)
onehot_encoded_rob_coords = rob_onehot_encoder.fit_transform(integer_encoded_rob_coords)
#print(onehot_encoded_rob_coords)

##############################################
# Testing
##############################################
## test robber coordinates of pilot01
#print('Testing the robber ')
#y = gamestates.iloc[:,3]
#values = np.array(y)
#print(values)
#integer_encoded = rob_label_encoder.transform(np.ravel(values))
#print(integer_encoded)
#integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
#onehot_encoded = rob_onehot_encoder.transform(integer_encoded)
#print(onehot_encoded)
#print('eotesting robber')


################################
# encoding the hex typed
################################
# this needs to have custom categories because of the ports
# in the game version of the data
# 6: water
# 0: desert
# 1: clay
# 2: ore
# 3: sheep
# 4: wheat
# 5: wood
# 7 - 12 : miscelaneous ports(3:1) facing on the different directions
# 16+ : non miscelaneous ports(2:1)
#
# 9 categories 

def hexLabelEncoder(hextypes):
    '''
    converts the hextypes to labeled (9 labels for the 9 categories)
    Parameters: hex board layout array
    Returns: array that contains the labels 
    '''
    y = []
    # pilot1 hexlayout is 
    #[9, 6, 67, 6, 6, 2, 5, 1, 66, 8, 2, 3, 1, 2, 6, 6, 5, 3, 4, 1, 4, 11, 36, 5, 4, 0, 5, 6, 6, 4, 3, 3, 97, 21, 6, 12, 6]
    for x in hextypes:
        if x < 7 : 
            y.append(x)
        elif 7<= x <= 12:
            y.append(7)
        else :
            y.append(8)
    
    return y

###### checking the general fit
###### generalized ohe encoder for list of all possible land types
hex_type_OHencoder = OneHotEncoder(sparse=False)
hex_type_labels = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
#integer_encoded_types = integer_encoded_types.reshape(len(integer_encoded_types),1)
OHE_land_types = hex_type_OHencoder.fit_transform(hex_type_labels.reshape(len(hex_type_labels),1))
#print(OHE_land_types)

################################################
# Testing
##############################################
## test land types of pilot01
#hextypes = gamestates.iloc[0,1]
#integer_encoded_types = np.array(hexLabelEncoder(hextypes))
#print(integer_encoded_types)
# outputs:
# pilot1 hexlayout is 
#[9, 6, 67, 6, 6, 2, 5, 1, 66, 8, 2, 3, 1, 2, 6, 6, 5, 3, 4, 1, 4, 11, 36, 5, 4, 0, 5, 6, 6, 4, 3, 3, 97, 21, 6, 12, 6]
# converted to:
# [7 6 8 6 6 2 5 1 8 7 2 3 1 2 6 6 5 3 4 1 4 7 8 5 4 0 5 6 6 4 3 3 8 8 6 7 6]


#ohe_hex_layout = hex_type_OHencoder.transform(integer_encoded_types.reshape(len(integer_encoded_types),1))





######################################################
# create the numpy array that contains the ohe vectors
######################################################
#
# store the data to an np array so that the can be used
# in keras 
#
# a massive np array will be created with all the games at the end, when we 
# will be ready to train

# to convert to ohe you first transform to label encoded
# and then to one-hot encode

# np array size :
#       rows : 4150 
#               i.e. for all 57 games we have 4150 gameturns
#       columns : 
#           hex layout : 37 hexes x 9 categories 
#                        -> 333
#           robber positions : 19 possible positions (land hexes)
#                               -> 19
#           player state : 
#                           builds : 24 building blocks x 79 categories(coords)
#                                    -> 1896
#                           dev cards : 25 dev cards (true-false)
#                                       -> 25
##
#           total : 333 + 19 + 4x(1896+25) = 8017 + 19 = 8036  


######### IMPORTAND ##########
## Instead of a big, chaotic table, save to various small np arrays 
##
#ohedata = np.zeros((4150,8036)) 
## saving pilot1 to np data array
## land hex types 
#temp = np.array(hexLabelEncoder(gamestates.iloc[0,1]))
#print('-------')
#print(temp)
#print(hex_type_OHencoder.transform(temp.reshape(len(temp),1)))
#
##oned_temp = np.ravel(hex_type_OHencoder.transform(temp.reshape(len(temp),1)))
## this goes from 0 to 332
#ohedata[0,0:333] = np.ravel(hex_type_OHencoder.transform(temp.reshape(len(temp),1)))
#ohedata[0,0:3]=1 # -> writes 1 to columns 0,1,2
######## IMPORTAND ##########

# OHE conversion steps: 
#        1. convert hex layout
#        2. convert robber position and append it
#        3. convert player1 build and append them
#        4. convert player1 devcard and append them
#        5. convert player2 3 4 
#        6. check size of all this

def convert_hex_layout(hexlayout):
    ''' converts the gamestates hexlayout to one hot encoding
    
    PARAMETERS
    ----------
    hexlayout : the gamestates hexlayout
    
    Returns
    -------
    an np array of size (1,333)
    '''
    
    # convert the layout to label encoding
    labeled = np.array(hexLabelEncoder(hexlayout))
    # convert the layout to one hot encoding
    ohe = hex_type_OHencoder.transform(labeled.reshape(len(labeled),1))
    return np.ravel(ohe)
    
####Testing OK
#print('Testing hex layout conversion')
#methodlayout = convert_hex_layout(gamestates.iloc[0,1])
#scriptlayout = np.ravel(hex_type_OHencoder.transform(temp.reshape(len(temp),1)))
 
def convert_robber_position(robber):
    ''' converts the robber position coordinates to one hot encoding
    
    Parameters
    ----------
    robber: the robber coordinates from the gamestates dataframe
    
    Returns
    -------
    encoded np array of size 19
    '''
    
    # convert the robber position to labeled encoding
    robber = np.array(robber)
    labeled = rob_label_encoder.transform(np.ravel(robber))
    # convert the robber position to one hot encoding
    labeled = labeled.reshape(len(labeled),1)
    ohe = rob_onehot_encoder.transform(labeled)
    # return with ravel to avoid the double list [[]]
    return np.ravel(ohe)

####Testing OK
#print('Testing the robber ')
#y = gamestates.iloc[1,3]
#values = np.array(y)
#print(values)
#integer_encoded = rob_label_encoder.transform(np.ravel(values))
#print(integer_encoded)
#integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
#onehot_encoded = rob_onehot_encoder.transform(integer_encoded)
#print(onehot_encoded)
#print('eotesting robber')
#print('Testing the robber method')
#methodrobber =  convert_robber_position(gamestates.iloc[1,3])
#print(methodrobber)

def convert_player_buildings(playerbuildings):
    '''
    Converts the player buildings coordinates to one hot encoding
    
    Parameters
    ----------
    from the gamestate the players columns of settlements, cities and roads
     a list of 24 coordinates
    
    Returns
    -------
    np array of one hot encoding for all 24 building blocks of the player
     size should be (24,79) (in one line vector 24*79 = 1896)
    
    '''
    
    # list of the buildings 
    buildings = []
    for coord in playerbuildings:
        ohe_coord = convert_building_coord(coord)
        buildings.append(ohe_coord)
        
    #print(buildings)
    npbuildings = np.array(buildings)
    return np.ravel(npbuildings)
        
    
    

def convert_building_coord(hexcoord):
    '''
    Convert a hex building coordinate to one hot encoding
    
    Parameters
    ----------
    a hex coordinate
    
    Returns
    -------
    one hot encoding of the coordinate, an np array or size 79
    '''
    
    value = np.array(hexcoord)
    # convert the coordinate to labeled encoding
    labeled = label_encoder.transform(np.ravel(value))
    # convert the coordinate to one hot encoding
    labeled = labeled.reshape(len(labeled), 1)
    ohe = onehot_encoder.transform(labeled)
    return ohe


#######
## Testing the coordinate convertion OK
#print('Testing the coordinate convertion to ohe')
## testing only one coordinate
#coord = gamestates.iloc[2,6]
#print(coord)
#methodcoord = convert_building_coord(coord)
## testing group of coordinates OK
#coords = gamestates.iloc[2,6:9]
#print(coords)
#methodcoords = convert_player_buildings(coords)
#print(methodcoords)
#print(methodcoords.reshape(3,79))


def convert_player_devcards(dev_cards):
    '''
    Coverts the gamestate fields of the players dev cards
    from true/false to binary 1/0 
    
    Parameters
    ----------
    dev_cards : the 25 dev cards potentialy available to the player
    
    Returns
    -------
    np array of size 25 where true is 1 and false is 0
    '''
    
    
    binary_dev_cards =[]
    for card in dev_cards:
        # type is np.bool, don't use quotes 
        if card == True :
            binary_dev_cards.append(1)
        else:
            binary_dev_cards.append(0)
    return np.array(binary_dev_cards)
    
#### Testing player dev cards OK
#dev_cards = gamestates.loc[58, 'pl0knight1' : 'pl0vp5']
#dclist = convert_player_devcards(dev_cards)
#print(dclist)
    


##############################################################################
# OHE conversion
##############################################################################
    
# convert each dataframe to np arrays 
# each game has 10 np arrays of the board, robber and player states in ohe data
    
datafiles = ["../soclogsData_NoResources/DataTables/pilot/pilot03_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot15_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot17_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot04_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot21_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot02_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot08_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot09_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot14_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot11_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot05_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot16_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot01_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot20_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot13_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot10_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot12_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot07_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/pilot/pilot06_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/league4_attempt2-2012-11-14-19-46-22-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/practice-2012-10-30-18-41-07-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League4-2012-11-24-09-17-47-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Test-2012-10-16-14-53-15-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/L5 Real game-2012-11-11-19-58-55-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Master League final-2012-12-05-16-59-57-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League 8 Game 2-2012-11-26-18-55-31-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/SOCL League 5 Game 2-2012-11-25-17-25-09-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/league 5 last game-2012-12-09-21-08-39-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/SOCL League 5 Game 4-2012-12-03-02-11-10-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League8-2012-11-24-12-04-51-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League3Game5-2012-11-30-19-59-18-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/master league 4-2012-12-04-17-37-56-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Master league game 2-2012-11-13-18-07-14-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Game 3-2012-11-25-20-09-16-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League 5 game 3-2012-11-26-00-51-20-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League4-2012-11-09-19-08-53-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/3version2-2012-11-21-20-23-31-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League3Game1-2012-11-18-20-34-38-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/League3Game4-2012-11-28-20-01-30-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/L5 practicegame-2012-11-11-19-26-36-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Master League Game 3-2012-11-17-17-01-18-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season2/Settles league 1-2012-11-08-18-05-34-+0000_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league3practice-2012-05-31-19-23-46-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League2.4-2012-06-26-22-47-04-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league3-2012-05-27-19-53-48-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league2.2-2012-06-18-20-50-12-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league3 michael-2012-06-17-20-54-03-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/3-2012-06-06-19-58-56-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 1-2012-06-17-19-53-24-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 1.2-2012-06-21-20-27-05-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league 3 (-k)-2012-06-25-18-22-53-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league3minus1-2012-05-25-22-22-21-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 2-2012-06-26-20-23-20-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 1 game-2012-06-19-18-49-00-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 1.1-2012-06-21-18-58-22-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/league1 31may-2012-05-31-19-59-37-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League 3 Finale-2012-06-25-21-57-53-+0100_gamestates.pkl",
            "../soclogsData_NoResources/DataTables/season1/League2-2012-06-17-19-58-07-+0100_gamestates.pkl"
            ]

# make directories to save the results
ohedata_dir = Path.cwd() / "OHEdata/season2" 
ohedata_dir.mkdir(parents=True, exist_ok=True)

ohedata_dir = Path.cwd() / "OHEdata/season1" 
ohedata_dir.mkdir(parents=True, exist_ok=True)

ohedata_dir = Path.cwd() / "OHEdata/pilot" 
ohedata_dir.mkdir(parents=True, exist_ok=True)      

print('Converting gamestates data to ohe-hot encoded vectors')
print('This might take a while. Please be patient...')
for file in datafiles:
    # create a dir with the game name
    # to save the 11 np arrays of the game
    # with the data in ohe
    
    filename_parts = re.split(r'[/]', file)
    season = filename_parts[3]
    dest = "./OHEdata/"+season
    gamename = filename_parts[4][:-15] #exclude the _gamestates.pkl part :-)  
    path = dest+"/"+gamename
    try:
        os.mkdir(path)
    except OSError :
        print("Creation of the directory %s failed" %path)
      
        
    gamestates = pd.read_pickle(file)
    # replace None values with 'None' to work with np
    gamestates.replace(to_replace=[None], value='None', inplace=True)
    # initialize nptables
    nplayout = np.zeros((1,333))
    nprobber = np.zeros((len(gamestates.index),19))
    np_pl0_builds = np.zeros((len(gamestates.index),1896))
    np_pl0_devcards = np.zeros((len(gamestates.index),25))
    np_pl1_builds = np.zeros((len(gamestates.index),1896))
    np_pl1_devcards = np.zeros((len(gamestates.index),25))
    np_pl2_builds = np.zeros((len(gamestates.index),1896))
    np_pl2_devcards = np.zeros((len(gamestates.index),25))
    np_pl3_builds = np.zeros((len(gamestates.index),1896))
    np_pl3_devcards = np.zeros((len(gamestates.index),25))
    
    # convert the hex layout,  column 1 is hexlayout
    # hex layout does not change during a game, hence it is saved only once
    # to view it nplayout.reshape(37,9) tested OK
    nplayout[:] = convert_hex_layout(gamestates.iloc[0,1]) 
    
    # for every row of the df, i.e. every game turn
    for turn in range(len(gamestates.index)):
        # convert the robber position, column 3 is robber
        # tested OK
        ohe_robber = convert_robber_position(gamestates.iloc[turn,3]) 
        nprobber[turn,:] = ohe_robber
         
        # convert player 0 building coordinates
        # (note the None is also a category in the ohe endoding)
        #print(gamestates.loc[turn,'pl0setm1':'pl0road15'])
        # ohe_pl0_builds is a np.array of size (1896,)
        ohe_pl0_builds = convert_player_buildings(gamestates.loc[turn,'pl0setm1':'pl0road15'])
        #print(ohe_pl0_builds)
        np_pl0_builds[turn,:] = ohe_pl0_builds
        #print(np_pl0_builds[turn,:])
        
        # convert player 0 dev cards
        np_pl0_devcards[turn,:] = convert_player_devcards(gamestates.loc[turn,'pl0knight1' : 'pl0vp5'])
        
        # convert player 1 building coordinates
        ohe_pl1_builds = convert_player_buildings(gamestates.loc[turn,'pl1setm1':'pl1road15'])
        np_pl1_builds[turn,:] = ohe_pl1_builds
        # convert player 1 dev cards
        np_pl1_devcards[turn,:] = convert_player_devcards(gamestates.loc[turn,'pl1knight1' : 'pl1vp5'])
        
        # convert player 2 building coordinates
        ohe_pl2_builds = convert_player_buildings(gamestates.loc[turn,'pl2setm1':'pl2road15'])
        np_pl2_builds[turn,:] = ohe_pl2_builds
        # convert player 1 dev cards
        np_pl2_devcards[turn,:] = convert_player_devcards(gamestates.loc[turn,'pl2knight1' : 'pl2vp5'])

        # convert player 3 building coordinates
        ohe_pl3_builds = convert_player_buildings(gamestates.loc[turn,'pl3setm1':'pl3road15'])
        np_pl3_builds[turn,:] = ohe_pl3_builds
        # convert player 3 dev cards
        np_pl3_devcards[turn,:] = convert_player_devcards(gamestates.loc[turn,'pl3knight1' : 'pl3vp5'])

        

    # save the np arrays of the game
    np.save(path+"/"+'layout.npy',nplayout)
    np.save(path+"/"+'robber.npy',nprobber)
    np.save(path+"/"+'pl0builds.npy',np_pl0_builds)
    np.save(path+"/"+'pl0devcards.npy',np_pl0_devcards)
    np.save(path+"/"+'pl1builds.npy',np_pl1_builds)
    np.save(path+"/"+'pl1devcards.npy',np_pl1_devcards)
    np.save(path+"/"+'pl2builds.npy',np_pl2_builds)
    np.save(path+"/"+'pl2devcards.npy',np_pl2_devcards)
    np.save(path+"/"+'pl3builds.npy',np_pl2_builds)
    np.save(path+"/"+'pl3devcards.npy',np_pl2_devcards)

