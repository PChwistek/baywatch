## add break once someone has a 0 total...

class LifeguardNode:
  def __init__(self, start, end):
    self.shift = [start, end]
    self.key = "{}.{}".format(start, end)
    self.aloneStart = start
    self.aloneEnd = end
    self.totalAlone = 0
    self.conflicts = {}

  def updateTotal(self):
    self.totalAlone = self.aloneEnd - self.aloneStart if self.aloneEnd - self.aloneStart >= 0 else 0

  def setAloneStart(self, aloneStart, conflictIndex):
    prevStart = self.aloneStart
    self.aloneStart = aloneStart
    self.conflicts[conflictIndex] = aloneStart - prevStart

  def setAloneEnd(self, aloneEnd, conflictIndex):
    prevEnd = self.aloneEnd
    self.aloneEnd = aloneEnd
    self.conflicts[conflictIndex] = prevEnd - aloneEnd

  def __repr__(self):
    return "{}:{} - alone {}:{}".format(self.shift[0], self.shift[1], self.aloneStart, self.aloneEnd)

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
  output.sort(key=lambda x: x.shift[0])
  return output

def findMaxHours(inputFile):
  sortedInput = readFileInput(inputFile)
  minNode = None

  for index, node in enumerate(sortedInput):
      next_index = index
      nextNode = None

      if index + 1 < len(sortedInput):
        next_index += 1
        nextNode = sortedInput[next_index]

      while nextNode != None:
        minNode = node if minNode is None else nextNode
        if node.aloneEnd < nextNode.aloneStart:
          nextNode = None
        elif node.aloneEnd > nextNode.aloneStart:
          temp = nextNode.aloneStart
          nextNode.setAloneStart(node.aloneEnd, node.key)
          node.setAloneEnd(temp, nextNode.key)

          node.updateTotal()
          nextNode.updateTotal()
          
          if node.totalAlone < minNode.totalAlone:
            minNode = node
          elif nextNode.totalAlone < minNode.totalAlone:
            minNode = nextNode

          if next_index + 1 < len(sortedInput):
            nextNode = sortedInput[next_index + 1]
          else:
            break

  totalHours = 0

  for index, node in enumerate(sortedInput):
    if node.key != minNode.key:
      if node.key in minNode.conflicts:
        totalHours += minNode.conflicts[node.key]
      totalHours += node.totalAlone

  print("total hours", totalHours)

# for i in range(10):
#   findMaxHours('./input/' + str(i + 1) + '.in')

### tests
findMaxHours('./input/11.in')

