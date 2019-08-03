"""
insert pseduo code here


===============================
Author: Philip Chwistek
"""

class LifeguardNode:
    def __init__(self, start, end):
        self.shift = [start, end]
        self.key = "{}.{}".format(start, end)
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

    def setAloneStart(self, aloneStart, conflictIndex):
        self.aloneStart = aloneStart

    def setAloneEnd(self, aloneEnd, conflictIndex):
        self.aloneEnd = aloneEnd

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
    
    def checkRedundancy(currentNode, nextNode): ## checks whether Lifeguard's shift is entirely covered by another
        if currentNode.aloneStart <= nextNode.aloneStart and currentNode.aloneEnd >= nextNode.aloneEnd:
            nextNode.makeRedundant()
            return True
        return False

    minNode = None
    minIndex = 0

    for index, currentNode in enumerate(sortedInput):
        nextIndex = index
        nextNode = None

        if index + 1 < len(sortedInput):
            nextIndex += 1
            nextNode = sortedInput[nextIndex]

        if not currentNode.redundant:
            while nextNode != None:
                if minNode is None:
                    minNode = currentNode
                    minIndex = 0

                if currentNode.aloneEnd < nextNode.aloneStart: 
                    nextNode = None

                elif currentNode.aloneEnd > nextNode.aloneStart: 
                    nextNodeRedundant = checkRedundancy(currentNode, nextNode)
                    if nextNodeRedundant:
                        return nextNode
                    else:
                        temp = nextNode.aloneStart
                        nextNode.setAloneStart(currentNode.aloneEnd, currentNode.key)
                        currentNode.setAloneEnd(temp, nextNode.key)
                        currentNode.updateTotal()
                        nextNode.updateTotal()
                
                        if currentNode.totalAlone < minNode.totalAlone:
                            minNode = currentNode
                            minIndex = index
                        elif nextNode.totalAlone < minNode.totalAlone:
                            minNode = nextNode
                            minIndex = nextIndex

                    if nextIndex + 1 < len(sortedInput):
                        nextNode = sortedInput[nextIndex + 1]
                    else:
                        nextNode = None

    return minNode


def findMaxHours(inputFile):
    sortedInput = readFileInput(inputFile)  # read in and sort by time starting (n * nlogn)
    lifeguardToRemove = findMinLifeguard(sortedInput) # find lifeguard to fire... m (interval length) ... n * m
    totalHours = 0
    intervalStart = None
    intervalEnd = None

    sortedInput.remove(lifeguardToRemove) # for some reason removing by index throws a key error

    for index, node in enumerate(sortedInput):

        if intervalStart == None:
            intervalStart = node.shift[0] 
        if intervalEnd == None:
            intervalEnd = node.shift[1]

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

### tests
#findMaxHours('./input/11.in')
#findMaxHours('./input/12.in')
#findMaxHours('./input/13.in')

