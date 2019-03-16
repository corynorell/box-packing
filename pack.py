#!/usr/bin/env python
import csv
import sys

# These would typically be parsed as options
boxVolume = 1.58 
csvFile = 'items.csv'

###############################################
# CLASSES
###############################################

class Box:
    def __init__(self, volume):
        self.items = []
        self.volume = volume
        self.usedSpace = 0

    def addItem(self, item):
        itemVolume = float(item.volume)

        self.items.append(item)
        self.usedSpace += itemVolume


class Item:
    def __init__(self, id, group, volume):
        self.id = id
        self.group = group
        self.volume = volume


###############################################
# FUNCTIONS
###############################################

def pack(itemList, boxVolume, returnBoxes = False):
    '''Pack specified items into boxes

    Keyword Arguments:
    
    itemList    -- list of items to be packed into boxes
    boxVolume   -- volume constraint of every box
    returnBoxes -- return box list instead of printing relevant data 
    '''

    boxes = []
    initialBox = Box(boxVolume)
    boxes.append(initialBox)

    for item in itemList:
        itemVolume = float(item.volume)

        for box in boxes:
            spaceToBeUsed = box.usedSpace + itemVolume
            if (spaceToBeUsed <= box.volume):
                box.addItem(item)
                break
        else:
            # Item didn't fit into any existing box, start another
            newBox = Box(boxVolume)
            newBox.addItem(item)
            boxes.append(newBox)

    if returnBoxes:
        # Do any desired post processing (json encode) and return
        return boxes
    else:
        
        efficiencyTotal = 0
        totalBoxes = len(boxes)

        for box in boxes:
            efficiency = box.usedSpace / box.volume
            efficiencyTotal += efficiency

        averageEfficiency = efficiencyTotal / len(boxes) * 100

        print "Boxes needed: %s | Average efficiency achieved: %s %%" % (totalBoxes, averageEfficiency)

def generateList(csvFile):
    '''Read specified CSV file and convert to list of objects

    Keyword Arguments:

    csvFile -- csv file to be read and converted, contains items to be packed
    '''

    itemsList = []

    try:
        with open(csvFile) as csvList:
            items = csv.DictReader(csvList)

            for item in items:
                itemId = item['item_id']
                itemGroup = item['item_group']
                itemVolume = item['cubic_volume_ft']
                newItem = Item(itemId, itemGroup, itemVolume)
                itemsList.append(newItem)

        # Catch empty lists
        if not itemsList:
            print "No items found in specified file. Please ensure file name is correct."
            sys.exit(1)

        # Sort by size (descending) for slight optimization
        itemsList = sorted(itemsList, key=lambda item: item.volume, reverse=True)
        return itemsList
    
    # Catch incorrect file name
    except IOError:
        print 'The specified file was not found.'


###############################################
# ENTRY POINT
###############################################

itemList = generateList(csvFile)

boxes = pack(itemList, boxVolume)