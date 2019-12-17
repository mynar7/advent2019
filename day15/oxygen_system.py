import os
with open('./input.txt', 'r') as _file:
  strInputs = _file.read().split(',')

def getInputs(program, index, relative_base):
  def handleMode(mode, param, relative_base):
    if mode == 0:
      return program[param]
    if mode == 1:
      return param
    if mode == 2:
      return program[param + relative_base]
    return 0

  opcode = program[index]
  # 99 / 3 opcodes don't care about immediate v position mode
  if (opcode == 99):
    return (opcode, None, None, None)

  # if (opcode == 3):
  #   param1 = program[index + 1]
  #   return (opcode, param1, None, None)

  opcode = str(opcode)

  if (len(opcode) < 3):
    # opcode < 3 means no modes given, all should be 0
    parsedOpcode = int(opcode)
    modes = '000'
  else:
    # opcode is last 2 digits
    parsedOpcode = int(opcode[-2:])
    if (len(opcode) == 3):
      modes = opcode[0] + '01'
    if (len(opcode) == 4):
      # grab all but last 2
      modes = opcode[:-2]
      # reverse digits so they're in order of params left
      modes = modes[::-1]
      modes += '1'
    if (len(opcode) == 5):
      # grab all but last 2
      modes = opcode[:-2]
      # reverse digits so they're in order of params left
      modes = modes[::-1]


  if (parsedOpcode < 3 or parsedOpcode == 7 or parsedOpcode == 8):
    param1 = program[index + 1]
    param2 = program[index + 2]
    param3 = program[index + 3]
    param1 = handleMode(int(modes[0]), param1, relative_base)
    param2 = handleMode(int(modes[1]), param2, relative_base)
    if int(modes[2]) == 2:
      param3 += relative_base
    return (parsedOpcode, param1, param2, param3)

  if (parsedOpcode == 5 or parsedOpcode == 6):
    param1 = program[index + 1]
    param2 = program[index + 2]
    param1 = handleMode(int(modes[0]), param1, relative_base)
    param2 = handleMode(int(modes[1]), param2, relative_base)
    return (parsedOpcode, param1, param2, None)
  if (parsedOpcode == 4 or parsedOpcode == 9):
    param1 = program[index + 1]
    param1 = handleMode(int(modes[0]), param1, relative_base)
    return (parsedOpcode, param1, None, None)
  if (parsedOpcode == 3):
    param1 = program[index + 1]
    if int(modes[0]) == 2:
      param1 += relative_base
    # param1 = handleMode(int(modes[0]), param1, relative_base)
    return (parsedOpcode, param1, None, None)


def intcode(program, inputMethod, outputMethod = print, index = 0):
  for _ in range(10000):
    program.append(0)
  relative_base = 0
  while index >= 0:
    # print(index)
    (opcode, param1, param2, param3) = getInputs(program, index, relative_base)
    # print(f'opcode {opcode}, p1 {param1} p2 {param2} p3 {param3}')
    # print(program)
    if opcode == 99:
      index = -1
      return 'done'

    # add
    if opcode == 1:
      program[param3] = param1 + param2
      index += 4
    # multiply
    if opcode == 2:
      program[param3] = param1 * param2
      index += 4
    #write input
    if opcode == 3:
      # take the input and save it to position
      inputValue = inputMethod()
      # print(f'got input {inputValue}, param {param1}, index {index}')
      if (inputValue is not False):
        program[param1] = inputValue
        index += 2
      else:
        return index
    # output
    if opcode == 4:
      # print(f'outputting {param1}')
      # take parameter and output it
      outputMethod(param1)
      # do whatever with output
      index += 2
    # jump-if-true
    if opcode == 5:
      index = param2 if param1 != 0 else index + 3
    # jump-if-false
    if opcode == 6:
      index = param2 if param1 == 0 else index + 3
    # less than
    if opcode == 7:
      program[param3] = 1 if param1 < param2 else 0
      index += 4
    # equals
    if opcode == 8:
      program[param3] = 1 if param1 == param2 else 0
      index += 4
    if opcode == 9:
      relative_base += param1
      index += 2

inputs = list(map(lambda str: int(str), strInputs))

walls = set()
paths = set()
deadends = set()
position = [0, 0]
next_position = [0, 0]
prev_position = [0, 0]
tank_location = None
tank_found = False
prev_move_result = None

def manual_input():
  print(f"position: {position}")
  direction = input("\n")
  if direction == 'w':
    direction = 1
  if direction == 's':
    direction = 2
  if direction == 'a':
    direction = 3
  if direction == 'd':
    direction = 4
  if direction not in [1, 2, 3, 4]:
    return manual_input()

  if direction == 1:
    next_position[0] = position[0]
    next_position[1] = position[1] - 1
  if direction == 2:
    next_position[0] = position[0]
    next_position[1] = position[1] + 1
  if direction == 3:
    next_position[0] = position[0] - 1
    next_position[1] = position[1]
  if direction == 4:
    next_position[0] = position[0] + 1
    next_position[1] = position[1]
  return direction

def outputter(code):
  global tank_location, prev_move_result, tank_found
  if code == 0:
    prev_move_result = 'WALL'
    walls.add(make_point_string(next_position))
  if code == 1 or code == 2:
    prev_move_result = 'MOVED'
    pt_string = make_point_string(next_position)
    if pt_string not in deadends:
      paths.add(pt_string)
    prev_position[0] = position[0]
    prev_position[1] = position[1]
    position[0] = next_position[0]
    position[1] = next_position[1]
  if code == 2:
    tank_found = True
    tank_location = [next_position[0], next_position[1]]
  print_grid()

def make_point_string(coords):
  [x, y] = coords
  return f"{x}|{y}"

def split_point(point_string):
  (x, y) = point_string.split('|')
  return (int(x), int(y))

def get_min_max(x, minX = 0, maxX = 0):
  if x > 0 and x > maxX:
    maxX = x
  if x < 0 and x < minX:
    minX = x
  return (minX, maxX)

def print_grid():
  maxX = 0
  minX = 0
  maxY = 0
  minY = 0
  for pos in paths:
    (x, y) = split_point(pos)
    (minX, maxX) = get_min_max(x, minX, maxX)
    (minY, maxY) = get_min_max(y, minY, maxY)
  for pos in walls:
    (x, y) = split_point(pos)
    (minX, maxX) = get_min_max(x, minX, maxX)
    (minY, maxY) = get_min_max(y, minY, maxY)

  gridX = maxX + abs(minX) + 1
  gridY = maxY + abs(minY) + 1
  grid = [[' ' for _ in range(gridX)] for _ in range(gridY)]

  def convert_position(x, y, minX, minY):
    if x < 0:
      x = abs(minX) - abs(x)
    elif x > 0:
      x = abs(minX) + x
    else:
      x = abs(minX)
    if y < 0:
      y = abs(minY) - abs(y)
    elif y > 0:
      y = abs(minY) + y
    else:
      y = abs(minY)
    return (x, y)
  for pos in walls:
    (_x, _y) = split_point(pos)
    (x, y) = convert_position(_x, _y, minX, minY)
    grid[y][x] = '#'
  for pos in paths:
    (_x, _y) = split_point(pos)
    (x, y) = convert_position(_x, _y, minX, minY)
    grid[y][x] = '.'

  (bot_x, bot_y) = convert_position(position[0], position[1], minX, minY)

  grid[bot_y][bot_x] = '@'
  if tank_location is not None:
    (tank_x, tank_y) = convert_position(tank_location[0], tank_location[1], minX, minY)
    grid[tank_y][tank_x] = 'X'

  os.system('cls' if os.name == 'nt' else 'clear')
  for row in grid:
    print(" ".join(row))

class MazeBot:
  probing_location = [0, 0]
  probe_state = None

  def get_surrounding_coords(self):
    # get 4 points around current location
    # and find out if they're known
    (x, y) = position
    coords_dict = {'paths': [], 'walls': [], 'unexplored': [], 'deadends': []}
    UP = [x, y - 1]
    DOWN = [x, y + 1]
    LEFT = [x - 1, y]
    RIGHT = [x + 1, y]
    coords_dict['UP'] = UP
    coords_dict['DOWN'] = DOWN
    coords_dict['LEFT'] = LEFT
    coords_dict['RIGHT'] = RIGHT
    for key in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
      coord_string = make_point_string(coords_dict[key])
      if coord_string in paths:
        coords_dict['paths'].append(key)
      elif coord_string in walls:
        coords_dict['walls'].append(key)
      elif coord_string in deadends:
        coords_dict['deadends'].append(key)
      else:
        coords_dict['unexplored'].append(key)
    return coords_dict

  def probe(self):
    if tank_found:
      print(tank_location)
      print(f"Steps to reach Tank: {len(paths) - 1}")
      return

    surrounding = self.get_surrounding_coords()
    probe_position = make_point_string(position)
    # probing unknown loc
    if self.probe_state == None:
      self.probe_start_location = make_point_string(position)
      self.probe_last_path_location = make_point_string(prev_position)
      self.probe_state = 'PROBING_SURROUNDINGS'

    if self.probe_state == 'PROBING_SURROUNDINGS':
      # still finding surroundings
      if probe_position != self.probe_start_location:
        return self.direction_to_go_back
      # if there's more than one unexplored direction, keep exploring
      elif (
        probe_position == self.probe_start_location and
        len(surrounding['unexplored']) > 0
      ):
        return surrounding['unexplored'][0]
      # explored all directions
      elif (
        probe_position == self.probe_start_location and
        len(surrounding['unexplored']) == 0
      ):
        # two paths means there's only one new direction to go in
        if len(surrounding['paths']) == 2:
          self.probe_state = None
          for direction in surrounding['paths']:
            if make_point_string(surrounding[direction]) != self.probe_last_path_location:
              return direction
        # more than two paths means we've reached a fork
        elif len(surrounding['paths']) > 2:
          # reset state so we can continue probing
          self.probe_state = None
          self.fork_location = make_point_string(position)
          self.pt_before_fork = self.probe_last_path_location
          # pick direction to explore in
          for direction in surrounding['paths']:
            if make_point_string(surrounding[direction]) != self.probe_last_path_location:
               chosen_direction = direction
               break
          # remove unexplored direction from path
          for direction in surrounding['paths']:
            pt_string = make_point_string(surrounding[direction])
            if (
              direction != chosen_direction and
              pt_string != self.probe_last_path_location
            ):
              paths.remove(pt_string)
          return chosen_direction
        # three walls means deadend
        elif (
          len(surrounding['walls']) == 3 and
          probe_position != '0|0'
        ):
          paths.remove(probe_position)
          deadends.add(probe_position)
          self.probe_state = 'BACK_TRACKING'
          return self.direction_to_go_back
        # only one open path and at origin, go that way
        else:
          self.probe_state = None
          return surrounding['paths'][0]

    elif self.probe_state == 'BACK_TRACKING':
      if len(surrounding['unexplored']) == 0:
        if probe_position in paths:
          paths.remove(probe_position)
        deadends.add(probe_position)
        return surrounding['paths'][0]
      elif (
        len(surrounding['unexplored']) == 1
      ):
        self.probe_state = None
        return surrounding['unexplored'][0]

  def get_move(self):
    direction = self.probe()
    output_direction = None

    if direction == 'UP':
      next_position[0] = position[0]
      next_position[1] = position[1] - 1
      output_direction = 1
      self.direction_moved = 'UP'
      self.direction_to_go_back = 'DOWN'
    elif direction == 'DOWN':
      next_position[0] = position[0]
      next_position[1] = position[1] + 1
      output_direction = 2
      self.direction_moved = 'DOWN'
      self.direction_to_go_back = 'UP'
    elif direction == 'LEFT':
      next_position[0] = position[0] - 1
      next_position[1] = position[1]
      output_direction = 3
      self.direction_moved = 'LEFT'
      self.direction_to_go_back = 'RIGHT'
    elif direction == 'RIGHT':
      next_position[0] = position[0] + 1
      next_position[1] = position[1]
      output_direction = 4
      self.direction_moved = 'RIGHT'
      self.direction_to_go_back = 'LEFT'
    return output_direction

bot1 = MazeBot()

intcode(inputs, bot1.get_move, outputter)
# intcode(inputs, manual_input, outputter)
