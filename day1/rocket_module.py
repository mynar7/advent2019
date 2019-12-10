import os
import math

from functools import reduce

filepath = os.path.join('.', 'input.txt')

answer = 0

with open(filepath, 'r') as file_handler:
  values = file_handler.read()
  lines = values.splitlines()
  for line in lines:
    calculatedFuelVal = math.floor(int(line) / 3) - 2
    answer = answer + calculatedFuelVal

print(answer)


with open(filepath, 'r') as file_handler:
  values = file_handler.read()
  lines = values.splitlines()
  answer = reduce(lambda accum, current: accum + (math.floor(int(current) / 3) - 2), lines, 0)
  print(answer)







with open(filepath, 'r') as file_handler:
  values = file_handler.read()
  lines = values.splitlines()
  def getFuel(mass):
    fuel = math.floor(mass / 3) - 2
    return fuel + getFuel(fuel) if fuel > 0 else 0
  answer = reduce(lambda accum, current: accum + getFuel(int(current)), lines, 0)
  print(answer)
