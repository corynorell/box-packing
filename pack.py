#!/usr/bin/env python
import csv
import sys
import optparse

###############################################
# CLASSES
###############################################

class Box:
    def __init__(self, volume, id, itemGroup = ''):
        self.items = []
        self.id = int(id)
        self.volume = volume
        self.usedSpace = 0
        self.itemGroup = itemGroup

    def addItem(self, item):
        self.items.append(item)
        self.usedSpace += item.volume

    def listItems(self, groupItems):
        itemIds = []

        for item in self.items:
            itemIds.append(item.id)

        if groupItems:
            print "Box %s (Group %s) contains the following items: %s" % (self.id, self.itemGroup, itemIds)
        else:
            print "Box %s contains the following items: %s" % (self.id, itemIds)


class Item:
    def __init__(self, id, group, volume):
        self.id = id
        self.group = group
        self.volume = float(volume)


###############################################
# FUNCTIONS
###############################################

def parseArgs():
    global options

    parser = optparse.OptionParser()

    parser.add_option("-f", "--file", default="items.csv", type="string", metavar="<csv-file>", help="The CSV file containing items to be packed.")
    parser.add_option("-v", "--volume", default=1.58, type="float", metavar="<box-volume>", help="The storage capacity (volume) of each box.")
    parser.add_option("-r", "--returnBoxes", default=False, action="store_true", help="If set, returns the list of packed boxes instead of printing result.")
    parser.add_option("-g", "--group", default=False, action="store_true", help="If set, restricts the boxes to one group of items per box.")

    (options, args) = parser.parse_args()

    if not options.file:
        parser.error("Please specify a CSV file to be parsed.")

    return options
    

def pack(itemList, boxVolume, returnBoxes = False, groupItems = False):
    '''Pack specified items into boxes

    Keyword Arguments:
    
    itemList    -- list of items to be packed into boxes
    boxVolume   -- volume constraint of every box
    returnBoxes -- return box list instead of printing relevant data
    '''

    itemList = generateList(itemList)

    boxes = []
    boxCount = 1

    for item in itemList:
        itemVolume = float(item.volume)

        for box in boxes:
            spaceToBeUsed = box.usedSpace + itemVolume
            if (spaceToBeUsed <= box.volume):
                if groupItems:
                    if item.group == box.itemGroup:
                        box.addItem(item)
                        break
                else:
                    box.addItem(item)
                    break
        else:
            # Item didn't fit into any existing box, start another
            if groupItems:
                newBox = Box(boxVolume, boxCount, item.group)
            else:
                newBox = Box(boxVolume, boxCount)
            newBox.addItem(item)
            boxes.append(newBox)
            boxCount += 1

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

    for box in boxes:
        box.listItems(groupItems)

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
        sys.exit(1)


###############################################
# ENTRY POINT
###############################################
options = parseArgs()
boxes = pack(options.file, options.volume, options.returnBoxes, options.group)

sys.exit(0)
