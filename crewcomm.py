# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 18:01:01 2019
CrewComm - Communicate with crew members... poorly.
Note: I am very tempted to make this more sophisticated.
Note: * is now used in keywords files to indicate multi-word terms.
@author: Nuke Bloodaxe
"""

import io, pygame, random, global_constants as g, crew

CrewKeywords = {} #crewmember{}->Keyword->{event:reponse code,runtime event,list treatment-single/multiline etc}

CrewReplies = {} #crewmember{}->Key Respose Code->[responses]

#dictionary of key words->check event codes->check response requirement
#->pick response from list 

#Dictionary of replies, index by reponse code.  Contains lists.

class crewComm(object):
    def __init__(self, shipCrew):
        self.crewMembers = shipCrew
        self.selectedCrew = 0 #nobody
        #Prepare background image
        self.charCom = pygame.image.load("Graphics_Assets\\charcom.png")
        self.charComScaled = pygame.transform.scale(self.charCom,(g.width,g.height))
        self.musicState = False
        
    def update(self, displaySurface):
        return self.communicate(displaySurface)

    #Compare the keyword against all event entries and check to see which
    #flags have been tripped, return the reply entry matching the highest
    #tripped flag number.
    def checkKeywordEventFlags(self, keyword = ""):
        
        pass
    
    #Parse the string of text looking for keywords present in the crewKeywords
    #Dictionary.  Returns a reply based on the best event flag for the text.
    def textInterpret(self, text=""):
        tokenisedText = text.split()
        pass
    
    def communicate(self,displaySurface):
        displaySurface.blit(self.charComScaled,(0,0)) # Set background.
        #Start main intro music
        if self.musicState == False:
            pygame.mixer.music.load("sound\\CREWCOMM.OGG")
            pygame.mixer.music.play()
            self.musicState = True
        return 6 # TODO, currently loops communication system for testing.



#load all crew comversation related data.
#file location and prefix, Number of files(file number), extension.
#Note: We have some advantages with the reposnse lines, as they are written
#to the crew terminal character by character, we can take advantage of the
#data formatting codes dynamically.
def loadCrewCommunications(file="Data_Generators\Other\crewcon",count=6,extension=".tab"):
    
    for index in range(1,count+1):
        commFile = io.open(file+str(index)+extension, "r")
        commDataString = []
        keyWords = []
        #commResponseString = [""]
        CrewKeywords[index] = {}
        CrewReplies[index] = {}
        temp = [""]
        while temp[0] != "ENDF":
            commDataString = (commFile.readline().split('\n')[0]).split('\t') #Data Line
            #print(commDataString) # for debug.
            keyWords = commDataString[4].split('*')
            for word in keyWords:
                try:
                    CrewKeywords[index][word][commDataString[0]] = [commDataString[1],
                                                                    commDataString[2],
                                                                    commDataString[3]]
                except:
                    CrewKeywords[index][word] = {}
                
                CrewKeywords[index][word][commDataString[0]] = [commDataString[1],
                                                                commDataString[2],
                                                                commDataString[3]]
            temp = (commFile.readline().split('\n')[0]).split('\t')
            while temp[0] != "EOD" and temp[0] != "ENDF":
                try:
                    CrewReplies[index][temp[0]]
                except:
                    CrewReplies[index][temp[0]] = []
                CrewReplies[index][temp[0]].append(temp[1])
                temp = (commFile.readline().split('\n')[0]).split('\t')
            
        # A crewmember's responses have now been loaded.

        commFile.close()