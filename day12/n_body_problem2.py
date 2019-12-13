io_position = {'x': -7, 'y': -8, 'z': 9}
europa_position = {'x': -12, 'y': -3, 'z': -4}
ganymede_position = {'x': 6, 'y': -17, 'z': -9}
callisto_position = {'x': 4, 'y': -10, 'z': -6}

# # EXAMPLE DATA SET 1
# io_position = {'x': -1, 'y': 0, 'z': 2}
# europa_position = {'x': 2, 'y': -10, 'z': -7}
# ganymede_position = {'x': 4, 'y': -8, 'z': 8}
# callisto_position = {'x': 3, 'y': 5, 'z': -1}

# # EXAMPLE DATA SET 2
# io_position = {'x': -8, 'y': -10, 'z': 0}
# europa_position = {'x': 5, 'y': 5, 'z': 10}
# ganymede_position = {'x': 2, 'y': -7, 'z': 3}
# callisto_position = {'x': 9, 'y': -8, 'z': -3}

moons = {
  'io': {
    'position': io_position,
    'velocity': {'x': 0, 'y': 0, 'z': 0}
  },
  'europa': {
    'position': europa_position,
    'velocity': {'x': 0, 'y': 0, 'z': 0}
  },
  'ganymede': {
    'position': ganymede_position,
    'velocity': {'x': 0, 'y': 0, 'z': 0}
  },
  'callisto': {
    'position': callisto_position,
    'velocity': {'x': 0, 'y': 0, 'z': 0}
  },
}

moon_pairs = set()
for moon in moons:
  for _moon in moons:
    if (moon is not _moon):
      _moons = sorted([moon, _moon])
      moon_pairs.add(f"{_moons[0]}|{_moons[1]}")

def print_moons():
  print('---\n')
  for moon in moons:
    print(moon.upper())
    print("position:", moons[moon]['position'])
    print("velocity:", moons[moon]['velocity'], '\n')
  print('---')

def update_velocity():
  # global moons
  for pair in moon_pairs:
    (moon1_key, moon2_key) = pair.split('|')
    for vector in ['x', 'y', 'z']:
      # smaller num gets +1, bigger gets -1
      if moons[moon1_key]['position'][vector] > moons[moon2_key]['position'][vector]:
        moons[moon1_key]['velocity'][vector]  -= 1
        moons[moon2_key]['velocity'][vector]  += 1
      elif moons[moon1_key]['position'][vector] < moons[moon2_key]['position'][vector]:
        moons[moon1_key]['velocity'][vector]  += 1
        moons[moon2_key]['velocity'][vector]  -= 1

def update_position():
  # global moons
  for moon in moons:
    for vector in ['x', 'y', 'z']:
      moons[moon]['position'][vector] += moons[moon]['velocity'][vector]

def get_total_system_energy():
  energy = 0
  for moon in moons:
    potential_energy = 0
    kinetic_energy = 0
    for vector in ['x', 'y', 'z']:
      potential_energy += abs(moons[moon]['position'][vector])
      kinetic_energy += abs(moons[moon]['velocity'][vector])
    energy += potential_energy * kinetic_energy
  return energy

def snapshot_system_axis(axis):
  assert axis in ['x', 'y', 'z']
  state = ""
  for index, moon in enumerate(moons):
    state += f"{moon}: "
    state += f"p{axis}: {moons[moon]['position'][axis]}, "
    state += f"v{axis}: {moons[moon]['velocity'][axis]}"
    if index != len(moons) - 1:
      state += ' | '
  return state

def get_sequence(axis):
  assert axis in ['x', 'y', 'z']
  positions = {}
  positions[snapshot_system_axis(axis)] = 0
  steps = 0

  while True:
    update_velocity()
    update_position()
    snapshot = snapshot_system_axis(axis)
    steps += 1
    if snapshot in positions:
      return steps - positions[snapshot]

    positions[snapshot] = steps

stepsX = get_sequence('x')
stepsY = get_sequence('y')
stepsZ = get_sequence('z')

print(f"Steps X: {stepsX}")
print(f"Steps Y: {stepsY}")
print(f"Steps Z: {stepsZ}")

def get_gcd(a, b):
  while a != b:
    if a > b:
      a = a - b
    else:
      b = b - a
  return a

def get_lcm(a, b):
  return (a * b) // get_gcd(a, b)

print(get_lcm(stepsX, get_lcm(stepsY, stepsZ)))


