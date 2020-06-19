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

""" Creating the game state and chat features and labels

Makes a feature vector for every game turn that shows the game state
#GameStates = #game turns for each log file
Makes the labels
Write all the chat data to a file
"""

import re
import pandas as pd
from GameState import GameState
from PlayerState import PlayerState
from Labels import Labels

# the soclog files
soclog_files = ["reduced/pilot/pilot20.soclog",
                  "reduced/pilot/pilot04.soclog",
                  #"reduced/pilot/pilot19.soclog",
                  "reduced/pilot/pilot08.soclog",
                  "reduced/pilot/pilot10.soclog",
                  "reduced/pilot/pilot12.soclog",
                  "reduced/pilot/pilot07.soclog",
                  #"reduced/pilot/pilot18.soclog",
                  "reduced/pilot/pilot15.soclog",
                  "reduced/pilot/pilot21.soclog",
                  "reduced/pilot/pilot01.soclog",
                  "reduced/pilot/pilot06.soclog",
                  "reduced/pilot/pilot05.soclog",
                  "reduced/pilot/pilot03.soclog",
                  "reduced/pilot/pilot13.soclog",
                  "reduced/pilot/pilot17.soclog",
                  "reduced/pilot/pilot09.soclog",
                  "reduced/pilot/pilot02.soclog",
                  "reduced/pilot/pilot16.soclog",
                  "reduced/pilot/pilot11.soclog",
                  "reduced/pilot/pilot14.soclog",
                  "reduced/season2/League 8 Game 2-2012-11-26-18-55-31-+0000.soclog",
                  "reduced/season2/Master League final-2012-12-05-16-59-57-+0000.soclog",
                  "reduced/season2/League4-2012-11-09-19-08-53-+0000.soclog",
                  "reduced/season2/Game 3-2012-11-25-20-09-16-+0000.soclog",
                  "reduced/season2/Master League Game 3-2012-11-17-17-01-18-+0000.soclog",
                  "reduced/season2/League4-2012-11-24-09-17-47-+0000.soclog",
                  "reduced/season2/master league 4-2012-12-04-17-37-56-+0000.soclog",
                  "reduced/season2/SOCL League 5 Game 2-2012-11-25-17-25-09-+0000.soclog",
                  "reduced/season2/League3Game5-2012-11-30-19-59-18-+0000.soclog",
                  "reduced/season2/league 5 last game-2012-12-09-21-08-39-+0000.soclog",
                  "reduced/season2/3version2-2012-11-21-20-23-31-+0000.soclog",
                  "reduced/season2/League 5 game 3-2012-11-26-00-51-20-+0000.soclog",
                  "reduced/season2/League8-2012-11-24-12-04-51-+0000.soclog",
                  "reduced/season2/Test-2012-10-16-14-53-15-+0100.soclog",
                  "reduced/season2/L5 practicegame-2012-11-11-19-26-36-+0000.soclog",
                  "reduced/season2/league4_attempt2-2012-11-14-19-46-22-+0000.soclog",
                  "reduced/season2/Master league game 2-2012-11-13-18-07-14-+0000.soclog",
                  "reduced/season2/SOCL League 5 Game 4-2012-12-03-02-11-10-+0000.soclog",
                  "reduced/season2/L5 Real game-2012-11-11-19-58-55-+0000.soclog",
                  "reduced/season2/League3Game1-2012-11-18-20-34-38-+0000.soclog",
                  "reduced/season2/Settles league 1-2012-11-08-18-05-34-+0000.soclog",
                  "reduced/season2/League3Game4-2012-11-28-20-01-30-+0000.soclog",
                  "reduced/season2/practice-2012-10-30-18-41-07-+0000.soclog",
                  "reduced/season1/league3minus1-2012-05-25-22-22-21-+0100.soclog",
                  "reduced/season1/league 3 (-k)-2012-06-25-18-22-53-+0100.soclog",
                  "reduced/season1/League 1 game-2012-06-19-18-49-00-+0100.soclog",
                  "reduced/season1/League2.4-2012-06-26-22-47-04-+0100.soclog",
                  "reduced/season1/league3-2012-05-27-19-53-48-+0100.soclog",
                  "reduced/season1/League 1-2012-06-17-19-53-24-+0100.soclog",
                  "reduced/season1/league2.2-2012-06-18-20-50-12-+0100.soclog",
                  "reduced/season1/3-2012-06-06-19-58-56-+0100.soclog",
                  "reduced/season1/League 1.1-2012-06-21-18-58-22-+0100.soclog",
                  "reduced/season1/League 3 Finale-2012-06-25-21-57-53-+0100.soclog",
                  "reduced/season1/League 2-2012-06-26-20-23-20-+0100.soclog",
                  "reduced/season1/league3practice-2012-05-31-19-23-46-+0100.soclog",
                  "reduced/season1/League2-2012-06-17-19-58-07-+0100.soclog",
                  "reduced/season1/League 1.2-2012-06-21-20-27-05-+0100.soclog",
                  "reduced/season1/league1 31may-2012-05-31-19-59-37-+0100.soclog",
                  "reduced/season1/league3 michael-2012-06-17-20-54-03-+0100.soclog"]



###################################################
# NOTE: for the NN i need inputs of the same size
#       gamestate vectors don't have fixed length
#       but table row have standard size
###################################################
# pandas table to save gamestate values of a single SOC game
# all possible pieces the player could put on board and
# all possible development cards the player could play are here
# each player has at his dispotion 5 settlements, 4 cities and 15 roads to 
# place on board
# and there are 25 development cards he could potentially buy 
#
# in total we have 228 attributes to represent a game state
# TO FIX index.pdf (wrong counting, not 231 features but 228)
# 228 fixed length input for a NN
gamestate_columns = ["Turn", "BoardHexLayout", "BoardNumLayout", "Robber",
           "player0num", "player0nickname",
           "pl0setm1","pl0setm2","pl0setm3","pl0setm4","pl0setm5",
           "pl0city1", "pl0city2", "pl0city3","pl0city4",           
           "pl0road1","pl0road2","pl0road3","pl0road4","pl0road5","pl0road6",
           "pl0road7","pl0road8","pl0road9","pl0road10","pl0road11",
           "pl0road12","pl0road13","pl0road14","pl0road15",
           "pl0knight1","pl0knight2","pl0knight3","pl0knight4","pl0knight5",
           "pl0knight6","pl0knight7","pl0knight8","pl0knight9","pl0knight10",
           "pl0knight11","pl0knight12","pl0knight13","pl0knight14",
           "pl0roadbuilding1","pl0roadbuilding2",
           "pl0monopoly1","pl0monopoly2",
           "pl0discovery1","pl0discovery2",
           "pl0vp1","pl0vp2","pl0vp3","pl0vp4","pl0vp5",
           "player1num", "player1nickname",
           "pl1setm1","pl1setm2","pl1setm3","pl1setm4","pl1setm5",
           "pl1city1", "pl1city2", "pl1city3","pl1city4",           
           "pl1road1","pl1road2","pl1road3","pl1road4","pl1road5","pl1road6",
           "pl1road7","pl1road8","pl1road9","pl1road10","pl1road11",
           "pl1road12","pl1road13","pl1road14","pl1road15",
           "pl1knight1","pl1knight2","pl1knight3","pl1knight4","pl1knight5",
           "pl1knight6","pl1knight7","pl1knight8","pl1knight9","pl1knight10",
           "pl1knight11","pl1knight12","pl1knight13","pl1knight14",
           "pl1roadbuilding1","pl1roadbuilding2",
           "pl1monopoly1","pl1monopoly2",
           "pl1discovery1","pl1discovery2",
           "pl1vp1","pl1vp2","pl1vp3","pl1vp4","pl1vp5",
           "player2num", "player2nickname",
           "pl2setm1","pl2setm2","pl2setm3","pl2setm4","pl2setm5",
           "pl2city1", "pl2city2", "pl2city3","pl2city4",           
           "pl2road1","pl2road2","pl2road3","pl2road4","pl2road5","pl2road6",
           "pl2road7","pl2road8","pl2road9","pl2road10","pl2road11",
           "pl2road12","pl2road13","pl2road14","pl2road15",
           "pl2knight1","pl2knight2","pl2knight3","pl2knight4","pl2knight5",
           "pl2knight6","pl2knight7","pl2knight8","pl2knight9","pl2knight10",
           "pl2knight11","pl2knight12","pl2knight13","pl2knight14",
           "pl2roadbuilding1","pl2roadbuilding2",
           "pl2monopoly1","pl2monopoly2",
           "pl2discovery1","pl2discovery2",
           "pl2vp1","pl2vp2","pl2vp3","pl2vp4","pl2vp5",
           "player3num", "player3nickname",
           "pl3setm1","pl3setm2","pl3setm3","pl3setm4","pl3setm5",
           "pl3city1", "pl3city2", "pl3city3","pl3city4",           
           "pl3road1","pl3road2","pl3road3","pl3road4","pl3road5","pl3road6",
           "pl3road7","pl3road8","pl3road9","pl3road10","pl3road11",
           "pl3road12","pl3road13","pl3road14","pl3road15",
           "pl3knight1","pl3knight2","pl3knight3","pl3knight4","pl3knight5",
           "pl3knight6","pl3knight7","pl3knight8","pl3knight9","pl3knight10",
           "pl3knight11","pl3knight12","pl3knight13","pl3knight14",
           "pl3roadbuilding1","pl3roadbuilding2",
           "pl3monopoly1","pl3monopoly2",
           "pl3discovery1","pl3discovery2",
           "pl3vp1","pl3vp2","pl3vp3","pl3vp4","pl3vp5"]
gamestatesDF = pd.DataFrame(columns=gamestate_columns,index=None)

# pandas table to save labels values of a game
label_columns = ["Turn","playedDevCard","builtRoad","builtSettlement",
                 "upgradedCity","boughtDevCar","madeOffer",
                 "tradedWithPlayer", "tradedWithBank","tradedWithPort",
                 "no_action"]
labelsDF = pd.DataFrame(columns=label_columns, index=None)

# pandas table to save chats from SOCGameTextMsg
chat_columns = ["Turn", "emitter_nickname","text"]
chatsDF = pd.DataFrame(columns=chat_columns,index=None)

# IMPORTANT: gamestatesDF have
#               number of DF rows = number of turns in the game
#            labelsDF have
#               number of DF row = number of turns -1 
#               (because the initial setup phase aka turn0 produces no labels)
#               added +1 at turn 0 with all labels false and we are set to go
#            BUT chatsDF will not have that many rows...
# NOTE: (to future me):
#               maybe i will have to group all chat utterances by turn 
#               to make a single vector for NN input..or not 

def read_soclog(soclog):
    """ Reads a soclog file as a panda dataframe
    
    Reads a soclog file from the reduced soclogfiles. These are the files that
    contain only the useful rows of data from the original log files.
    Produces a pandas dataframe with columns Turn, MessageType and Message.
    
    Parameters
    ----------
    soclog : filename
        The .soclog file from the reduced soclogs (see /reduced)
        
    Returns
    -------
    dataframe
        A pandas dataframe with the Turn, MessageType and Message columns
    """

    column_names = ['Turn','MessageType','Message']
    df = pd.read_csv(soclog, sep = ':', header = None, names = column_names)
    return df

def initial_setup_state(df):
    """ Creates the game state for the initial setup phase of the game
    
    Creates the game state for the setup phase of the game, i.e. turn 0.
    During this phase each player places on board his first 2 settlements and 
    2 roads.
    Also returns all chat messages during this phase to save to chatsDF
    
    Parameters
    ----------
    df : pandas dataframe 
        The soclogs in dataframe form, as returned from read_soclog() for tun 0
    
    Returns
    -------
    turn0_game_state : GameState feature vector
        The game state feature vector from the initial set-up phase
    chats0 : a pandas df 
        The chat messages during the setup phase
    """
    
    # DONE: call methods with specific rows to retrieve the info
    
    # DONE: call get_board with message SOCBoardLayout to get board and robber
    #     locate row of SOCBoard Layout and call the get_board(SOCBoardLayout)
    
    # IMPORTANT : Maybe i should only get turn 0 df part
    
    # NOTE : turn 0 has no labels  (it is not an actual player's turn)
    
    # locate the SOCBoardLayout message
    board_message = df.loc[df.MessageType == "SOCBoardLayout"]
    # get_board returns tuple (hexLayout, numLayout,robberHex)
    (hexlayout,numlayout,robberHex) = get_board(board_message.Message.item())
  
        
    # call get_players to get the players nicknames and ids
    # find SOCSitDown messages
    sitDown_messages = df.loc[df.MessageType == "SOCSitDown"]
    # players is a dictionary key:playernum value:nickname
    players = get_players(sitDown_messages)   
    
    # DONE : get placement of road and settlement
    # find SOCPutPiece messages
    putPiece_messages = df.loc[df.MessageType == "SOCPutPiece"]
    buildings = get_buildings0(putPiece_messages)
      
    # create players states
    playerstate = []
    for x in range(4):
        playerstate.append(PlayerState(x,players[x]))
    
    # update playerStates with the buildings of turn 0
    for player in buildings:
        # for all of player's roads
        for road in buildings[player][0]: # ROAD = 0            
            playerstate[player].built_road(road)
            
        for settlement in buildings[player][1]: # SETM = 1
            playerstate[player].built_settlement(settlement)
    

    # create game state
    turn0_game_state = GameState(0,hexlayout,numlayout, hex(robberHex), 
                                 playerstate[0], playerstate[1], playerstate[2],
                                 playerstate[3])
    
    # get the chat messages 
    game_txt_messages = df.loc[df.MessageType == "SOCGameTextMsg"]
    chats0 = get_chats0(game_txt_messages)
    return (turn0_game_state, chats0)
    
def get_board(message):
    """ Gets the board layout from the data 
    
    Fills in the board layout part of the game state feature vector. The 
    hexLayout refers to the resources each hexagon on the board offers. The 
    numLayout refers to dice number corresponding to each hexagon. Initial 
    placement of the robber (in the dessert hexagon) is also found here. 
    This information is retrieved from the message of type SOCBoardLayout,
    during the initial set up phase of the game (turn 0). 
    
    Parameters
    ----------
    message: str
        A SOCBoardLayout message  
        
    Return
    ------
    hexLayout: int list
        The resources on the board. (See jSettlers boardlayout class to map 
        these numbers to the coresponding resource types.)
    numLayout: int list
        The dice number on each board hexagon (See also jSettlers boardLayout)
    robberHex: hexadecimanl coordinate
        Initial position of the robber (on the dessert hexagon)
        
    """
    
    # break message to fields with del |
    # hexLayout -> field[1]
    # numberLayout -> field[2]
    # robberHex -> field[3]
    fields = message.split('|')
    hexLayout_message = fields[1]
    numLayout_message = fields[2]
    robberHex_message = fields[3]
    
    # frome messages extract values and return them
    # OK print(hexLayout_message) # this is a str
    hexLayout = get_int_values(hexLayout_message)
    numLayout = get_int_values(numLayout_message)
    robberHex = get_int_value(robberHex_message,'hex')
    return (hexLayout, numLayout, robberHex)
    
def get_int_values(layoutmessage):
    """ Converts a layout from a str message to a list of numbers 
    
    From a string of the form "infoname= { ...int values...}" returns only the
    int values in a list of integers
    
    Parameters
    ----------
    layoutmessage: str
        A str describing the hex or num Layout (e.g. hexLayout= { 50 6 ... 6})
        
    Returns
    -------
    layout: int list
        The mapped list of integers
    """
    
    # DONE convert str message to int list
    # split and keep only { ... } part
    # convert it to list of ints DONE
    
    # string with only the numbers
    # keep only text within brackets
    numstr = layoutmessage[layoutmessage.find("{")+1:layoutmessage.find("}")]
    # integer list from the numstr
    # split  on spaces, map strings to ints
    # list is needed from python 3...
    layout = list(map(int, numstr.split()))
    # OBSOLETE numstr = re.searc# OK h(r'\{.*?\}', layoutmessage)   
    # OK print(numstr)
    # OK print('-return value-')
    # OK print(layout)
    return layout
    
def get_int_value(message, base):
    """ Converts a field from a str message to a number
    
    From a string of the form "varname=val" returns only the value in hex
    
    Parameters
    ----------
    message: str
    base: str, hex or dec
    
    Returns
    -------
    val: int (hexadecimal)
    """
    
    num = message[message.find("=")+1:]
    if base == 'hex':
        val = int(num, 16)
    else:
        val = int(num,10)
    return val

def get_players(df):
    """ Finds players' nicknames and number ids
    
    From the SOCSitDown messages of the soclogs, finds the nicknames and 
    player ids of the people participating in the game
    
    Parameters
    ----------
    df: pandas dataframe
        The rows of the game dataframe that hold SOCSitDown messages at turn 0
    
    Returns
    -------
    nicks: dictionary
        players' nicknames and numbers, key:playerid(0,1,2,3) value:nickname
    """
    
    # initialized to dummy as in jSettlers 
    nicks = {0: 'dummy',
             1: 'dummy',
             2: 'dummy',
             3: 'dummy'}    

    # keep only the message field of the log
    # select all rows from column Message
    messages = df.loc[:, 'Message']

    # OK print(messages) # OK
    
    for x in messages:
        # break message by |
        fields = x.split('|')
        # field[0] -> game=sth
        # field[1] -> nickname=sth
        # field[2] -> playerNumber=sth
        # field[3] -> robotFlag=false
        # OK print(x.split('|'))
        playernum = get_int_value(fields[2],'dec')
        # from field[1] keep only the part after "="
        nickname = fields[1][fields[1].find("=")+1:]
        # OK print(playernum) # OK
        # OK print(nickname)  # OK
        
        # MAYBE check both for dummy to avoid overwritting when there have been 
        # reconnection problems (for future worring, so far no bugs)
        if nickname != 'dummy' :
            nicks[playernum] = nickname
        # OK print(nicks)
        
        
        # DONE if nickname not dummy -> change nicks val accordingly
    # OK print('FInIshED') #OK
    # OK print(nicks)
    return nicks

def get_buildings0(df):
    """ Returns the positions where the players placed 1st road and settlement.
    
    During the initial setup phase all players place a settlement and a road
    on the board.
    
    Parameters
    ----------
    df: pandas dataframe
        The rows of the game dataframe that hold SOCPutPiece messages at turn 0
    
    Returns
    -------
    buildings: dictionary
        players' settlements and roads at turn 0 
    """

    # ATTENTION: the same messages are written 2 times in the soclogs...
    #            no problem so far because no info is changed, only assigned 
    #            twice the same value
    # REMEMBER: pieceType = 0 is road
    #           pieceType = 1 is settlement
    #           pieceType = 2 is city
    
    ROAD = 0 
    SETM = 1
    
    # initialize
    # after initial phase supposed to have two roads and 2 settlements placed
    buildings = {0: {ROAD:[],SETM:[]},
                 1: {ROAD:[],SETM:[]},
                 2: {ROAD:[],SETM:[]},
                 3: {ROAD:[],SETM:[]}
                 }    

    # keep only the message field of the log
    # select all rows from column Message
    messages = df.loc[:, 'Message']
    
    for x in messages:
        # break message by |
        fields = x.split('|')
        # field[0] -> game=sth
        # field[1] -> playerNumber=sth
        # field[2] -> pieceType=num
        # field[3] -> coord=num  is in hex
        # OK print(x.split('|'))
        playernum = get_int_value(fields[1],'dec')
        pieceType = get_int_value(fields[2],'dec')
        pieceCoord = hex(get_int_value(fields[3],'hex'))
        
        # set dictionary values
        
        # ATTENTION how you write pieceCoord
        #           when converted with hex it is viewed as an str
        if pieceCoord not in buildings[playernum][pieceType]:
            buildings[playernum][pieceType].append(pieceCoord)
        
    return buildings
        
    
    
def get_state(df,prev_state):
    """ Creates a game state for a specific turn
    
    For the logs of a game turn calls methods to extract the infromation 
    from each MessageType. 
    
    Parameters
    ----------
    df: pandas dataframe
        The soclogs in dataframe form, as returned from read_soclog() for a
        given turn
    prev_state: game state at the previous turn 
        
    Returns
    -------
    game_state: GameState feature vector
        The game state feature vector of the game turn
    labels : Labels
        The prediction labels for this game turn
    """
    
    # check every row
    # call method for the MessageType of the row
    # save all that info to a game state vector
    # (after return save that to a pandas dataframe that represents the game
    
    # at the previous turn the game state was prev_state
    # we start from this and every action changes the state a little bit 
    # temp_state shows the state after every little action
    # after we will have examined all rows or the log for a turn
    # the temp_state will have the final form of the game state at the given 
    # turn
    # create a new game state vector, copy previous one and change turn num
    #   GameState(turn, hexLayout, numLayout,robberHex, player0state,
    #             player1state, player2state, player3state)
    
    temp_state = GameState(prev_state.turn + 1,prev_state.board['hexLayout'],
                           prev_state.board['numLayout'], prev_state.robber,
                           prev_state.player0, prev_state.player1,
                           prev_state.player2,prev_state.player3)
    
    # create a new labels vector
    labels = Labels(prev_state.turn + 1)
    # OK temp_state.print_GameState()
    
    # chatsDF within local scope, to be returned and then appended to chatsDF
    chat_columns = ["Turn", "emitter_nickname","text"]
    turn_chatsDF = pd.DataFrame(columns=chat_columns,index=None)
    
    for index,row in df.iterrows():
        if row["MessageType"] == "SOCGameTextMsg":
            # get the chat message 
            (nickname,chat_msg) = get_chat(row)
            # if nickname is Server check to see if
            # player traded with port/bank message occured
            # else (nickame is a player's nickname)
            # append it to the temporary df (chats of this turn)
            if nickname == "Server":
                if re.search("traded .* bank",chat_msg):
                    # set label true
                    labels.traded_with_bank = True
                if re.search("traded .* port", chat_msg):
                    # set label true
                    labels.traded_with_port = True
            else:
                turn_chatsDF = turn_chatsDF.append({'Turn':temp_state.turn,
                                  'emitter_nickname':nickname,
                                  'text':chat_msg}, ignore_index=True)
        elif row["MessageType"] == "SOCPutPiece":
            buildings = putPiece(row)            
            # check who built what and change temp game state accordingly
            # check who it was...
            # buildings -> {'playernum':playernum, 'pieceType':pieceType,'pieceCoord': pieceCoord}
            if buildings['playernum'] == 0 :
                # change state of player0
                # _type_ = road if a road is successfully built
                # _type_ = setm if a settlement is indeed successfully built
                # _type_ = city if a city is indeed successfully built
                # _type_ = None if an unsuccessful attempt to built was made
                # use _type_ to update labels
                _type_ = temp_state.player0.new_build(buildings['pieceType'],
                                            buildings['pieceCoord'])
                labels.update_buildings(_type_)
            elif buildings['playernum'] == 1 :
                # change state of player1
                _type_ = temp_state.player1.new_build(buildings['pieceType'],
                                            buildings['pieceCoord'])
                labels.update_buildings(_type_)
            elif buildings['playernum'] == 2 :
                # change state of player2
                _type_ = temp_state.player2.new_build(buildings['pieceType'],
                                            buildings['pieceCoord'])
                labels.update_buildings(_type_)
            elif buildings['playernum'] == 3 :
                # change state of player3
                _type_ = temp_state.player3.new_build(buildings['pieceType'],
                                            buildings['pieceCoord'])
                labels.update_buildings(_type_)
            else:
                print("Error with player number")
                

        elif row["MessageType"] == "SOCMoveRobber":
            new_coord = hex(moveRobber(row))
            temp_state.place_robber(new_coord)
            # TO DO label true
        
        elif row["MessageType"] == "SOCDevCard":
            (playernum, actionType, cardType) = devCard(row)
            # update game state vector 
            # update card list of player that played
            # card_action returns 'bought' if player bought a card
            # card_action returns 'played' if player played a card
            # _action_ is used to make the label of the turn
            if playernum == 0:
                _action_= temp_state.player0.card_action(actionType, cardType)
                # update the labels
                if _action_=='bought': labels.bought_dev_card = True
                if _action_=='played': labels.played_dev_card = True
            elif playernum == 1:
                _action_= temp_state.player1.card_action(actionType, cardType)
                # update the labels
                if _action_=='bought': labels.bought_dev_card = True
                if _action_=='played': labels.played_dev_card = True
            elif playernum == 2:
                _action_= temp_state.player2.card_action(actionType, cardType)
                # update the labels
                if _action_=='bought': labels.bought_dev_card = True
                if _action_=='played': labels.played_dev_card = True
            elif playernum == 3:
                _action_= temp_state.player3.card_action(actionType, cardType)
                # update the labels
                if _action_=='bought': labels.bought_dev_card = True
                if _action_=='played': labels.played_dev_card = True
            else:
                print("Error with player number")
                
        # NOTE: SOCMakeOffer and SOCAcceptOffer are writen two times in 
        #       the logs 
        #           SOC*Offer
        #           SOCGameTextMsg (Server message)
        #           SOC*Offer (duplicate)
        #       but thank God no problem for me here :-)
        elif row["MessageType"] == "SOCMakeOffer":
            labels.made_offer = True
            
        elif row["MessageType"] == "SOCAcceptOffer":
            labels.traded_with_player = True
        else:
            # no action found
            # make true label no action
            # print('no action')
            pass

    
    # before returning labels check for no action
    labels.check_no_action()
    return (temp_state,labels,turn_chatsDF)

def putPiece(df):
    """ method to call for a SOCPutPiece message

    This method is called when a message of type SOCPutPiece is found in 
    the log. Updates the state of a player.
        
    Parameters
    ----------
    df: pandas dataframe
        The row of the game dataframe that holds SOCPutPiece messages 

    Returns
    -------
    building: dictionary
        Holds the player id, the type of piece he placed on the board and
        the coordinates where he placed it
    """
    
    # keep only the message field of the log
    # select all rows from column Message BUG
    # BUG FIXED message = df.loc[:, 'Message']
    #       we have only one row here
    message = df["Message"]
    
    # break message by |
    fields = message.split('|')
    # field[0] -> game=sth
    # field[1] -> playerNumber=sth
    # field[2] -> pieceType=num
    # field[3] -> coord=num  is in hex
    # OK print(x.split('|'))
    playernum = get_int_value(fields[1],'dec')
    pieceType = get_int_value(fields[2],'dec')
    pieceCoord = hex(get_int_value(fields[3],'hex'))
    
    return {'playernum':playernum, 'pieceType':pieceType,'pieceCoord': pieceCoord}
    
def moveRobber(df):
    """ method to call for a SOCMoveRobber message

    This method is called when a message of type SOCMoveRobber is found in 
    the log. Updates the position of the robber on the board.
        
    Parameters
    ----------
    df: pandas dataframe
        The row of the game dataframe that holds SOCPutPiece message

    Returns
    -------
    coord: hex int
        Hexadecimal coordinate on the board
    """
    # keep only the message field of the log
    # select all rows from column Message BUG
    # BUG FIXED message = df.loc[:, 'Message']
    #       we have only one row here
    message = df["Message"]
    
    # break message by |
    fields = message.split('|')
    # field[0] -> game=sth
    # field[1] -> playerNumber=sth
    # field[2] -> coord=num  is in hex but the 0x part is ommited....
    coord = get_int_value(fields[2],'hex')
    # TO CHECk: that the coordinate is returned correctly
    return coord

def playerElement(df):
    """ method to call for a SOCPlayerElement message

    This method is called when a message of type SOCPlayerElement is found
    in the log. Used to update the resources of a player
        
    Parameters
    ----------
    df: pandas dataframe
        The row of the game dataframe that holds SOCPlayerElement message 

    Returns
    -------
    playernum: player number
    actionType: Set, Gain or Loose a resource
    elementType: Type of the resource
    val: int
        
    """

    # keep only the message field of the log
    # select all rows from column Message BUG
    # BUG FIXED message = df.loc[:, 'Message']
    #       we have only one row here
    message = df["Message"]
    # OK print(message)
    
    # break message by |
    fields = message.split('|')
    # field[0] -> game=sth
    # field[1] -> playerNumber=sth
    # field[2] -> actionType=num   TO DO: write actiontype codes
    # field[3] -> elementType=num
    # field[4] -> value=num
    
    #OCPlayerElement:game=pilot01|playerNum=3|actionType=102|elementType=3|value=1    
    
    playernum = get_int_value(fields[1],'dec')
    actionType = get_int_value(fields[2],'dec')
    elementType = get_int_value(fields[3],'dec')
    val = get_int_value(fields[4],'dec')
    
    dic = { 'actionType' : actionType,
            'playernum' : playernum,
            'elementType' : elementType,
            'value' : val
            }
    # TO DO at get_state
    # for each action type call message of playerstate to update his 
    # resources accordingly
    # i.e. gained lost or has resources...
    # IMPORtant at get state check that we only care for resources
    # and not road, setm or other elementtypes
    return dic
    
def devCard(df):
    """ method to call for a SOCDevCard message

    This method is called when a message of type SOCDevCard is found
    in the log. Used to update the development cards of a player
        
    Parameters
    ----------
    df: pandas dataframe
        The row of the game dataframe that holds SOCDevCard message 

    Returns
    -------
    playernum: player number
    actionType: bought or played
    cardType: type of development card
        
    """

    # MESSAGE EXAMPLE 
    # SOCDevCard:game=pilot01|playerNum=1|actionType=0|cardType=0
    
    # keep only the message field of the log
    message = df["Message"]
    # OK print(message)
    
    # break message by |
    fields = message.split('|')
    # field[0] -> game=sth
    # field[1] -> playerNumber=sth
    # field[2] -> actionType=num   
    # field[3] -> cardType=num
    
    playernum = get_int_value(fields[1],'dec')
    actionType = get_int_value(fields[2],'dec')
    cardType = get_int_value(fields[3],'dec')
    
    return (playernum, actionType, cardType)
 
def get_chats0(df):
    """ method to save the chats of the initial setup phase to chatsDF
    
    Parameters
    ----------
    df: pandas dataframe
        The rows of the game dataframe that hold SOCGameTextMsg messages at 
        turn 0
    """  
    
    # keep only the message field of the log
    # select all rows from column Message
    messages = df.loc[:, 'Message']    
    #SOCGameTextMsg:game=pilot01|nickname=Dave|text=sorry
    
    # chatsDF within local scope (see ATTENTION below for more details)
    chat_columns = ["Turn", "emitter_nickname","text"]
    turn_chatsDF = pd.DataFrame(columns=chat_columns,index=None)
    
    for x in messages:
        # break message by |
        fields = x.split('|')
        # field[0] -> game=sth
        # field[1] -> nickname=sth
        # field[2] -> text=str
        nickname = fields[1][fields[1].find("=")+1:]
        chat_msg = fields[2][fields[2].find("=")+1:]
        
        # write to chatsDF
        # ATTENTION : watch out with the scope of the variables
        # anything done in get_chats0 stays in get_chats0
        # make a pandas DF in the same form as chatsDF 
        # return it 
        # then save it (append it) to the chatsDF
        
        # ignore the messages of the server
        if nickname != "Server":
            turn_chatsDF = turn_chatsDF.append({'Turn':0,
                                  'emitter_nickname':nickname,
                                  'text':chat_msg}, ignore_index=True)
    return turn_chatsDF

def get_chat(df):
    """ method to get a chat message of a SOCGameTextMsg
    
    Parameters
    ----------
    df: pandas dataframe
        The row of the game dataframe that holds a SOCGameTextMsg message
        
    Returns
    -------
    nickname : str
        The nickname of the emitter
    chat_msg : str
        The chat message emitted 
    """  
    
    # keep only the message field of the log
    message = df["Message"]
    
    #SOCGameTextMsg:game=pilot01|nickname=Dave|text=sorry
    # break message by |
    fields = message.split('|')
    # field[0] -> game=sth
    # field[1] -> nickname=sth
    # field[2] -> text=str
    nickname = fields[1][fields[1].find("=")+1:]
    chat_msg = fields[2][fields[2].find("=")+1:]
    return (nickname, chat_msg)
    
        
 
        
    
############################
# Running for files
############################

# Debugging
# seen_list = []
# PROBLEM WITH PILOT19, PILOT18
# Problem at get_board
for file in soclog_files:
    # read log
    # seen_list.append(file) # OK without pilot18 pilot19
    df = read_soclog(file)
    # find number of turns 
    # from the last row (df.tail(1) returns a df row) 
    # locate Turn attributre -> row 0, attribute Turn
    num_of_turns = df.tail(1).iloc[0]["Turn"]
    # send only turn 0 to initial setup state
    dfturn0 = df.loc[df.Turn == 0]
    (gamestate,chats0) = initial_setup_state(dfturn0)
    gamestatesDF.loc[0] = gamestate.write_to_DF()
    # OK gamestate.print_GameState()  # OK
    # NOTE: initial set up phase has no labels
    #   but for the NN... 
    #   write a labels with all false at turn 0
    labelsDF.loc[0] = Labels(0).write_to_DF()
    # append chats0 to the chatsDF
    chatsDF = chatsDF.append(chats0,ignore_index=True)

    for turn in range(1,num_of_turns+1):
        # find the logs of this turn
        df_of_turn = df.loc[df.Turn==turn]
        (gamestate,labels,chats) = get_state(df_of_turn, gamestate)
        # OK gamestate.print_GameState() # OK
        #OK labels.print_labels() # OK
        
        # save to pandas tables
        # write gamestate to gamestatesDF
        gamestatesDF.loc[turn] = gamestate.write_to_DF()
        # write labels to labelsDF
        labelsDF.loc[turn] = labels.write_to_DF()
        # write chats to chatsDF
        chatsDF = chatsDF.append(chats)
    
    
    # save to pickles
    #filename_parts = re.split(r'[/.]', file)
    # BUG FIX: SOME FILES USE . IN THE FILENAME
    #          split only on / and delete the last 7 chars of .soclog extension
    filename_parts = re.split(r'[/]', file)
    gamename = filename_parts[1]+"/"+filename_parts[2][:-7]
    gamestate_filename = "./DataTables/"+gamename+"_gamestates.pkl"
    labels_filename = "./DataTables/"+gamename+"_labels.pkl"
    chats_filename = "./DataTables/"+gamename+"_chats.pkl"
    #gamestatesDF.to_pickle("./pilot01_gamestates.pkl")
    #labelsDF.to_pickle("./pilot01_labels.pkl")
    gamestatesDF.to_pickle(gamestate_filename)
    labelsDF.to_pickle(labels_filename)
    chatsDF.to_pickle(chats_filename)
    
    # clear chatsDF dataframe
    # or else chats will be appended from the next file
    chatsDF = chatsDF.iloc[0:0]
    
    # clear gamestatesDF and labelsDF
    # or else rubbish from the previous soclogfile may remain 
    # in the last rows of the dataframe
    # in the case where the next game has fewer tuns that this one
    gamestatesDF = gamestatesDF.iloc[0:0]
    labelsDF = labelsDF.iloc[0:0]
    
