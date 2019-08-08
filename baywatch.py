"""
1. convert input to array of Lifeguard nodes
2. sort array by shift start times
3. Find the least productive lifeguard and remove them 
5. Iterate over modified array and add to total, keeping in mind overlapping intervals
===============================
Author: Philip Chwistek
"""

class LifeguardNode:
    def __init__(self, start, end):
        self.shift = [start, end]
        self.aloneStart = start
        self.aloneEnd = end
        self.totalAlone = end - start
        self.redundant = False

    def updateTotal(self):
        self.totalAlone = self.aloneEnd - self.aloneStart if self.aloneEnd - self.aloneStart >= 0 else 0

    def makeRedundant(self):
        self.redundant = True
        self.aloneStart = 0
        self.aloneEnd = 0
        self.totalAlone = 0

    def updateAloneStart(self, aloneStart):
        self.aloneStart = aloneStart
        self.updateTotal()

    def updateAloneEnd(self, aloneEnd):
        self.aloneEnd = aloneEnd
        self.updateTotal()

    def __repr__(self):
        return "{}-{}".format(self.shift[0], self.shift[1])

def readFileInput(pathToFile):
    reader = open(pathToFile, "r")
    contents = reader.readlines()
    output = []
    i = 0
    for line in contents:
        editedLine = line.rstrip("\n")
        spaceIndex = editedLine.find(' ')
        if spaceIndex > -1:
            rangeValues = editedLine.split(' ')
            newNode = LifeguardNode(int(rangeValues[0]), int(rangeValues[1]))
            newNode.index = i
            output.append(newNode)
            i += 1

    reader.close()
    output.sort(key=lambda x: x.shift[0]) # sort by time starting shift 
    return output

def output(outputFile, totalHours):
    f = open(outputFile, "w+")
    f.write(str(totalHours))
    f.close()

def findMinLifeguard(sortedInput):
    
    def checkRedundancy(firstNode, otherNode): ## checks whether Lifeguard's shift is entirely covered by another
        if firstNode.aloneStart <= otherNode.aloneStart and firstNode.aloneEnd >= otherNode.aloneEnd:
            otherNode.makeRedundant()
            return True
        return False

    minNode = sortedInput[0]
    minIndex = 0

    for index, currentNode in enumerate(sortedInput):
        nextIndex = index
        nextNode = None

        if index + 1 < len(sortedInput):
            nextIndex += 1
            nextNode = sortedInput[nextIndex]

        while nextNode != None:
            if currentNode.aloneEnd < nextNode.aloneStart: # ex [x, 4], [5, y]
                break
            elif currentNode.aloneEnd > nextNode.aloneStart: # ex [x, 4], [3, y]
                nextNodeRedundant = checkRedundancy(currentNode, nextNode)
                currentNodeRedundant = checkRedundancy(nextNode, currentNode)
                if nextNodeRedundant: # ex [x, 10], [x, 4]
                    return nextIndex
                elif currentNodeRedundant: # ex [x, 4], [x, 10]
                    return index
                else:
                    temp = nextNode.aloneStart
                    nextNode.updateAloneStart(currentNode.aloneEnd)
                    currentNode.updateAloneEnd(temp)
            
                    if currentNode.totalAlone < minNode.totalAlone:
                        minNode = currentNode
                        minIndex = index
                    elif nextNode.totalAlone < minNode.totalAlone:
                        minNode = nextNode
                        minIndex = nextIndex

                if nextIndex + 1 > len(sortedInput):
                    nextNode = sortedInput[nextIndex + 1]
                else:
                    break

    return minIndex


def findMaxHours(inputFile):
    sortedInput = readFileInput(inputFile)  # read in and sort by time starting (n * nlogn)
    minLifeguardIndex = findMinLifeguard(sortedInput) # find lifeguard to fire... m (interval length) ... n * m

    totalHours = 0
    intervalStart = sortedInput[0].shift[0]
    intervalEnd = sortedInput[0].shift[1]

    minLifeguard = sortedInput.pop(minLifeguardIndex) 

    for index, node in enumerate(sortedInput):
        if node.shift[0] < intervalEnd and node.shift[1] > intervalEnd:
            intervalEnd = node.shift[1]
        elif node.shift[0] > intervalEnd:
            totalHours += intervalEnd - intervalStart
            intervalStart = node.shift[0]
            intervalEnd = node.shift[1]

        if index + 1 == len(sortedInput) and intervalEnd >= node.shift[1]:
            totalHours += intervalEnd - intervalStart

    return totalHours

for i in range(10):
    totalHours  = findMaxHours('./input/' + str(i + 1) + '.in')
    output('./output/' + str(i + 1) + '.out', totalHours)

