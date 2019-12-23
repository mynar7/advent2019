import os

input_file = './input.txt'

with open(input_file) as _file:
  lines = _file.read().splitlines()

maze = []
walls = set()
doors_dict = {}
keys_dict = {}

def print_maze():
  for row in maze:
    print(" ".join(row))

def make_point_string(coords):
  [x, y] = coords
  return f"{x}|{y}"

def split_point(point_string):
  (x, y) = point_string.split('|')
  return (int(x), int(y))

for y, line in enumerate(lines):
  line = list(line)
  for x, char in enumerate(line):
    if char == '.':
      line[x] = ' '
    if char == '#':
      walls.add(make_point_string([x, y]))
    if char == '@':
      origin = make_point_string([x, y])
    if ord(char) >= 65 and ord(char) <= 90:
      pt = make_point_string([x, y])
      doors_dict[pt] = char
    if ord(char) >= 97 and ord(char) <= 122:
      pt = make_point_string([x, y])
      keys_dict[pt] = char
  maze.append(line)

maze_width = len(maze[0])
maze_height = len(maze)

class MazeBot:
  keys = {}
  grabbed_keys = set()
  doors = {}
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
      elif coord_string in walls:
        coords_dict['walls'].append(key)
      else:
        coords_dict['unexplored'].append(key)

    return coords_dict

  def print(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    grid = [[' ' for _ in range(maze_width)] for _ in range(maze_height)]
    for pt in walls:
      (x, y) = split_point(pt)
      grid[y][x] = '#'
    for loc, door in doors_dict.items():
      (x, y) = split_point(loc)
      grid[y][x] = door
    for loc, key in keys_dict.items():
      (x, y) = split_point(loc)
      grid[y][x] = key
    for pt in self.paths:
      (x, y) = split_point(pt)
      grid[y][x] = '.'

    (x, y) = self.position
    grid[y][x] = '@'

    top_ruler = "  "
    for index in range(len(grid[0])):
      index = '0' + str(index) if index < 10 else str(index)
      top_ruler += index + ' '
    print(top_ruler)
    for index, row in enumerate(grid):
      index = '0' + str(index) if index < 10 else str(index)
      print(index, "  ".join(row), index)
    print(top_ruler)

  def flood(self, position):
    exploring = True
    paths = {}
    key_paths = {}
    path_count = 0
    surrounding = self.get_surrounding_coords(position)
    amt_of_possible_paths = len(surrounding['unexplored'])

    if amt_of_possible_paths == 0: assert False

    for direction in surrounding['unexplored']:
      path_count += 1
      next_coord = make_point_string(surrounding[direction])
      new_path = [next_coord]
      path_key = str(path_count)
      paths[path_key] = {'path': new_path, 'doors': set()}

    # for pretty printing only
    self.paths = set()
    self.position = split_point(position)

    while exploring:
      # if paths is 0, end loop
      if len(paths) == 0:
        break
      new_paths = {}
      for path_key in paths:
        coords_list = paths[path_key]['path']
        doors = paths[path_key]['doors']
        pos_str = coords_list[-1]
        if pos_str in keys_dict and pos_str != position:
          # end path, add to keys
          key_letter = keys_dict[pos_str]
          if key_letter not in key_paths:
            key_paths[key_letter] = {}
            key_paths[key_letter]['path'] = coords_list
            key_paths[key_letter]['doors'] = doors
          elif len(coords_list) < len(key_paths[key_letter]):
            key_paths[key_letter]['path'] = coords_list
            key_paths[key_letter]['doors'] = doors
        if pos_str in doors_dict:
          doors.add(doors_dict[pos_str])
        coords_set = set(coords_list)
        surrounding = self.get_surrounding_coords(pos_str, paths = coords_set)
        if len(surrounding['unexplored']) > 0:
          for direction in surrounding['unexplored']:
            path_count += 1
            new_path_coords_list = coords_list.copy()
            new_path_doors = doors.copy()
            new_coord = make_point_string(surrounding[direction])
            new_path_coords_list.append(new_coord)
            new_path_key = str(path_count)
            new_paths[new_path_key] = {}
            new_paths[new_path_key]['path'] = new_path_coords_list
            new_paths[new_path_key]['doors'] = new_path_doors
      paths = new_paths
      if input_file != './input.txt':
        for path in paths.values():
          for coord in path['path']:
            self.paths.add(coord)
        self.print()

    for key_path in key_paths:
      loc = key_paths[key_path]['path'][-1]
      assert loc in keys_dict
      path = key_paths[key_path]['path']
      distance = len(path)
      doors = key_paths[key_path]['doors']
      # key_paths[key_path] = {'distance': distance, 'doors': doors, 'location': loc, 'path': path}
      key_paths[key_path] = {'distance': distance, 'doors': doors, 'location': loc}
    return key_paths

  def get_keys(self):
    orig_key_distances = self.flood(self.origin)
    between_key_distances = {}
    paths = {}
    final_paths = {}

    for key_dist_key, key_dist_dict in orig_key_distances.items():
      location = key_dist_dict['location']
      doors = key_dist_dict['doors']
      other_keys = self.flood(location)
      between_key_distances[key_dist_key] = other_keys
      if len(doors) == 0:
        paths[key_dist_key] = key_dist_dict['distance']

    while True:
      if len(paths) == 0:
        break
      new_paths = {}
      for path, distance in paths.items():
        if len(path) == len(keys_dict):
          final_paths[path] = distance
        else:
          last_key = path[-1]
          keys = set(path)
          passable_doors = set(path.upper())
          for next_key, next_key_dict in between_key_distances[last_key].items():
            if next_key not in keys:
              key_reachable = True
              for door in next_key_dict['doors']:
                if door not in passable_doors:
                  key_reachable = False

              if key_reachable:
                new_distance = distance + next_key_dict['distance']
                ordered_path = "".join(sorted(list(path))) + next_key
                if ordered_path in new_paths:
                  if new_paths[ordered_path] > new_distance:
                    new_paths[ordered_path] = new_distance
                else:
                  new_paths[ordered_path] = new_distance

      paths = new_paths
      print(len(paths))
    path_list = [(path, final_paths[path]) for path in final_paths]
    sorted_path_list = sorted(path_list, key = lambda x: x[1])
    return sorted_path_list[0]

bot1 = MazeBot(origin)
print(bot1.get_keys())