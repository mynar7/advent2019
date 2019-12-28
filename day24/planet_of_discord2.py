with open('./input.txt') as _file:
  lines = _file.read().splitlines()

bug_grid = []

for line in lines:
  bug_grid.append(line)

def print_grid(grid):
  for row in grid:
    print(row)

def count_bugs_top_outer(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    bugs = 0
    for char in bug_grid[0]:
      if char == '#':
        bugs += 1
    return bugs
  else:
    return 0

def count_bugs_bottom_outer(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    bugs = 0
    for char in bug_grid[-1]:
      if char == '#':
        bugs += 1
    return bugs
  else:
    return 0

def count_bugs_left_outer(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    bugs = 0
    for row in bug_grid:
      if row[0] == '#':
        bugs += 1
    return bugs
  else:
    return 0

def count_bugs_right_outer(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    bugs = 0
    for row in bug_grid:
      if row[-1] == '#':
        bugs += 1
    return bugs
  else:
    return 0

def count_bugs_top_inner(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    return 1 if bug_grid[1][2] == '#' else 0
  else:
    return 0

def count_bugs_bottom_inner(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    return 1 if bug_grid[3][2] == '#' else 0
  else:
    return 0

def count_bugs_left_inner(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    return 1 if bug_grid[2][1] == '#' else 0
  else:
    return 0

def count_bugs_right_inner(depth):
  if depth in grid_dict:
    bug_grid = grid_dict[depth]
    return 1 if bug_grid[2][3] == '#' else 0
  else:
    return 0

def count_bugs(bug_grid, x, y, depth):
  bugs = 0
  width = len(bug_grid[0])
  height = len(bug_grid)

  # check outer depth
  if x == 0:
    bugs += count_bugs_left_inner(depth + 1)
  if x == width - 1:
    bugs += count_bugs_right_inner(depth + 1)
  if y == 0:
    bugs += count_bugs_top_inner(depth + 1)
  if y == height - 1:
    bugs += count_bugs_bottom_inner(depth + 1)

  # check inner depth
  # top middle
  if x == 2 and y == 1:
    bugs += count_bugs_top_outer(depth - 1)
  # bottom middle
  if x == 2 and y == 3:
    bugs += count_bugs_bottom_outer(depth - 1)
  # left middle
  if x == 1 and y == 2:
    bugs += count_bugs_left_outer(depth - 1)
  # right middle
  if x == 3 and y == 2:
    bugs += count_bugs_right_outer(depth - 1)

  # check current grid for bugs
  top = (x, y - 1)
  bottom = (x, y + 1)
  left = (x - 1, y)
  right = (x + 1, y)
  for _x, _y in [top, bottom, left, right]:
    if (
      _x > -1 and
      _x < width and
      _y > -1 and
      _y < height and
      not (_x == 2 and _y == 2)
    ):
      bugs += 1 if bug_grid[_y][_x] == '#' else 0
  return bugs

def update_bug_grid(bug_grid, depth):
  width = len(bug_grid[0])
  height = len(bug_grid)
  _bug_grid = [['.' for _ in range(width)] for _ in range(height)]

  for y in range(height):
    for x in range(width):
      if x == 2 and y == 2:
        _bug_grid[y][x] = '?'
      else:
        bugs = count_bugs(bug_grid, x, y, depth)
        bug_present = True if bug_grid[y][x] == '#' else False
        if bugs != 1 and bug_present:
          _bug_grid[y][x] = '.'
        elif bugs == 1 and bug_present:
          _bug_grid[y][x] = '#'
        elif (bugs == 1 or bugs == 2) and not bug_present:
          _bug_grid[y][x] = '#'

  for index, row in enumerate(_bug_grid):
    _bug_grid[index] = "".join(row)

  return _bug_grid

def generate_grid(width = 5, height = 5):
  new_grid = [['.' for _ in range(width)] for _ in range(height)]
  for index, row in enumerate(new_grid):
    new_grid[index] = "".join(row)
  return new_grid

def update_grid_dict(grid_dict):
  _grid_dict = {}
  max_depth = 0
  min_depth = 0
  for depth, grid in grid_dict.items():
    if depth > max_depth:
      max_depth = depth
    if depth < min_depth:
      min_depth = depth

    _new_grid = update_bug_grid(grid, depth)
    _grid_dict[depth] = _new_grid

  new_max_grid = generate_grid()
  new_max_depth = max_depth + 1
  new_max_grid = update_bug_grid(new_max_grid, new_max_depth)
  _grid_dict[new_max_depth] = new_max_grid

  new_min_grid = generate_grid()
  new_min_depth = min_depth - 1
  new_min_grid = update_bug_grid(new_min_grid, new_min_depth)
  _grid_dict[new_min_depth] = new_min_grid

  return _grid_dict

def count_all_bugs(grid_dict):
  bugs = 0
  for grid in grid_dict.values():
    for row in grid:
      for char in row:
        if char == '#':
          bugs += 1
  return bugs

grid_dict = {}
grid_dict[0] = bug_grid


for _ in range(200):
  grid_dict = update_grid_dict(grid_dict)

print(count_all_bugs(grid_dict))