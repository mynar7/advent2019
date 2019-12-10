with open('./input.txt') as _file:
  asteroid_map = _file.read().splitlines()

for index, row in enumerate(asteroid_map):
  _row = []
  for char in row:
    _row.append(char)
  asteroid_map[index] = _row

def print_asteroids():
  for row in asteroid_map:
    print("".join(row))

def split_point(point):
  (point_x, point_y) = point.split('|')
  return (int(point_x), int(point_y))

# find distance to edges of a point
def get_distance_to_edges(point, asteroid_map):
  (x, y) = split_point(point)
  width = len(asteroid_map[0])
  height = len(asteroid_map)
  distance_to_left_side = x
  distance_to_top = y
  distance_to_right_side = width - x - 1
  distance_to_bottom = height - y - 1
  return {
    'to_left_side': distance_to_left_side,
    'to_right_side': distance_to_right_side,
    'to_top': distance_to_top,
    'to_bottom': distance_to_bottom,
  }

def find_slopes(point, asteroid_map):
  distance = get_distance_to_edges(point, asteroid_map)
  slopes = set()
  # get horizontal/vertical slopes
  if distance['to_top'] > 0:
    slopes.add('0|-1')
  if distance['to_bottom'] > 0:
    slopes.add('0|1')
  if distance['to_right_side'] > 0:
    slopes.add('1|0')
  if distance['to_left_side'] > 0:
    slopes.add('-1|0')
  # both positive
  if distance['to_right_side'] > 0 and distance['to_bottom'] > 0:
    slopes.add('1|1')
    for i in range(1, distance['to_right_side'] + 1):
      for j in range(1, distance['to_bottom'] + 1):
        if (i != 0 and j != 0 and i != j ):
          slopes.add(f"{i}|{j}")
  # both negative
  if distance['to_left_side'] > 0 and distance['to_top'] > 0:
    slopes.add('-1|-1')
    for i in range(1, distance['to_left_side'] + 1):
      for j in range(1, distance['to_top'] + 1):
        if (i != 0 and j != 0 and i != j ):
          slopes.add(f"{i * -1}|{j * -1}")
  # positive x, negative y
  if distance['to_right_side'] > 0 and distance['to_top'] > 0:
    slopes.add('1|-1')
    for i in range(1, distance['to_right_side'] + 1):
      for j in range(1, distance['to_top'] + 1):
        if (i != 0 and j != 0 and i != j ):
          slopes.add(f"{i}|{j * -1}")
  # negative x, positive y
  if distance['to_left_side'] > 0 and distance['to_bottom'] > 0:
    slopes.add('-1|1')
    for i in range(1, distance['to_left_side'] + 1):
      for j in range(1, distance['to_bottom'] + 1):
        if (i != 0 and j != 0 and i != j ):
          slopes.add(f"{i * -1}|{j}")

  def reduce_fractions(slopes):
    deduped = set()
    for slope in slopes:
      (x, y) = split_point(slope)
      (_x, _y) = (abs(x),abs(y))
      if x == 0 or y == 0:
        deduped.add(slope)
      else:
        max_val = max(_x, _y)
        i = 1
        reduced_x = _x
        reduced_y = _y
        while i < max_val:
          if _x % i == 0 and _y % i == 0:
            reduced_x = _x // i
            reduced_y = _y // i
          i += 1
        if x < 0:
          reduced_x = reduced_x * -1
        if y < 0:
          reduced_y = reduced_y * -1
        deduped.add(f"{reduced_x}|{reduced_y}")
    return deduped

  return reduce_fractions(slopes)

def find_asteroids(point, asteroid_map):
  slopes = find_slopes(point,asteroid_map)
  width = len(asteroid_map[0])
  height = len(asteroid_map)
  (origin_x, origin_y) = split_point(point)
  found_asteroids = set()
  for slope in slopes:
    current_x = origin_x
    current_y = origin_y
    (dx, dy) = split_point(slope)
    in_bounds = True
    while in_bounds:
      current_x += dx
      current_y += dy
      if (current_x >= 0 and
        current_x < width and
        current_y >= 0 and
        current_y < height):
        if (asteroid_map[current_y][current_x] == '#'):
          found_asteroid = f"{current_x}|{current_y}"
          found_asteroids.add(found_asteroid)
          break
      else:
        in_bounds = False

  return len(found_asteroids)

num_asteroids = 0
for y in range(len(asteroid_map)):
  for x in range(len(asteroid_map[0])):
    if asteroid_map[y][x] == '#':
      _num_asteroids = find_asteroids(f'{x}|{y}', asteroid_map)
      if _num_asteroids > num_asteroids:
        num_asteroids = _num_asteroids
        loc = (x, y)

(x, y) = loc
asteroid_map[y][x] = '@'

print_asteroids()
print(num_asteroids)
print(loc)


