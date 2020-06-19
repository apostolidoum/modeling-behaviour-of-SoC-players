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

from Piece import Piece
from DevCard import DevCard

class PlayerState: 
    """ A class used to present a player state
    
    A game state feature vector describes a players state at a specific point 
    during the game.
    A seperate dataset including the resources information (true nubmer of 
    resources each player holds at each game turn) was collected, but
    was not used in training because it does not distinguish between 
    resource information known to all players and resource information that
    is secret (stealing cards, discarding cards etc.)
    
    Attributes
    ----------
    number : int
        the player's number id
    nickname : str
        the player's nickname
    clay : int
        the player's resource units of clay
    wood : int
        the player's resource units of wood
    ore : int
        the player's resource units of ore
    wheat : int 
        the player's resource units of wheat
    sheep : int
        the player's resource units of sheep
    settlements : list
        the coordinates of the player's settlements   
    cities : list
        the coordinates of the player's cities
    roads : list
        the coordinates of the player's roads
    dev_cards : list
        the development cards the player has bought and/or played
    
    """

    def __init__(self,number, nickname = 'dummy'):
        self.number = number
        self.nickname = nickname
        self.settlements = []
        self.cities = []
        self.roads = []
        self.dev_cards = []
      
        
    def already_exists(self,pieceType, coord):
        """ check if a pieceType has already been place on these coords 
        
        Parameters
        ----------
        piceType : int
            0 for road, 1 for settlement and 2 for city
        coord : int
            the hex coordinate on the board

        Returns
        -------
        bool
            True if successful, False otherwise.         
        """
        
        # PieceTypes as in jSettlers code
        # ROAD = 0
        # SETM = 1
        # CITY = 2
        if pieceType==0:
            # check roads list to see if this road has already been built
            # get list of roads locations
            if coord in [x.location for x in self.roads]:
                return True
            else:
                return False
        elif pieceType==1:
            # check settlements list to see if this setm has already been built
            # get list of setms locations
            if coord in [x.location for x in self.settlements]:
                return True
            else:
                return False
        elif pieceType==2:
            # check cities list to see if this city has already been built
            # get list of cities locations
            if coord in [x.location for x in self.cities]:
                return True
            else:
                return False
        else:
            print("Error in playerstate. pieceType is not a road, settlement \
                  or city type")
        
    def new_build(self,type, coord):
        """ player built something, disambiguation 
        
        if road, setm or city are successfully built returns a str with the 
        type that was built (to change the labels value accordingly)

        Parameters
        ----------
        type : int
            0 for road, 1 for settlement, 2 for city
        coord : int
            the coordinate on the board
        
        Returns
        -------
        Str
            road, setm of city
        """
        
        # IMPORTANT: in the logs the same SOCPutPiece message appears
        #               two times
        #               -> SOCPutPiece
        #               -> SOCGameTextMsg (server announcement)
        #               -> SOCPutPiece again
        #           So CHECK FIRST that you are not trying to build
        #           the same thing twice...
        
        # PieceTypes as in jSettlers code
        # ROAD = 0
        # SETM = 1
        # CITY = 2
        if type == 0: 
            # check that there is no road already there
            # if not exists build it
            if not self.already_exists(0, coord):
                self.built_road(coord)
                return 'road' # successfully built a road
        elif type == 1:
            if not self.already_exists(1,coord):
                self.built_settlement(coord)
                return 'setm'
        elif type == 2:
            if not self.already_exists(2,coord):
                success = self.upgraded_city(coord) #successfully upgraded city
                if success: return 'city'
        else:
            print("Error with pieceType")
        
    def built_settlement(self, location):
        """ updates list of players settlements

        Parameters
        ----------
        location : int
            the hex coordinate location on board

        """
        
        self.settlements.append(Piece(1,location))
        
    def built_road(self, location):
        """ updates list of players roads

        Parameters
        ----------
        location : int
            the hex coordinate location on board
        """
        
        self.roads.append(Piece(0,location))
    
    def upgraded_city(self, location):
        """ updates list of players cities and settlements

        From the player's settlements list deletes the settlement built 
        in that location and appends the city in the list of cities 

        Parameters
        ----------
        location : int
            the hex coordinate location on board  
        """
        
        # delete settlement and make city
        # find stmt with same location
        # delete it 
        # insert city
        # city is piece type 2
        if location not in [x.location for x in self.settlements]:
            print("Error in playerstate. Trying to upgrade to city a \
                  settlement doesn't exist")
            return False #unsuccessful
        else:
            # OK print('trying to delete piece with location: '+str(location))
            # OK print(self.settlements)
            #self.settlements.remove(Piece(1,location))
            # find settlement at given location
            # pieceType = 1 (settlement)
            item_to_del = self.get_piece_at_location(1,location)
            self.settlements.remove(item_to_del)
            # checking
            # OK print('deleted setm')
            # OK self.print_playerState()
            self.cities.append(Piece(2,location))
            # OK print('inserted city')
            # OK self.print_playerState()
            return True # success
    
    def get_piece_at_location(self,pieceType,loc):
        """ Return the piece of piecetype at the given location
        
        Similar to already_exists, but returns the item rather than 
        true/false

        Parameters
        ----------
        pieceType : int
            0 for road, 1 for settlement, 2 for city
        location : int
            hex coordinate location on board

        Returns
        -------
        Piece
            the piece built in that location 
        """
        
        # Like already exists but return the item rather than true/false
        # PieceTypes as in jSettlers code
        # ROAD = 0
        # SETM = 1
        # CITY = 2
        if pieceType==0:
            # check roads list items. if you find item with that location 
            # return it
            for x in self.roads:
                if x.location == loc:
                    return x
            
        elif pieceType==1:
            # check settlements list. if you find item with that location 
            # return it
            for x in self.settlements:
                if x.location == loc:
                    return x
                
        elif pieceType==2:
            # check cities list. if this city has  been built return it
            for x in self.cities:
                if x.location == loc:
                    return x
            
        else:
            print("Error in playerstate. pieceType is not a road, settlement \
                  or city type")
        
    def change_in_resources(self,actionType,elementType,value):
        """ called when there has been a change in the player's resources """
        
        # ActionTypes as in jSettlers code
        SET = 100
        GAIN = 101
        LOOSE = 102
                
        if actionType == SET:
            self.set_resource(elementType, value)
        elif actionType == GAIN:
            self.gain_resource(elementType, value)
        elif actionType == LOOSE:
            self.loose_resource(elementType, value)     
       
            
    def card_action(self,actionType, cardType):
        """ Called when there is a SOCDevCard message in the log 
        
        Parameters
        ----------
        actionType : {'BOUGHT','PLAYED'}
            player bought of played a devcard, other actions ignored    
        cardType : int
            DevCard types as in jSettlers (see DevCard )
        
        Returns
        -------
        Str 
            bought, played, ignore (other action type of unknown card type, i.e. 9)
        """
        
        # check cardType
        # IMPORTANT check cardType
        #           we do not need unknown cards here
        # messages are repeated, the second time with the unknown so
        # ignore unknown cardTypes
        if cardType == 9 : #unknown card
            return 'ignore' # CHECK return value
        else:
            # check action type (ignore action types that you don't care about)
            # ActionTypes as in jSettlers code
            BOUGHT = 0
            PLAYED = 1
            # victory point cards as in jSettlers
            # NOT NEEDED HERE VPCARDS = {4,5,6,7,8}
            # NOTE Also exist a mystery action type 3 for the library dev card
            #       ignore it, we don't care about it here
            if actionType == BOUGHT:
                # make the card and append it to list of cards
                self.bought_devCard(cardType)
                return 'bought'
            elif actionType == PLAYED:
                self.played_devCard(cardType)
                # set played true to the card attribute
                return 'played'
            else:
                return 'ignore'
            
    def bought_devCard(self,cardType):
        """ Updates development card list when player has bought a new card
        
        Called from card_action method when there is a SOCDevCard message in 
        the log of ActionType = 0

        Parameters
        ----------
        cardType : int
            DevCard types as in jSettlers (see DevCard )
        
        """

        # make a card and append it to the list of cards        
        self.dev_cards.append(DevCard(cardType))
        
    
    def played_devCard(self,cardType):
        """Updates development card list when player has played a dev card
        
        Called form card_action when there is a SOCDevCard message in the log 
        of ActionType = 1
        Notice that victory point cards are played immediately when bought

        Parameters
        ----------
        cardType : int
            DevCard types as in jSettlers (see DevCard )
        """
        
        # DONE find the played card and set its played value true
        # search the card list for unplayed cards 
        # find first unplayed card of cardtype
        # set it played
        for x in self.dev_cards: 
            if x.played == False and x.cardType == cardType:
                x.set_played()
                  
        
    def to_list(self):
        """ convert a playerstate to a list of 56 features
        
        Returns
        -------
        list
            The playerstate list
        """
        
        # write with the following order
        # num nickname
        # settlements (5)
        # cities (4)
        # roads(15)
        # knights (14)
        # roadbuilding (2)
        # monopoly (2)
        # discovery (2)
        # vp cards (5)
        
        playerstate_list = [self.number, self.nickname]
        
        settlements_list = [x.location for x in self.settlements]
        pads = 5 - len(settlements_list)
        settlements_list = settlements_list+[None]*pads
        
        cities_list = [x.location for x in self.cities]
        pads = 4 - len(cities_list)
        cities_list = cities_list+[None]*pads
        
        roads_list = [x.location for x in self.roads]
        pads = 15 - len(roads_list)
        roads_list = roads_list+[None]*pads
        
        playerstate_list = playerstate_list+settlements_list+cities_list+roads_list

        
        # find knight cards if any
        # kinght -> cardType0
        knights_num = self.played_cards(0)
        pads = 14 - knights_num
        knights_list = [True]*knights_num + [False]*pads
        
        # road building cards
        # road building card type -> 1
        rb_num = self.played_cards(1)
        pads = 2- rb_num
        rb_list = [True]*rb_num+[False]*pads
        
        # monopoly cards
        # monopoly card type -> 3
        monopoly_num = self.played_cards(3)
        pads = 2 - monopoly_num
        monopoly_list = [True]*monopoly_num+[False]*pads
        
        # discovery cards
        # discovery card type -> 2
        discovery_num = self.played_cards(2)
        pads = 2 - discovery_num
        discovery_list = [True]*discovery_num+[False]*pads
        
        # VP1 card
        # card type -> 4
        if self.played_cards(4) == 1:
            VP1=True
        else:
            VP1=False
        # VP2 card
        # card type -> 5
        if self.played_cards(5) == 1:
            VP2=True
        else:
            VP2=False
        # VP3 card
        # card type -> 6
        if self.played_cards(6) == 1:
            VP3=True
        else:
            VP3=False
        # VP4 card
        # card type -> 7
        if self.played_cards(7) == 1:
            VP4=True
        else:
            VP4=False
        # VP5 card
        # card type -> 8
        if self.played_cards(8) == 1:
            VP5=True
        else:
            VP5=False
            
        # list of dev cards the player has played
        dev_cards_list = knights_list+rb_list+monopoly_list+discovery_list
        dev_cards_list.append(VP1)
        dev_cards_list.append(VP2)
        dev_cards_list.append(VP3)
        dev_cards_list.append(VP4)
        dev_cards_list.append(VP5)
        
        playerstate_list = playerstate_list+dev_cards_list
        # check list size
        if len(playerstate_list) != 51:
            print("Error with player state list")
        
        return playerstate_list
    
    def played_cards(self, cardType):
        """ Number of cards the player has played 
        
        Returns
        -------
        int
            a number that show how many cards of cardType the player
            has played
        """

        count = 0
        for x in self.dev_cards:
            if x.cardType == cardType and x.played ==True:
                count = count + 1
        return count
    
    
    def print_playerState(self):
        """ print the attributes of a playerState """
        
        print('PLAYER INFO')
        print('-----------')
        print('number: ' + str(self.number) )
        print('nickname: '+ str(self.nickname))
        # TO DO resources
        # check if empty
        if not self.settlements :
            print('no settlements')
        else:
            print('settlements: ')
            for x in self.settlements:
                print('    location: ' + str(x.location) )
        
        if not self.cities:
            print('no cities')
        else:
            print('cities: ')
            for x in self.cities:
                print('    location: ' + str(x.location) )
        
        
        if not self.roads:
            print('no roads')
        else:
            print('roads: ')
            for x in self.roads:
                print('    location: ' + str(x.location) )
                
       
        print('Development Cards')
        for card in self.dev_cards:
            card.print_card()
        
        
        
        
#######################
## TESTING
#######################
#plstate = PlayerState(5,'GOD')
#plstate.print_playerState()
#plstate.built_road(0)
#plstate.print_playerState()
#what = plstate.new_build(0,5) #road at location 5
#print('player built a '+str(what))
#plstate.print_playerState()
## try to rebuild road at 0
#what = plstate.new_build(0,0)
#print('player built a '+str(what))
#plstate.print_playerState()
## check resources
#plstate.change_in_resources(101,1,4) # gain 4 clays
#plstate.print_playerState()
#plstate.change_in_resources(102,1,2) # loose 2  clays
#plstate.print_playerState()
#plstate.change_in_resources(100,2,3) # set 3 ores
#plstate.print_playerState()
## build settlements
#what = plstate.new_build(1,10)
#print('player built a '+str(what))
#what = plstate.new_build(1,12)
#print('player built a '+str(what))
#plstate.print_playerState()
## upgrade setm at 10 to city
#what = plstate.new_build(2,10)
#print('player built a '+str(what))
#plstate.print_playerState()
## try to upgrade imaginary seem at 50 
#what = plstate.new_build(2,50)
#print('player built a '+str(what))
#plstate.print_playerState()
#########
## Testing the dev cards
#plstate.card_action(0,4) # buy vp card
#plstate.print_playerState()
#plstate.card_action(0,0) # buy knight
#plstate.print_playerState()
## now play the knight card that you bought
#plstate.card_action(1,0)
#print('played a knight card type -0-')
#plstate.print_playerState()

        
