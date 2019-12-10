from math import atan2

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

  def order_slopes(slopes):
    ordered_slopes_list = []

    def _order_slopes(slope):
      (x, y) = split_point(slope)
      return atan2(y, x)

    # x = 0, y = -1
    if '0|-1' in slopes:
      ordered_slopes_list.append('0|-1')
    # x inc y dec
    matching_slopes = []
    for slope in slopes:
      (x, y) = split_point(slope)
      if x > 0 and y < 0:
        matching_slopes.append(slope)
    matching_slopes = sorted(matching_slopes, key = lambda slope: _order_slopes(slope))
    for slope in matching_slopes:
      ordered_slopes_list.append(slope)

    # to x = 1, y = 0
    if '1|0' in slopes:
      ordered_slopes_list.append('1|0')
    # x inc y inc
    matching_slopes = []
    for slope in slopes:
      (x, y) = split_point(slope)
      if x > 0 and y > 0:
        matching_slopes.append(slope)
    matching_slopes = sorted(matching_slopes, key = lambda slope: _order_slopes(slope))
    for slope in matching_slopes:
      ordered_slopes_list.append(slope)

    # to x = 0, y = 1
    if '0|1' in slopes:
      ordered_slopes_list.append('0|1')
    # x dec, y inc
    matching_slopes = []
    for slope in slopes:
      (x, y) = split_point(slope)
      if x < 0 and y > 0:
        matching_slopes.append(slope)
    matching_slopes = sorted(matching_slopes, key = lambda slope: _order_slopes(slope))
    for slope in matching_slopes:
      ordered_slopes_list.append(slope)

    # to x = -1, y = 0
    if '-1|0' in slopes:
      ordered_slopes_list.append('-1|0')
    # x dec, y dec
    matching_slopes = []
    for slope in slopes:
      (x, y) = split_point(slope)
      if x < 0 and y < 0:
        matching_slopes.append(slope)
    matching_slopes = sorted(matching_slopes, key = lambda slope: _order_slopes(slope))
    for slope in matching_slopes:
      ordered_slopes_list.append(slope)

    return ordered_slopes_list

  return order_slopes(reduce_fractions(slopes))

def find_asteroids(point, asteroid_map):
  slopes = find_slopes(point,asteroid_map)
  # print(slopes)
  width = len(asteroid_map[0])
  height = len(asteroid_map)
  (origin_x, origin_y) = split_point(point)
  found_asteroids = []
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
          found_asteroids.append(found_asteroid)
          break
      else:
        in_bounds = False

  return found_asteroids


def vaporize_asteroids(asteroid_list):
  global asteroid_map
  global vaporize_asteroids_count
  for asteroid in asteroid_list:
    (x, y) = split_point(asteroid)
    if asteroid_map[y][x] == '#':
      asteroid_map[y][x] = '.'
      vaporize_asteroids_count += 1
      if vaporize_asteroids_count == 200:
        print(x * 100 + y)
  print_asteroids()

asteroid_map[19][27] = '@'

print_asteroids()

vaporize_asteroids_count = 0
first_round = find_asteroids('27|19', asteroid_map)
# print(first_round)
vaporize_asteroids(first_round)
print(vaporize_asteroids_count)

