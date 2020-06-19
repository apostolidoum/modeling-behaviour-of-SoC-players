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




class Labels: 
    """ A class used to present the labels of a game turn
    
    labels that are true mean that at the given turn the player did the 
    action indicated by the label. if no action label is turned into True
    a no action label is "activated"
    
    Attributes
    ----------
    turn : int
        the gameturn
    played_dev_card : boolean
    built_road : boolean
    built_setm : boolean
    upgraded_city : boolean
    bought_dev_card : boolean
    made_offer : boolean
        player suggested a trading offer to another player
    traded_with_player : boolean
    traded_with_bank : boolean
    traded_with_port : boolean
    no_action : boolean

    """
    
    def __init__(self,turn):
        self.turn = turn
        self.played_dev_card = False
        self.built_road =  False
        self.built_setm = False
        self.upgraded_city = False
        self.bought_dev_card = False
        self.made_offer = False
        self.traded_with_player = False
        self.traded_with_bank = False
        self.traded_with_port = False
        self.no_action = False 
        
    def print_labels(self):
        """ Print the labels' values """
        
        print('~~~~~~~~~~~~')
        print('  LABELS    ')
        print('~~~~~~~~~~~~')
        print('turn: '+str(self.turn))
        print('played development card: '+str(self.played_dev_card))
        print('built a road: '+str(self.built_road))
        print('built a settlement: '+str(self.built_setm))
        print('upgraded a settlement to city: '+str(self.upgraded_city))
        print('bought a development card: ' +str(self.bought_dev_card))
        print('made a trading offer: '+str(self.made_offer))
        print('traded with another player: '+str(self.traded_with_player))
        print('traded with the bank: '+ str(self.traded_with_bank))
        print('traded from a port: ' +str(self.traded_with_port))
        print('no action: '+str(self.no_action))        
        
        
    def check_no_action(self):
        """ Check if no action was made during a game turn 
        
        if no action label has been turned into true during a game turn
        turn the no action label true. Call this function just before you 
        are ready to finalize and save the labels
        """
        
        # if any of the labels is true
        if (self.played_dev_card | self.built_road | self.built_setm |
                self.upgraded_city | self.bought_dev_card | self.made_offer |
                self.traded_with_player | self.traded_with_bank |
                self.traded_with_port):
            self.no_action = False
        else:
            self.no_action = True
            
    def update_buildings(self,pieceType):
        """ Update the labels when the player builts a road, city or settlement
        
        Check what was built by the player when he put a piece on the board  and
        update the labels of the turn
    
        Parameters
        ----------
        pieceType : str
            road, setm or city
    
        """
        
        if pieceType == 'road':
            self.built_road = True
        elif pieceType == 'setm':
            self.built_setm = True
        elif pieceType == 'city':
            self.upgraded_city = True
        else:
            pass
            # no error..just ignoring other piece types
            # print("Error setting label for the type of piece that was built")
         
    def write_to_DF(self):
        """ return labels to list form to write a row at labelsDF """

        # TO DO self.made_offer , self.traded_with_player,
        #       self.traded_with_bank,  self.traded_with_port = False
        return [self.turn, self.played_dev_card, self.built_road,
                self.built_setm,self.upgraded_city,self.bought_dev_card, 
                self.made_offer, self.traded_with_player, 
                self.traded_with_bank, self.traded_with_port,self.no_action]
        
        
###########################
## TESTING
###########################
#my_labels0 = Labels(0)
#my_labels0.print_labels()
#my_labels0.check_no_action()
#my_labels0.print_labels()
#my_labels1 = Labels(1)
#my_labels1.built_road = True
#my_labels1.print_labels()
#my_labels1.check_no_action()
#my_labels1.print_labels()
        
        
        
        
        
