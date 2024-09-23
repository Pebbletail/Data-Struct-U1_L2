#Luke Brudnok
#9/19/24

from texttools import readFile
import matplotlib.pyplot as plt

def retrieveData(file_names):
  data = []
  for x in file_names:
    text = readFile(x)
    text = list(text.split(","))
    data.append(text)

  return data

def createPlot(data):
  smallest = data[0]
  largest = data[1]
  average = data[2]

  for dataset in [smallest, largest, average]:
    plt.plot(dataset)

    plt.title("Rat Weight Graph")
    plt.xlabel("Generation")
    plt.ylabel("Weight (grams)")

    plt.legend(["smallest", "largest", "average"])
    plt.show()
    plt.savefig('rat_graph.png')



def main():
  data = retrieveData(["Smallest Rats", "Largest Rats", "Average Rats"])
  createPlot(data)

if __name__ == "__main__":
  main()