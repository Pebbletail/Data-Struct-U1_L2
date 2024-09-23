#Luke Brudnok
#9/19/24

def createFile(file_name, contents):
  with open(file_name, 'w') as file:
    file.write(str(contents))

def readFile(file_name):
  f = open(file_name, "r")
  return f.read()
