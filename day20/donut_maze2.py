import os

input_file = './input.txt'

with open(input_file) as _file:
  lines = _file.read().splitlines()

maze = []
walls = set()
portals_dict_by_name = {}
portals_dict = {}
outer_portals = set()
inner_portals = set()
portal_letters = set()

def make_point_string(coords):
  [x, y] = coords
  return f"{x}|{y}"

def make_point_and_level_string(x, y, level = 0):
  return f"{x}|{y},{level}"

def split_point(point_string):
  (x, y) = point_string.split('|')
  return (int(x), int(y))

def split_point_and_level(point_string):
  (coords, level) = point_string.split(',')
  (x, y) = coords.split('|')
  return (int(x), int(y), int(level))

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

  is_top_outer_portal = y == 0
  is_top_inner_portal = (
      y < maze_height // 2 and y > 1 and
      x > 1 and x < maze_height - 2 and
      lines[y - 1][x] == '.'
    )

  is_bottom_outer_portal = y == maze_height - 2
  is_bottom_inner_portal = (
      y > maze_height // 2 and y < maze_height - 2 and
      x > 1 and x < maze_height - 2 and
      lines[y + 2][x] == '.'
    )

  is_left_outer_portal = x == 0
  is_left_inner_portal = (
      x > 1 and x < maze_width // 2 and
      y > 1 and y < maze_height - 2 and
      lines[y][x - 1] == '.'
    )

  is_right_outer_portal = x == maze_width - 2
  is_right_inner_portal = (
      x > maze_width // 2 and x < maze_width - 2 and
      y > 1 and y < maze_height - 2 and
      lines[y][x + 2] == '.'
    )

  if is_top_outer_portal or is_bottom_inner_portal:
    second_portal_letter = lines[y + 1][x]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x, y + 1])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x, y + 2])

  elif is_bottom_outer_portal or is_top_inner_portal:
    second_portal_letter = lines[y + 1][x]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x, y + 1])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x, y - 1])

  elif is_left_outer_portal or is_right_inner_portal:
    second_portal_letter = lines[y][x + 1]
    first_portal_letter_loc = make_point_string([x, y])
    second_portal_letter_loc = make_point_string([x + 1, y])
    portal_name = portal_letter + second_portal_letter
    portal_loc = make_point_string([x + 2, y])

  elif is_right_outer_portal or is_left_inner_portal:
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
  else:
    if portal_name in portals_dict_by_name:
      portals_dict_by_name[portal_name].append(portal_loc)
    else:
      portals_dict_by_name[portal_name] = [portal_loc]

    if (
      is_left_outer_portal or
      is_right_outer_portal or
      is_top_outer_portal or
      is_bottom_outer_portal
    ):
      outer_portals.add(portal_loc)
    else:
      inner_portals.add(portal_loc)

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


def get_surrounding_coords(current_position, paths = set()):
  # get 4 points around current location
  # and find out if they're known
  (x, y, level) = split_point_and_level(current_position)
  coords_dict = {'paths': [], 'walls': [], 'unexplored': []}
  UP = [x, y - 1, level]
  DOWN = [x, y + 1, level]
  LEFT = [x - 1, y, level]
  RIGHT = [x + 1, y, level]
  coords_dict['UP'] = UP
  coords_dict['DOWN'] = DOWN
  coords_dict['LEFT'] = LEFT
  coords_dict['RIGHT'] = RIGHT
  for key in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
    (x, y, level) = coords_dict[key]
    coord_string_with_level = make_point_and_level_string(x, y, level)
    coord_string = make_point_string([x, y])
    if coord_string_with_level in paths:
      coords_dict['paths'].append(key)
    elif (
      coord_string in walls or
      coord_string in portal_letters
    ):
      coords_dict['walls'].append(key)
    else:
      coords_dict['unexplored'].append(key)

  (x, y, level) = split_point_and_level(current_position)
  current_position_coords = make_point_string([x, y])

  if (
    (
      current_position_coords in outer_portals and
      level > 0
    ) or
    (current_position_coords in inner_portals)
  ):
    portal_exit = portals_dict[current_position_coords]
    (x, y) = split_point(portal_exit)
    new_level = level - 1 if current_position_coords in outer_portals else level + 1
    portal_exit += ',' + str(new_level)
    if portal_exit not in paths and new_level >= 0 and new_level < len(inner_portals):
      coords_dict['unexplored'].append('PORTAL')
      coords_dict['PORTAL'] = [x, y, new_level]

  return coords_dict

def find_exit(position):
  exploring = True
  paths = {}
  path_count = 0
  surrounding = get_surrounding_coords(position + ',0')
  amt_of_possible_paths = len(surrounding['unexplored'])

  if amt_of_possible_paths == 0: assert False

  for direction in surrounding['unexplored']:
    path_count += 1
    (x, y, level) = surrounding[direction]
    next_coord = make_point_and_level_string(x, y, level)
    new_path = [next_coord]
    path_key = str(path_count)
    paths[path_key] = new_path

  while exploring:
    # if paths is 0, end loop
    # print(len(paths))
    if len(paths) == 0:
      break
    new_paths = {}
    for path_key in paths:
      coords_list = paths[path_key]
      pos_str = coords_list[-1]
      (x, y, level) = split_point_and_level(pos_str)
      coords_string = make_point_string([x, y])
      # reached the end
      # if coords_string == exit_portal:
      #   print('YAHTZEE', level)
      if coords_string == exit_portal and level == 0:
        return len(coords_list)

      coords_set = set(coords_list)
      surrounding = get_surrounding_coords(pos_str, coords_set)
      if len(surrounding['unexplored']) > 0:
        for direction in surrounding['unexplored']:
          path_count += 1
          new_path_coords_list = coords_list.copy()
          (x, y, level) = surrounding[direction]
          new_coord = make_point_and_level_string(x, y, level)
          new_path_coords_list.append(new_coord)
          new_path_key = str(path_count)
          new_paths[new_path_key] = new_path_coords_list
    paths = new_paths

print(find_exit(entrance_portal))