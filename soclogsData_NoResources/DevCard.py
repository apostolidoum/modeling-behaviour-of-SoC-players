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

class DevCard: 
    """ A class used to present a development card
    
    In the Settlers of Catan there are 25 development cards:
        14 knight cards
        2 Road Building cards
        2 Monopoly cards
        2 Discovery cards
        5 Victory Point cards
    
 
    Attributes
    ----------
    cardType : int
        codes  for the types of Dev Cards as in jSettlers    
    bought : boolean
        Dev card bought flag
    played : boolean
        Dev card played flag

    """

    # card Types as in jSettlers code
    # ATTENTION IMPORTANT changes from version 1 to later versions
    #                       unknown and knight codes have been switched
    # Here: version 1 codes
    KNIGHT = 0 # knight card (14 in total)
    ROAD = 1 # road building card (2 in total)
    DISC = 2 # discovery card aka year of plenty (2 in total)
    MONO = 3 # monopoly card (2 in total)
    CAP = 4 # VP card aka capitol aka governors house (1st of 5)
    LIB = 5 # VP card aka library aka market (2nd of 5)
    UNI = 6 # VP card aka university  (3rd of 5)
    TEM = 7 # VP card aka temple  (4th of 5)
    TOW = 8 # VP card aka tower  (5th of 5)
    UNK = 9 # unknown (used to represent hidden cards to other players)
    
    # VP cards only bought, never played by action type 1
    def __init__(self, cardType):
        
        self.cardType = cardType
        self.bought = True # player has bought the dev card
        self.played = False
        
    def set_played(self):
        self.played = True
       
            
    def print_card(self):
        print("type: "+str(self.cardType)+" played: "+str(self.played))
            
#############################
## TESTING
#############################
#my_card = DevCard(0)
#my_card.print_card()
#my_card.set_played()
#my_card.print_card()

    
    
