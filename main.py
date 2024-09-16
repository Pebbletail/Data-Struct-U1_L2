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
from random import triangular
from random import random
from random import uniform
from time import time

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
  for rat in pups:
    if random() <= MUTATE_ODDS:
      mutation = uniform(MUTATE_MIN, MUTATE_MAX)
      rat.mutate(mutation)

  return pups

def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  male = rats[0]
  female = rats[1]
  ratSex = ""
  children = []

  for rat in range(len(male)):
    father = male[rat]
    mother = female[rat]

    for i in range(LITTER_SIZE):
      if i % 2 == 0:
        ratSex = "M"
      else:
        ratSex = "F"

      wt = calculate_weight(ratSex, mother, father)
      pup = Rat(ratSex, wt)
      children.append(pup)


  return children  

def select(rats, pups):
  '''Choose the largest viable rats for the next round of breeding'''
  all = rats[0] + rats[1] + pups
  males = []
  females = []
  print(len(all))
  

  males = [rat for rat in all if rat.getSex() == "M"]
  females = [rat for rat in all if rat.getSex() == "F"]

  males.sort(reverse = True)
  females.sort(reverse = True)

  for rat in males:
    if rat.canBreed() == False:
      
  print(females[:10])
  print(males[:10])

  rats = [[males], [females]]
  largest = [[males[:10]], [females[:10]]]


  return rats, largest

def calculate_mean(rats):
  '''Calculate the mean weight of a population'''
  sumWt = 0
  numRats = len(rats[0]) + len(rats[1])
  for rat in rats:
    sumWt += rat.getWeight()

  return sumWt // numRats

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  pass
  #return mean >= GOAL, mean

def main():
  timer1 = time()
  rats = initial_population()

  pups = breed(rats)
  newGen = mutate(pups)
  status = fitness()
  rats, breed = select(rats, newGen)

  timer2 = time()
  elapsed = timer2 - timer1
  print(f"completed simulation in {elapsed}s")
  pass

if __name__ == "__main__":
  main()