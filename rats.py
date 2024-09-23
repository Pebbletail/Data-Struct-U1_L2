class Rat:
  def __init__(self, sex, weight):
    self.sex = sex
    self.weight = weight
    self.litters = 0

  def __str__(self):
    str = f"({self.sex}) {self.weight}g"
    return str

  def __repr__(self):
    #rep = f"{[self.sex, self.weight]}"
    rep = f"{self.sex}{self.weight}"
    return rep

  def getSex(self):
    return self.sex

  def getWeight(self):
    return self.weight

  def canBreed(self):
    if self.litters > 5:
      return False
    else:
      return True

  def mutate(self, mutation):
    self.weight = self.weight * mutation

  def incrementLitters(self):
    self.litters += 1

  def __lt__(self, other):
    return self.weight < other.weight

  def __gt__(self, other):
    return self.weight > other.weight

  def __le__(self,other):
    return self.weight >= other.weight

  def __ge__(self,other):
    return self.weight <= other.weight

  def __eq__(self,other):
    return self.weight == other.weight