#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# Thesis code
# A model that emulates players' actions in the Settlers of Catan (SOC) game
# based on linguistic references and previous actions.
# 
# Data: jSettlers game logs (.soclog)
# Author: Apostolidou Maria
# Technical University of Crete
# Spring Semester, 2019
##############################################################################


from PlayerState import PlayerState

class GameState: 
    """ A class used to present a game state
    
    A game state feature vector describes the game state at a specific turn.
    A collection of (#game turns) features describes a whole game
    
    Attributes
    ----------
    turn : int
        the gameturn
    robber : int
        the hex coordinates of the robber's position
    player0 : Playerstate
        playerstate of the player sitting at position 0 (player id = 0)
    player1 : Playerstate
        playerstate of the player sitting at position 1 (player id = 1)
    player2 : Playerstate
        playerstate of the player sitting at position 2 (player id = 2)
    player3 : Playerstate
        playerstate of the player sitting at position 3 (player id = 3) 
    
    
    """
    
    def __init__(self,turn, hexLayout, numLayout,robberHex, player0state,
                 player1state, player2state, player3state):
        self.turn = turn
        self.board = {'hexLayout' : hexLayout , 'numLayout' : numLayout}
        self.robber = robberHex
        self.player0 = player0state
        self.player1 = player1state
        self.player2 = player2state
        self.player3 = player3state
        
    def place_robber(self, coord):
        """ set robber position on board"""
        
        self.robber = coord
    
                
    def write_to_DF(self):
        """ returns the game state in list form to write to gamestateDF """

        # write to row of our turn
        # write a list of 228  features
        row_vals = [self.turn] 
        row_vals.append(self.board['hexLayout']) 
        row_vals.append(self.board['numLayout'])
        row_vals.append(self.robber)
        
        # append the players state features
        row_vals = row_vals + self.player0.to_list()
        row_vals = row_vals + self.player1.to_list()
        row_vals = row_vals + self.player2.to_list()
        row_vals = row_vals + self.player3.to_list()
        # check list size
        if len(row_vals) != 208:
            print("Error with game state size")
            print("len of game state "+str(len(row_vals)))
            
        # OK print(row_vals) #OK
        return row_vals
                
        
    def print_GameState(self):
        """ prints the values of a gamestate"""

        print('~~~~~~~~~~~~')
        print(' GAME STATE')
        print('~~~~~~~~~~~~')
        print('turn: '+str(self.turn))
        print('board: '+str(self.board))
        print('robber: '+str(self.robber))
        self.player0.print_playerState()
        self.player1.print_playerState()
        self.player2.print_playerState()
        self.player3.print_playerState()
        
#######################
##        Testing
#######################
#        # board of pilot01
#player0state = PlayerState(0,'rennoc1')
#print(player0state.ore)
#testfeature = GameState (0,[9, 6, 67, 6, 6, 2, 5, 1, 66, 8, 2, 3, 1, 2, 6, 6, 5, 3, 4, 1, 4, 11, 36, 5, 4, 0, 5, 6, 6, 4, 3, 3, 97, 21, 6, 12, 6],
#                         [-1, -1, -1, -1, -1, 8, 9, 6, -1, -1, 2, 4, 3, 7, -1, -1, 5, 1, 8, 2, 5, -1, -1, 7, 6, -1, 1, -1, -1, 3, 0, 4, -1, -1, -1, -1, -1],
#                         0x97, player0state, PlayerState(1), PlayerState(2),
#                         PlayerState(3))
#print(testfeature.turn)
#print(testfeature.board)
#
#print(testfeature.robber)
#print(testfeature.player0.nickname)
#print(testfeature.player2.nickname)
#

