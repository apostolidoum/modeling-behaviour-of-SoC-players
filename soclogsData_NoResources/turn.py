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

""" Inserting the turn number to soclogs

Write new soclog files where the first field is the turn number.
Initial set up of the game is considered turn 0
When it is time for a new turn the SOCGameState sends a message
that the game state is state=15 
state=15 (PLAY, start a normal turn, time to roll or play card)
(for more information about states, their codes and meanings see SOCGame.java)
"""

import re #used to split line with multiple delimeters
from pathlib import Path


# the original soclog files
soclog_files = ["./soclogs/season2/League3Game1-2012-11-18-20-34-38-+0000.soclog",
"./soclogs/season2/Master League Game 3-2012-11-17-17-01-18-+0000.soclog",
"./soclogs/season2/League3Game4-2012-11-28-20-01-30-+0000.soclog",
"./soclogs/season2/Master league game 2-2012-11-13-18-07-14-+0000.soclog",
"./soclogs/season2/L5 Real game-2012-11-11-19-58-55-+0000.soclog",
"./soclogs/season2/Game 3-2012-11-25-20-09-16-+0000.soclog",
"./soclogs/season2/League8-2012-11-24-12-04-51-+0000.soclog",
"./soclogs/season2/Test-2012-10-16-14-53-15-+0100.soclog",
"./soclogs/season2/League4-2012-11-24-09-17-47-+0000.soclog",
"./soclogs/season2/League3Game5-2012-11-30-19-59-18-+0000.soclog",
"./soclogs/season2/Settles league 1-2012-11-08-18-05-34-+0000.soclog",
"./soclogs/season2/League 5 game 3-2012-11-26-00-51-20-+0000.soclog",
"./soclogs/season2/practice-2012-10-30-18-41-07-+0000.soclog",
"./soclogs/season2/league 5 last game-2012-12-09-21-08-39-+0000.soclog",
"./soclogs/season2/3version2-2012-11-21-20-23-31-+0000.soclog",
"./soclogs/season2/L5 practicegame-2012-11-11-19-26-36-+0000.soclog",
"./soclogs/season2/League4-2012-11-09-19-08-53-+0000.soclog",
"./soclogs/season2/Master League final-2012-12-05-16-59-57-+0000.soclog",
"./soclogs/season2/League 8 Game 2-2012-11-26-18-55-31-+0000.soclog",
"./soclogs/season2/league4_attempt2-2012-11-14-19-46-22-+0000.soclog",
"./soclogs/season2/SOCL League 5 Game 4-2012-12-03-02-11-10-+0000.soclog",
"./soclogs/season2/master league 4-2012-12-04-17-37-56-+0000.soclog",
"./soclogs/season2/SOCL League 5 Game 2-2012-11-25-17-25-09-+0000.soclog",
"./soclogs/season1/league3practice-2012-05-31-19-23-46-+0100.soclog",
"./soclogs/season1/league2.2-2012-06-18-20-50-12-+0100.soclog",
"./soclogs/season1/league 3 (-k)-2012-06-25-18-22-53-+0100.soclog",
"./soclogs/season1/League 2-2012-06-26-20-23-20-+0100.soclog",
"./soclogs/season1/League 1 game-2012-06-19-18-49-00-+0100.soclog",
"./soclogs/season1/league3-2012-05-27-19-53-48-+0100.soclog",
"./soclogs/season1/League2-2012-06-17-19-58-07-+0100.soclog",
"./soclogs/season1/League 1-2012-06-17-19-53-24-+0100.soclog",
"./soclogs/season1/league3minus1-2012-05-25-22-22-21-+0100.soclog",
"./soclogs/season1/League 3 Finale-2012-06-25-21-57-53-+0100.soclog",
"./soclogs/season1/3-2012-06-06-19-58-56-+0100.soclog",
"./soclogs/season1/League 1.1-2012-06-21-18-58-22-+0100.soclog",
"./soclogs/season1/league1 31may-2012-05-31-19-59-37-+0100.soclog",
"./soclogs/season1/League 1.2-2012-06-21-20-27-05-+0100.soclog",
"./soclogs/season1/league3 michael-2012-06-17-20-54-03-+0100.soclog",
"./soclogs/season1/League2.4-2012-06-26-22-47-04-+0100.soclog",
"./soclogs/pilot/pilot15-2011-10-28-09-54-56-+0100.soclog",
"./soclogs/pilot/pilot19-2011-10-31-15-56-37-+0000.soclog",
"./soclogs/pilot/pilot17-2011-10-27-11-55-04-+0100.soclog",
"./soclogs/pilot/pilot12-2011-10-26-13-52-29-+0100.soclog",
"./soclogs/pilot/pilot09-2011-10-21-15-57-13-+0100.soclog",
"./soclogs/pilot/pilot06-2011-10-20-10-06-38-+0100.soclog",
"./soclogs/pilot/pilot11-2011-10-24-15-56-26-+0100.soclog",
"./soclogs/pilot/pilot16-2011-10-27-10-07-18-+0100.soclog",
"./soclogs/pilot/pilot18-2011-10-28-15-54-36-+0100.soclog",
"./soclogs/pilot/pilot20-2011-10-31-16-16-29-+0000.soclog",
"./soclogs/pilot/pilot21-2011-10-31-15-58-38-+0000.soclog",
"./soclogs/pilot/pilot02-2011-10-12-13-38-43-+0100.soclog",
"./soclogs/pilot/pilot13-2011-10-24-15-56-42-+0100.soclog",
"./soclogs/pilot/pilot14-2011-10-25-09-54-06-+0100.soclog",
"./soclogs/pilot/pilot10-2011-10-21-15-57-22-+0100.soclog",
"./soclogs/pilot/pilot08-2011-10-21-13-57-25-+0100.soclog",
"./soclogs/pilot/pilot07-2011-10-21-10-01-31-+0100.soclog",
"./soclogs/pilot/pilot05-2011-10-19-15-53-07-+0100.soclog",
"./soclogs/pilot/pilot03-2011-10-19-16-30-51-+0100.soclog",
"./soclogs/pilot/pilot01-2011-10-10-15-28-56-+0100.soclog",
"./soclogs/pilot/pilot04-2011-10-19-15-52-57-+0100.soclog"]


# destinations for the extended soclog files
# that are created from add_turns
extended_soclog_files = ["./extended/season2/League3Game1-2012-11-18-20-34-38-+0000.soclog",
"./extended/season2/Master League Game 3-2012-11-17-17-01-18-+0000.soclog",
"./extended/season2/League3Game4-2012-11-28-20-01-30-+0000.soclog",
"./extended/season2/Master league game 2-2012-11-13-18-07-14-+0000.soclog",
"./extended/season2/L5 Real game-2012-11-11-19-58-55-+0000.soclog",
"./extended/season2/Game 3-2012-11-25-20-09-16-+0000.soclog",
"./extended/season2/League8-2012-11-24-12-04-51-+0000.soclog",
"./extended/season2/Test-2012-10-16-14-53-15-+0100.soclog",
"./extended/season2/League4-2012-11-24-09-17-47-+0000.soclog",
"./extended/season2/League3Game5-2012-11-30-19-59-18-+0000.soclog",
"./extended/season2/Settles league 1-2012-11-08-18-05-34-+0000.soclog",
"./extended/season2/League 5 game 3-2012-11-26-00-51-20-+0000.soclog",
"./extended/season2/practice-2012-10-30-18-41-07-+0000.soclog",
"./extended/season2/league 5 last game-2012-12-09-21-08-39-+0000.soclog",
"./extended/season2/3version2-2012-11-21-20-23-31-+0000.soclog",
"./extended/season2/L5 practicegame-2012-11-11-19-26-36-+0000.soclog",
"./extended/season2/League4-2012-11-09-19-08-53-+0000.soclog",
"./extended/season2/Master League final-2012-12-05-16-59-57-+0000.soclog",
"./extended/season2/League 8 Game 2-2012-11-26-18-55-31-+0000.soclog",
"./extended/season2/league4_attempt2-2012-11-14-19-46-22-+0000.soclog",
"./extended/season2/SOCL League 5 Game 4-2012-12-03-02-11-10-+0000.soclog",
"./extended/season2/master league 4-2012-12-04-17-37-56-+0000.soclog",
"./extended/season2/SOCL League 5 Game 2-2012-11-25-17-25-09-+0000.soclog",
"./extended/season1/league3practice-2012-05-31-19-23-46-+0100.soclog",
"./extended/season1/league2.2-2012-06-18-20-50-12-+0100.soclog",
"./extended/season1/league 3 (-k)-2012-06-25-18-22-53-+0100.soclog",
"./extended/season1/League 2-2012-06-26-20-23-20-+0100.soclog",
"./extended/season1/League 1 game-2012-06-19-18-49-00-+0100.soclog",
"./extended/season1/league3-2012-05-27-19-53-48-+0100.soclog",
"./extended/season1/League2-2012-06-17-19-58-07-+0100.soclog",
"./extended/season1/League 1-2012-06-17-19-53-24-+0100.soclog",
"./extended/season1/league3minus1-2012-05-25-22-22-21-+0100.soclog",
"./extended/season1/League 3 Finale-2012-06-25-21-57-53-+0100.soclog",
"./extended/season1/3-2012-06-06-19-58-56-+0100.soclog",
"./extended/season1/League 1.1-2012-06-21-18-58-22-+0100.soclog",
"./extended/season1/league1 31may-2012-05-31-19-59-37-+0100.soclog",
"./extended/season1/League 1.2-2012-06-21-20-27-05-+0100.soclog",
"./extended/season1/league3 michael-2012-06-17-20-54-03-+0100.soclog",
"./extended/season1/League2.4-2012-06-26-22-47-04-+0100.soclog",
"./extended/pilot/pilot15.soclog",
"./extended/pilot/pilot19.soclog",
"./extended/pilot/pilot17.soclog",
"./extended/pilot/pilot12.soclog",
"./extended/pilot/pilot09.soclog",
"./extended/pilot/pilot06.soclog",
"./extended/pilot/pilot11.soclog",
"./extended/pilot/pilot16.soclog",
"./extended/pilot/pilot18.soclog",
"./extended/pilot/pilot20.soclog",
"./extended/pilot/pilot21.soclog",
"./extended/pilot/pilot02.soclog",
"./extended/pilot/pilot13.soclog",
"./extended/pilot/pilot14.soclog",
"./extended/pilot/pilot10.soclog",
"./extended/pilot/pilot08.soclog",
"./extended/pilot/pilot07.soclog",
"./extended/pilot/pilot05.soclog",
"./extended/pilot/pilot03.soclog",
"./extended/pilot/pilot01.soclog",
"./extended/pilot/pilot04.soclog"]


def add_turns(inputfile,outputfile):
    """ Adds the turn number to the data
    
    Reads an original soclog file and inserts the turn number at the
    beggining of each log.
    The new, extended soclog is saved as a new soclog file
    
    Parameters
    ----------
    inputfile: file
        The original soclog file to be modified
    outputfile: file
        The destination where the new soclogfile will be written 
    """

    turn = 0 
    with open(inputfile,'r') as file:
        with open(outputfile,'w') as destfile:
            lines = file.readlines()
            for line in lines:
                
                #split on 2 delimeters :|
                words = re.split(r'[|:]', line)
                #print(words)
                # when the game state in the log is 15
                # it is time for a player to start his turn
                # time to roll the dice of play a card
                if 'state=15\n' in words:
                    turn +=1
                    
                # write turn: at the beggining of the line and save to destfile
                destfile.write(str(turn)+':'+line)
            
 
# make directories to save the results
extended_dir = Path.cwd() / "extended/season2" 
extended_dir.mkdir(parents=True, exist_ok=True)

extended_dir = Path.cwd() / "extended/season1" 
extended_dir.mkdir(parents=True, exist_ok=True)

extended_dir = Path.cwd() / "extended/pilot" 
extended_dir.mkdir(parents=True, exist_ok=True)
 
# run for every soclog       
for soclog,new_soclog in zip(soclog_files,extended_soclog_files):  
    add_turns(soclog,new_soclog)
            
    
    
