with open('./input.txt') as _file:
  lines = _file.read().splitlines()

bug_grid = []

for line in lines:
  bug_grid.append(line)

states = set()

def print_grid(grid):
  for row in grid:
    print(row)

def convert_grid_to_string(bug_grid):
  state_str = ""
  for line in bug_grid:
    state_str += line
  return state_str

def count_bugs(bug_grid, x, y):
  bugs = 0
  width = len(bug_grid[0])
  height = len(bug_grid)
  top = (x, y - 1)
  bottom = (x, y + 1)
  left = (x - 1, y)
  right = (x + 1, y)
  for x, y in [top, bottom, left, right]:
    if (
      x > -1 and
      x < width and
      y > -1 and
      y < height
    ):
      bugs += 1 if bug_grid[y][x] == '#' else 0
  return bugs

def update_bug_grid(bug_grid):
  width = len(bug_grid[0])
  height = len(bug_grid)
  _bug_grid = [['.' for _ in range(width)] for _ in range(height)]

  for y in range(height):
    for x in range(width):
      bugs = count_bugs(bug_grid, x, y)
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

def calculate_biodiversity(bug_grid):
  rating = 0
  n = 0
  for row in bug_grid:
    for char in row:
      if char == '#':
        rating += pow(2, n)
      n += 1
  return rating


state_repeated = False
while not state_repeated:
  bug_grid = update_bug_grid(bug_grid)
  grid_state = convert_grid_to_string(bug_grid)
  if grid_state not in states:
    states.add(grid_state)
  else:
    state_repeated = True

print_grid(bug_grid)

rating = calculate_biodiversity(bug_grid)
print(rating)