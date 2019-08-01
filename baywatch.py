import copy 

class LifeguardNode:
  def __init__(self, start, end):
    self.shift = [start, end]
    self.key = "{}-{}".format(start, end)
    self.soloStart = start
    self.soloEnd = end
    self.soloTotal = self.soloEnd - self.soloStart
    self.timeConflicts = {} ## key, cost

  def adjustUniqueCoverage(self, otherNodeSoloStart, otherNodeSoloEnd, otherNodeKey):
    prevTotal = self.soloTotal
    if self.soloEnd > otherNodeSoloStart and self.soloEnd <= otherNodeSoloEnd:
      self.soloEnd = otherNodeSoloStart
    if self.soloStart > otherNodeSoloStart and self.soloStart < otherNodeSoloEnd:
      self.soloStart = otherNodeSoloEnd
    self.updateTotal()
    if prevTotal != self.soloTotal:
      self.addConflict(otherNodeKey, prevTotal - self.soloTotal)
    return self.soloTotal

  def updateTotal(self):
    self.soloTotal = self.soloEnd - self.soloStart

  def addConflict(self, otherNodeKey, numHoursConflicting):
    self.timeConflicts[otherNodeKey] = numHoursConflicting

  def __repr__(self):
    return "hours solo:{}".format(self.soloTotal)

def calculateCoverage(dictOfShifts, lifeguard1, lifeguard2, minKey):

    lg1Start = lifeguard1.soloStart
    lg1End = lifeguard1.soloEnd

    lg1NewTotal = lifeguard1.adjustUniqueCoverage(lifeguard2.soloStart, lifeguard2.soloEnd, lifeguard2.key)
    lg2NewTotal = lifeguard2.adjustUniqueCoverage(lg1Start, lg1End, lifeguard1.key)

    return minKey

    
def readFileInput(pathToFile, dictOfShifts):
  reader = open(pathToFile, "r")
  contents = reader.readlines()

  minKey = None
  for line in contents:
    editedLine = line.rstrip("\n")
    spaceIndex = editedLine.find(' ')
    if spaceIndex > -1:
      range = editedLine.split(' ')
      newNode = LifeguardNode(int(range[0]), int(range[1]))
      for key in dictOfShifts:
        minKey = calculateCoverage(dictOfShifts, newNode, dictOfShifts[key], minKey)
      dictOfShifts[newNode.key] = newNode

  print(minKey)
  print(dictOfShifts)
  reader.close()


""" invocations... """

dictOfShifts = {}
readFileInput('./input/1.in', dictOfShifts)