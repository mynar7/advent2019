import os

input_file = './input.txt'

with open(input_file) as _file:
  lines = _file.read().splitlines()

maze = []
walls = set()
portals_dict_by_name = {}
portals_dict = {}
portal_letters = set()

def make_point_string(coords):
  [x, y] = coords
  return f"{x}|{y}"

def split_point(point_string):
  (x, y) = point_string.split('|')
  return (int(x), int(y))

for y, line in enumerate(lines):
  line = list(line)
  for x, char in enumerate(line):
    if char == '#':
      walls.add(make_point_string([x, y]))
    else:
      line[x] = ' '
  maze.append(line)

maze_width = len(maze[0])
maze_height = len(maze)

def print_maze():
  for row in maze:
    print(" ".join(row))

def add_portal(x, y, portal_letter):
  global entrance_portal, exit_portal
  if (
    # top vertical portals
    y == 0 or
    # bottom inside donut
    (
      y > maze_height // 2 and y < maze_height - 2 and
      x > 1 and x < maze_width - 2 and
      lines[y + 2][x] == '.'
    )
  ):
    second_portal_letter = lines[y + 1][x]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x, y + 1])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x, y + 2])
  elif (
    # bottom vertical portals
    y == maze_height - 2 or
    # top inside donut
    (
      y < maze_height // 2 and y > 1 and
      x > 1 and x < maze_width - 2 and
      lines[y - 1][x] == '.'
    )
  ):
    second_portal_letter = lines[y + 1][x]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x, y + 1])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x, y - 1])
  elif (
    # left edge horiz portal
    x == 0 or
    # right inside donut
    (
      x > maze_width // 2 and x < maze_width - 2 and
      y > 1 and y < maze_height - 2 and
      lines[y][x + 2] == '.'
    )
  ):
    second_portal_letter = lines[y][x + 1]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x + 1, y])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x + 2, y])
  elif (
    # right edge horiz portal
    x == maze_width - 2 or
    # left inside donut
    (
      x > 1 and x < maze_width // 2 and
      y > 1 and y < maze_height - 2 and
      lines[y][x - 1] == '.'
    )
  ):
    second_portal_letter = lines[y][x + 1]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x + 1, y])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x - 1, y])

  if 'second_portal_letter' not in locals(): return

  ascii_second_letter = ord(second_portal_letter)
  if ascii_second_letter < 65 or ascii_second_letter > 90: return
  assert ascii_second_letter >= 65 and ascii_second_letter <= 90

  portal_letters.add(first_portal_letter_loc)
  portal_letters.add(second_portal_letter_loc)

  if portal_name == 'AA':
    entrance_portal = portal_loc
  elif portal_name == 'ZZ':
    exit_portal = portal_loc
  elif portal_name in portals_dict_by_name:
    portals_dict_by_name[portal_name].append(portal_loc)
  else:
    portals_dict_by_name[portal_name] = [portal_loc]

  maze[y][x] = portal_letter
  (x, y) = split_point(second_portal_letter_loc)
  maze[y][x] = second_portal_letter
  # (x, y) = split_point(portal_loc)
  # maze[y][x] = '@'

for y, line in enumerate(lines):
  line = list(line)
  for x, char in enumerate(line):
    if ord(char) >= 65 and ord(char) <= 90:
      add_portal(x, y, char)

for first, second in portals_dict_by_name.values():
  portals_dict[first] = second
  portals_dict[second] = first

class MazeBot:
  paths = set()
  position = [0, 0]

  def __init__(self, origin = '0|0'):
    self.origin = origin
    self.position = split_point(origin)

  def get_surrounding_coords(self, current_position, paths = set()):
    # get 4 points around current location
    # and find out if they're known
    (x, y) = split_point(current_position)
    coords_dict = {'paths': [], 'walls': [], 'unexplored': []}
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
      elif coord_string in walls or coord_string in portal_letters:
        coords_dict['walls'].append(key)
      else:
        coords_dict['unexplored'].append(key)

    if current_position in portals_dict:
      portal_exit = portals_dict[current_position]
      if portal_exit not in paths:
        coords_dict['unexplored'].append('PORTAL')
        coords_dict['PORTAL'] = split_point(portal_exit)

    return coords_dict

  def print(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    grid = maze.copy()

    for pt in self.paths:
      (x, y) = split_point(pt)
      grid[y][x] = '.'

    for row in grid:
      print(" ".join(row))

  def find_exit(self, position):
    exploring = True
    paths = {}
    path_count = 0
    surrounding = self.get_surrounding_coords(position)
    amt_of_possible_paths = len(surrounding['unexplored'])

    if amt_of_possible_paths == 0: assert False

    for direction in surrounding['unexplored']:
      path_count += 1
      next_coord = make_point_string(surrounding[direction])
      new_path = [next_coord]
      path_key = str(path_count)
      paths[path_key] = new_path

    # for pretty printing only
    self.paths = set()
    self.position = split_point(position)

    while exploring:
      # if paths is 0, end loop
      if len(paths) == 0:
        break
      new_paths = {}
      for path_key in paths:
        coords_list = paths[path_key]
        pos_str = coords_list[-1]

        # reached the end
        if pos_str == exit_portal:
          return len(coords_list)

        coords_set = set(coords_list)
        surrounding = self.get_surrounding_coords(pos_str, paths = coords_set)
        if len(surrounding['unexplored']) > 0:
          for direction in surrounding['unexplored']:
            path_count += 1
            new_path_coords_list = coords_list.copy()
            new_coord = make_point_string(surrounding[direction])
            new_path_coords_list.append(new_coord)
            new_path_key = str(path_count)
            new_paths[new_path_key] = new_path_coords_list
      paths = new_paths

      if input_file != './input.txt':
        for path in paths.values():
          for coord in path:
            self.paths.add(coord)
        self.print()


bot1 = MazeBot(entrance_portal)
print(bot1.find_exit(entrance_portal))