# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:32:51 2019
Item Datastructures
@author: Nuke Bloodaxe
"""
import io

itemDictionary = {}
itemConstructionDictionary = {}

#Base object parameters.
class Item(object):
    def __init__(self, name, cargoSize, worth, levels):
        self.name = name
        self.cargoSize = cargoSize
        self.worth = worth
        self.levels = levels #These appear to be the level requirements
                             #for each type of crew member. [6 crew, 6 levels.]
        #[psychometry, engineering, science, security, astrogation, medical]
        self.description #Item description.

# This data should be added to a dictionary, by name, on load.
#By tradition, the Iron Seed three items requirement is used.
class createItem(Item):
    def __init__(self, name, cargoSize, worth, levels, part1, part2, part3):
        self.part1 = part1
        self.part2 = part2
        self.part3 = part3
        Item.__init__(self,name,cargoSize,worth,levels)

#Populate the item and item construction dictionaries.
#we load from two different data files to do this, tab delimited.
#Data Order: Name, cargosize, worth, part1, part2, part3, levels
def loadItemData(file1="Data_Generators\Other\IronPy_items.tab",
                 file2="Data_Generators\Other\IronPy_itemdata.tab",
                 file3="Data_Generators\Other\IronPy_iteminfo.tab"):
    itemFile = io.open(file1, "r")
    itemString = itemFile.readline() #title line
    itemString = itemFile.readline() #spacer line
    itemString = itemFile.readline() #real data
    constructFile = io.open(file2, "r")
    constString = constructFile.readline() #title line
    constString = constructFile.readline() #spacer line
    constString = constructFile.readline() #real data    
    iteminfoFile = io.open(file3, "r")
    iteminfoString = iteminfoFile.readline() # immediate real data
    S1 = itemString #used plenty, so must be short, is read string from file.
    S2 = constString #Used plenty, so must be short, is read string from file.
    S3 = iteminfoString #Used plenty, so must be short, is read string from file.
    
    while S2 != "":
        decodedConst = S2.split('\t')
        temp = [] # remove the \n and make elements ints.
        for integer in decodedConst[5:]:
            if integer != '\n':
                temp.append(int(integer))
        itemConstructionDictionary[decodedConst[0]] = [decodedConst[0],
                                                       decodedConst[1],
                                                       decodedConst[2],
                                                       decodedConst[3],
                                                       int(decodedConst[4]),
                                                       temp]
        S2 = constructFile.readline()
        
    while S1 != "":
        decodedItem = S1.split('\t')
        dump = decodedItem[1].split('\n') # removing newline
        decodedItem[1] = int(dump[0])
        try:
            itemDictionary[decodedItem[0]] = [decodedItem[0],
                                              decodedItem[1],
                                              itemConstructionDictionary[decodedItem[0]][4],
                                              itemConstructionDictionary[decodedItem[0]][5]]
        except KeyError:
            #We don't care about missing items.
            #We set these up as singular instances.
            try:
                itemDictionary[decodedItem[0]] = [decodedItem[0],
                                                  decodedItem[1],
                                                  0,[1,1,1,1,1,1]]
            except:
                print("Tried Key:", decodedItem[0])
                #Usually indicates the file we are loading is incorrectly
                #formatted.  If you are modding, double-check your tabs.
                print("Absolutely fatal error on creating items")    
            
        S1 = itemFile.readline()
    
    while S3 != "ENDF":
        itemName = S3.split('\n')[0]
        S3 = iteminfoFile.readline().split('\n')[0]
        itemDescription = []
        while S3 != "EOD" and S3 != "ENDF":
            itemDescription.append(S3)
            S3 = iteminfoFile.readline().split('\n')[0]
        try:
            itemDictionary[itemName].append(itemDescription)
        except KeyError:
            print("Tried Key:", itemName)
            #Usually indicates the file we are loading is incorrectly
            #formatted.  If you are modding, double-check your item
            #files, as you may have a spelling mistake in the key names.
            print("Absolutely fatal error on adding item description.")    
        
        # An Item Description has now been loaded.
        S3 = iteminfoFile.readline()
    
    itemFile.close()
    constructFile.close()
    iteminfoFile.close()