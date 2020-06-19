#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To debugg the renaming of the files
cause one file gets lost due to use of . in the file name
FOR GODS SAKE!
WHO USES . IN THE NAME OF A FILE?!?!?!?
if you use rubbish data you get rubbish results


Created on Wed Nov 27 21:23:14 2019

@author: maria
"""


import re

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

gamenames = []
for file in soclog_files:
    filename_parts = re.split(r'[/]', file)
    gamename = filename_parts[1]+"/"+filename_parts[2][:-7]
    gamenames.append(gamename)
    gamestate_filename = "./DataTables/"+gamename+"_gamestates.pkl"
    labels_filename = "./DataTables/"+gamename+"_labels.pkl"
    chats_filename = "./DataTables/"+gamename+"_chats.pkl"
    