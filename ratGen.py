#Luke Brudnok
#9/10/24
GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

from rats import *
from texttools import createFile
from random import triangular, shuffle, uniform, choice, random
from time import time
from math import trunc

def initial_population():
     #Create the initial set of rats based on constants
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1
  
    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def calculate_weight(sex, mother, father):
     #Generate the weight of a single rat
  
  
  # Use the triangular function from the random library to skew the 
  #baby's weight based on its sex
  if father > mother:
    max = father.getWeight()
    min = mother.getWeight()
  else:
    max = mother.getWeight()
    min = father.getWeight()

  if sex == "M":
    wt = int(triangular(min, max, max))
  else:
    wt = int(triangular(min, max, min))

  return wt

def mutate(pups):
  """Check for mutability, modify weight of affected pups"""
  for rat in pups[0]:
    if random() <= MUTATE_ODDS:
      mutation = uniform(MUTATE_MIN, MUTATE_MAX)
      rat.mutate(mutation)

  for rat in pups[1]:
    if random() <= MUTATE_ODDS:
      mutation = uniform(MUTATE_MIN, MUTATE_MAX)
      rat.mutate(mutation)

  return pups

def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  male = rats[0]
  female = rats[1]
  shuffle(male)
  children = [[], []]

  for rat in range(10):
    father = male[rat]
    mother = female[rat]
    mother.incrementLitters()
    father.incrementLitters()

    for r in range(LITTER_SIZE):
      sex = choice(["M", "F"])
      if sex == "M":
        ind = 0
      else:
        ind = 1

      wt = calculate_weight(sex, mother, father)
      pup = Rat(sex, wt)
      children[ind].append(pup)
  return children  

def select(rats, pups):
  '''Choose the largest viable rats for the next round of breeding'''
  males = rats[0] + pups[0]
  females = rats[1] + pups[1]

  males.sort(reverse = True)
  females.sort(reverse = True)
  rats = [[], []]
  largest = None
  smallest = None
  if males[0] > females[0]:
    largest = males[0]
  else:
    largest = females[0]

  if males[-1] < females[-1]:
    smallest = males[-1]
  else:
    smallest = females[-1]


  for rat in males:
    if len(rats[0]) < 10 and rat.canBreed():
      rats[0].append(rat)

  for rat in females:
    if (len(rats[1]) < 10) and rat.canBreed():
      rats[1].append(rat)

  return rats, largest, smallest

def calculate_mean(rats):
  '''Calculate the mean weight of a population'''
  sumWt = 0
  numRats = len(rats[0]) + len(rats[1])
  for rat in rats[0]:
    sumWt += rat.getWeight()
  for rat in rats[1]:
    sumWt += rat.getWeight()

  return trunc(sumWt) // numRats

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  mean = calculate_mean(rats)

  return mean >= GOAL, mean

def main():
  timer1 = time()
  rats = initial_population()
  generations = 1
  status = False
  weight_averages = []
  largest = Rat("M", 0)
  largeList = []
  smallList = []

  while status == False and generations < GENERATION_LIMIT:

    pups = breed(rats)
    newGen = mutate(pups)
    rats, newlargest, smallest = select(rats, newGen)
    if newlargest > largest:
      largest = newlargest
    generations += 1
    largeList.append(trunc(newlargest.getWeight()))
    smallList.append(trunc(smallest.getWeight()))
    status, mean = fitness(rats)
    weight_averages.append(trunc(mean))


  timer2 = time()
  elapsed = timer2 - timer1
  print(f"final average weight: {mean}")
  print(f"Generations: {generations}")
  print(f"Experiment Duration: {generations/10} years")
  print(f"Completed Simulation in {elapsed} seconds")
  print(f"Largest Rat: {largest}")

  print("Generation Averages: ")
  for i in range(len(weight_averages)):
    print(weight_averages[i], end="\t")
    if i % 12 == 11:
      print()

  createFile("Largest Rats", largeList)
  createFile("Smallest Rats", smallList)
  createFile("Average Rats", weight_averages)
  
if __name__ == "__main__":
  main()