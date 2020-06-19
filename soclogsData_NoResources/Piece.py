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

class Piece():
    """ A class used to present a piece of the game 
    
    A class that represents the settlements, roads and cities that a player 
    can build on the board. Pieces use the same labels as the jSettlers code 
    (PieceTypes).
    
    Attributes
    ----------
    type : int
        0 for road, 1 for settlement, 2 for city, as in jSettlers
    location : int
        the hexadecimal number indicated the board coordinate
    
    
    """
    
    # piece types as in jSettlers
    # NOTE: piece are represented with that piece type in the PutPiece messages
    #       the PlayerElement messages use element types for roads, cities and
    #       settlements 
    #       corresponding Element types are
    #       ROAD = 10
    #       SETM = 11
    #       CIYT = 12
    # CAREFUL what messages you are using to collect your info
    
    ROAD = 0
    SETM = 1
    CITY = 2 
    
    def __init__(self, type, location):
        self.type = type 
        self.location = location 
        
    
