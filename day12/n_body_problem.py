io_position = {'x': -7, 'y': -8, 'z': 9}
europa_position = {'x': -12, 'y': -3, 'z': -4}
ganymede_position = {'x': 6, 'y': -17, 'z': -9}
callisto_position = {'x': 4, 'y': -10, 'z': -6}

# EXAMPLE DATA SET
# io_position = {'x': -1, 'y': 0, 'z': 2}
# europa_position = {'x': 2, 'y': -10, 'z': -7}
# ganymede_position = {'x': 4, 'y': -8, 'z': 8}
# callisto_position = {'x': 3, 'y': 5, 'z': -1}

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

def snapshot_system_state():
  state = ""
  for index, moon in enumerate(moons):
    state += moon + ': positions:'
    for vector in ['x', 'y', 'z']:
      state += vector + '=' + str(moons[moon]['position'][vector])
      if vector is not 'z':
        state += ','
    state += ' vectors:'
    for vector in ['x', 'y', 'z']:
      state += vector + '=' + str(moons[moon]['velocity'][vector])
      if vector is not 'z':
        state += ','
    if index != len(moons) - 1:
      state += '\n'
  return state

positions = set()
positions.add(snapshot_system_state())
steps = 0
size = len(positions)
while True:
  update_velocity()
  update_position()
  snapshot = snapshot_system_state()
  steps += 1
  positions.add(snapshot)
  if size != len(positions):
    size += 1
  else:
    print(steps)
    print(size)
    print(snapshot)
    break


# print_moons()
# print(get_total_system_energy())

