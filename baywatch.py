
def readFileInput(pathToFile):
  reader = open(pathToFile, "r")
  contents = reader.readlines()

  for line in contents:
    editedLine = line.rstrip("\n")
    print(editedLine)

  reader.close()


readFileInput('./input/1.in')