with open('./input.txt') as _file:
  inputs = _file.read()
inputs = inputs.splitlines()

# part 1 help
# inputs = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L']

# part 2 help
# inputs = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']

# create dictionary for fast lookups
orbitDictionary = {}

for line in inputs:
  (orbit, planet) = line.split(')')
  # insert into dictionary by Planet, set value to orbit
  # { planet: orbit }
  orbitDictionary[planet] = orbit

# part 1 solution
orbits = 0

for planet in orbitDictionary:
  # direct orbits
  directOrbit = orbitDictionary[planet]
  orbits += 1
  # indirect orbits
  COM_found = False
  while not COM_found:
    if (directOrbit in orbitDictionary):
      directOrbit = orbitDictionary[directOrbit]
      orbits += 1
    else:
      COM_found = True

print(f" number of direct and indirect orbits: {orbits}")

# part 2 solution
# find YOU
# traverse to COM
# store path
# find SAN
# traverse to COM until common planet in path
# store num indirect orbits
# go back to YOU's path, count until you get to common planet
# add together

my_path = []
# find planet I'm orbiting
my_planet = orbitDictionary['YOU']
print(f"My starting planet: {my_planet}")
# find planet Santa is orbiting
santa_planet = orbitDictionary['SAN']
print(F"Santa's starting planet: {santa_planet}")

# find my path to COM
COM_found = False
directOrbit = my_planet
while not COM_found:
  if (directOrbit in orbitDictionary):
      directOrbit = orbitDictionary[directOrbit]
      my_path.append(directOrbit)
  else:
    COM_found = True
print(f"My path to COM: {my_path}")

# find Santa's path to common planet
COM_found = False
directOrbit = santa_planet
# track number of jumps
santa_steps = 0
while not COM_found:
  if (directOrbit in orbitDictionary):
      directOrbit = orbitDictionary[directOrbit]
      santa_steps += 1
      # if common planet is found, break loop
      if (directOrbit in my_path):
        common_planet = directOrbit
        break
  else:
    COM_found = True

print(f"Common planet between Santa and I: {common_planet}")
print(f"Santa's steps to get there: {santa_steps}")

# trace my steps to common planet
my_steps = 0
for planet in my_path:
  if (planet == common_planet):
    my_steps += 1
    break
  else:
    my_steps += 1
print(f"My steps to common planet: {my_steps}")

steps_to_santa = my_steps + santa_steps
print(f"Steps to Santa: {steps_to_santa}")