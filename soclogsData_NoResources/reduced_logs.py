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

""" Collecting the useful data from the soclogs

Selects the useful messages from the soclogs
to extract the informations needed for the state features.
SOCGameTextMsg, GAME-TEXT-MESSAGE, SOCGameState
"""

import pandas as pd
import csv


# list of all the soclogs files locations
soclog_files = [ "extended/pilot/pilot20.soclog",
                 "extended/pilot/pilot04.soclog",
                 "extended/pilot/pilot19.soclog",
                 "extended/pilot/pilot08.soclog",
                 "extended/pilot/pilot10.soclog",
                 "extended/pilot/pilot12.soclog",
                 "extended/pilot/pilot07.soclog",
                 "extended/pilot/pilot18.soclog",
                 "extended/pilot/pilot15.soclog",
                 "extended/pilot/pilot21.soclog",
                 "extended/pilot/pilot01.soclog",
                 "extended/pilot/pilot06.soclog",
                 "extended/pilot/pilot05.soclog",
                 "extended/pilot/pilot03.soclog",
                 "extended/pilot/pilot13.soclog",
                 "extended/pilot/pilot17.soclog",
                 "extended/pilot/pilot09.soclog",
                 "extended/pilot/pilot02.soclog",
                 "extended/pilot/pilot16.soclog",
                 "extended/pilot/pilot11.soclog",
                 "extended/pilot/pilot14.soclog",
                 "extended/season2/League 8 Game 2-2012-11-26-18-55-31-+0000.soclog",
                 "extended/season2/Master League final-2012-12-05-16-59-57-+0000.soclog",
                 "extended/season2/League4-2012-11-09-19-08-53-+0000.soclog",
                 "extended/season2/Game 3-2012-11-25-20-09-16-+0000.soclog",
                 "extended/season2/Master League Game 3-2012-11-17-17-01-18-+0000.soclog",
                 "extended/season2/League4-2012-11-24-09-17-47-+0000.soclog",
                 "extended/season2/master league 4-2012-12-04-17-37-56-+0000.soclog",
                 "extended/season2/SOCL League 5 Game 2-2012-11-25-17-25-09-+0000.soclog",
                 "extended/season2/League3Game5-2012-11-30-19-59-18-+0000.soclog",
                 "extended/season2/league 5 last game-2012-12-09-21-08-39-+0000.soclog",
                 "extended/season2/3version2-2012-11-21-20-23-31-+0000.soclog",
                 "extended/season2/League 5 game 3-2012-11-26-00-51-20-+0000.soclog",
                 "extended/season2/League8-2012-11-24-12-04-51-+0000.soclog",
                 "extended/season2/Test-2012-10-16-14-53-15-+0100.soclog",
                 "extended/season2/L5 practicegame-2012-11-11-19-26-36-+0000.soclog",
                 "extended/season2/league4_attempt2-2012-11-14-19-46-22-+0000.soclog",
                 "extended/season2/Master league game 2-2012-11-13-18-07-14-+0000.soclog",
                 "extended/season2/SOCL League 5 Game 4-2012-12-03-02-11-10-+0000.soclog",
                 "extended/season2/L5 Real game-2012-11-11-19-58-55-+0000.soclog",
                 "extended/season2/League3Game1-2012-11-18-20-34-38-+0000.soclog",
                 "extended/season2/Settles league 1-2012-11-08-18-05-34-+0000.soclog",
                 "extended/season2/League3Game4-2012-11-28-20-01-30-+0000.soclog",
                 "extended/season2/practice-2012-10-30-18-41-07-+0000.soclog",
                 "extended/season1/league3minus1-2012-05-25-22-22-21-+0100.soclog",
                 "extended/season1/league 3 (-k)-2012-06-25-18-22-53-+0100.soclog",
                 "extended/season1/League 1 game-2012-06-19-18-49-00-+0100.soclog",
                 "extended/season1/League2.4-2012-06-26-22-47-04-+0100.soclog",
                 "extended/season1/league3-2012-05-27-19-53-48-+0100.soclog",
                 "extended/season1/League 1-2012-06-17-19-53-24-+0100.soclog",
                 "extended/season1/league2.2-2012-06-18-20-50-12-+0100.soclog",
                 "extended/season1/3-2012-06-06-19-58-56-+0100.soclog",
                 "extended/season1/League 1.1-2012-06-21-18-58-22-+0100.soclog",
                 "extended/season1/League 3 Finale-2012-06-25-21-57-53-+0100.soclog",
                 "extended/season1/League 2-2012-06-26-20-23-20-+0100.soclog",
                 "extended/season1/league3practice-2012-05-31-19-23-46-+0100.soclog",
                 "extended/season1/League2-2012-06-17-19-58-07-+0100.soclog",
                 "extended/season1/League 1.2-2012-06-21-20-27-05-+0100.soclog",
                 "extended/season1/league1 31may-2012-05-31-19-59-37-+0100.soclog",
                 "extended/season1/league3 michael-2012-06-17-20-54-03-+0100.soclog"]


# list of all the destination files 
# where the useful data collected from the soclogs will be stored
r_soclog_files = ["reduced/pilot/pilot20.soclog",
                  "reduced/pilot/pilot04.soclog",
                  "reduced/pilot/pilot19.soclog",
                  "reduced/pilot/pilot08.soclog",
                  "reduced/pilot/pilot10.soclog",
                  "reduced/pilot/pilot12.soclog",
                  "reduced/pilot/pilot07.soclog",
                  "reduced/pilot/pilot18.soclog",
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


def read_soclog(soclogfile):
    """ Reads a soclog and separates basic columns
    
    Read a soclog and separates columns by ':'
    The first 8 columns are the timestamp, when the message was sent
    The 9th column is the MessageType
    (for details about MessageTypes see /messages of jSettlers)
    The 10th column is the Message
        
    Parameters
    ----------
    soclogfile: file
        The soclog .soclog file
            
    Returns
    -------
    soclog: dataframe 
        the soclog in dataframe form
    """
    
    column_names = ["Turn","Year","Month","Day","Hour","Minute","Second","unk1","unk2", "MessageType","Message"]
    soclog = pd.read_csv(soclogfile, sep = ":",header = None, names = column_names)
    return soclog



def reduce_log(soclog):
    """ Creates a dataframe that contains only the useful parts of the logs
    
    Creates a dataframe that contains only rows of MessageType
    SOCGameTextMsg | GAME-TEXT-MESSAGE | SOCGameState.
    Deletes the timestamp from the row.
    Saves to a csv using the '|' as delimeter
    
    Parameters
    ----------
    soclog: dataframe
        The dataframe of a soclog (as returned from read_soclog)
        
    Returns
    -------
    data: dataframe
        A dataframe with the useful data (rows) collected from the soclog
    """

    # SOCSetPlayedDevCard is problematic (writtend multiple times within a 
    # turn) and unnecessary (same info can be retrieved from SOCDevCard)

    rows = soclog["MessageType"].isin({"SOCSitDown","SOCBoardLayout",
                 "SOCMoveRobber", "SOCPutPiece", 
                 "SOCDevCard",
                 "SOCMakeOffer", "SOCAcceptOffer",
                 "SOCGameTextMsg"})
    columns = ['Turn','MessageType','Message']
    data = soclog.loc[rows,columns]
    return data


def write_to_csv(data,filename,delimiter):
    """ Writes a dataframe to a csv file
    
    Parameters
    ----------
    data: dataframe
        The dataframe to be written to the csv file
    filename: file
        The destination file
    delimeter: str
        The separator two put between fields in the csv (e.g. '|', ':')
    """
    
    # csv.QUOTE_NONE, escapecha are used  to avoid double quotes
    # when writing the Message field of the dataframe
    # So that in the future i can use only '|' as a delimeter
    # and extract other fields from the Message field
    # CAVEAT: adds extra spaces 
    # BUGFIXED : Because the csv rows have different #columns
    #            i actually need the 2 delimeters.
    #            I break the data into columns Turn, MessageType, Message
    #               using del :
    #            And then break futher down the Message using del |
    # NOTE : When using del | the message is saved with quotes
    #        When saving with del : no such problem hence quote_none is only 
    #           needed when saving with del |
    data.to_csv(filename, header=None, index=None, sep=delimiter)
                #quoting=csv.QUOTE_NONE, escapechar=' ')

# run for every soclog
for soclog, r_log in zip(soclog_files,r_soclog_files):
    data = reduce_log(read_soclog(soclog))
    write_to_csv(data,r_log,delimiter = ':')
