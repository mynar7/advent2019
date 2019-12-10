with open('./input.txt') as _file:
  (wire1, wire2) = _file.read().splitlines()

wire1 = wire1.split(',')
# wire1 = ['R8','U5','L5','D3']
# wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
# wire1 = ['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51']

wire2 = wire2.split(',')
# wire2 = ['U7','R6','D4','L4']
# wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
# wire2 = ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']

wire1info = {
  'hLines': [],
  'vLines': [],
  'steps': 0,
  'lastSteps': 0,
  'pos': [0, 0],
  'lastpos': [0, 0]
}
wire2info = {
  'hLines': [],
  'vLines': [],
  'steps': 0,
  'lastSteps': 0,
  'pos': [0, 0],
  'lastpos': [0, 0]
}

intersections = []

def splitInput(input):
  direction = input[0]
  amount = int(input[1:])
  return (direction, amount)

def move(input, info):
  (direction, amount) = splitInput(input)
  info['lastSteps'] = amount
  origin = info['pos']
  if direction == 'R':
    end = [info['pos'][0] + amount, info['pos'][1]]
    newPoint = [origin, end]
    info['hLines'].append(newPoint)
  if direction == 'L':
    end = [info['pos'][0] - amount, info['pos'][1]]
    newPoint = [origin, end]
    info['hLines'].append(newPoint)

  if direction == 'U':
    end = [info['pos'][0], info['pos'][1] + amount]
    info['vLines'].append([origin, end])
  if direction == 'D':
    end = [info['pos'][0], info['pos'][1] - amount]
    info['vLines'].append([origin, end])
  info['pos'] = end
  info['lastpos'] = origin

for instruction in wire1:
  move(instruction, wire1info)
for instruction in wire2:
  move(instruction, wire2info)

for hLine in wire1info['hLines']:
  for vLine in wire2info['vLines']:
    if ((hLine[0][1] <= max(vLine[0][1], vLine[1][1]) and
    hLine[0][1] >= min(vLine[0][1], vLine[1][1])) and
    (vLine[0][0] <= max(hLine[0][0], hLine[1][0]) and
    vLine[0][0] >= min(hLine[0][0], hLine[1][0]))):
      # check that point is not origin
      if(vLine[0][0] != 0 and hLine[0][1] != 0):
        intersections.append([vLine[0][0], hLine[0][1]])

for hLine in wire2info['hLines']:
  for vLine in wire1info['vLines']:
    if ((hLine[0][1] <= max(vLine[0][1], vLine[1][1]) and
    hLine[0][1] >= min(vLine[0][1], vLine[1][1])) and
    (vLine[0][0] <= max(hLine[0][0], hLine[1][0]) and
    vLine[0][0] >= min(hLine[0][0], hLine[1][0]))):
      # check that point is not origin
      if(vLine[0][0] != 0 and hLine[0][1] != 0):
        intersections.append([vLine[0][0], hLine[0][1]])

for sect in intersections:
  newAnswer = abs(sect[0]) + abs(sect[1])
  if ('answer' in globals() and newAnswer < answer):
    answer = newAnswer
  else:
    answer = newAnswer

print(f"part 1 answer: {answer}")

# reinitialize values since we're going to retrace our steps
# now that we have all the interesections
# add in step count, previous step count, last position, and last step count
wire1info = {
  'hLines': [],
  'vLines': [],
  'steps': 0,
  'lastSteps': 0,
  'pos': [0, 0],
  'lastpos': [0, 0]
}
wire2info = {
  'hLines': [],
  'vLines': [],
  'steps': 0,
  'lastSteps': 0,
  'pos': [0, 0],
  'lastpos': [0, 0]
}

# checks if the last line segment created
# passes through any intersections
# then calculates the distance from the origin of that segment
# to the intersection and adds it to the steps count in the wire1/2info dict
def checkIntersections(info):
  pos = info['pos']
  lastpos = info['lastpos']
  # last move made a vertical line
  if (pos[0] == lastpos[0]):
    x = pos[0]
    ystart = min(pos[1], lastpos[1])
    yend = max(pos[1], lastpos[1])
    for sect in intersections:
      # if x value of intersection is the same as this vertical line
      # and intersection's y value is between this segment's y values
      # then we crossed through the intersection on the last move
      if (sect[0] == x and (sect[1] >= ystart and sect[1] <= yend)):
        # distance from where we started our last line segment and our
        # intersection is equal to intersection's y - last position's y
        stepsToIntersection = abs(sect[1] - lastpos[1])
        # check if our dict of intersections with amount contains this
        # amount of steps
        if(f"{sect[0]}|{sect[1]}" not in intersectionsWithAmount):
          # if it doesnt, add a new rec
          intersectionsWithAmount[f"{sect[0]}|{sect[1]}"] = {'sect': sect, 'amount': info['steps'] + stepsToIntersection }
        else:
          # if it does, add the new amount of steps to the old rec's stepcount
          intersectionsWithAmount[f"{sect[0]}|{sect[1]}"]['amount'] += info['steps'] + stepsToIntersection
  # last move made a horizontal line
  if (pos[1] == lastpos[1]):
    y = pos[1]
    xstart = min(lastpos[0], pos[0])
    xend = max(lastpos[0], pos[0])
    # if y value of intersection is the same as this horizontal line
    # and intersection's x value is between this segment's x values
    # then we crossed through the intersection on the last move
    for sect in intersections:
      if (sect[1] == y and (sect[0] >= xstart and sect[0] <= xend)):
        # distance from where we started our last line segment and our
        # intersection is equal to intersection's x - last position's x
        stepsToIntersection = abs(sect[0] - lastpos[0])
        # check if our dict of intersections with amount contains this
        # amount of steps
        if(f"{sect[0]}|{sect[1]}" not in intersectionsWithAmount):
          # if it doesnt, add a new rec
          intersectionsWithAmount[f"{sect[0]}|{sect[1]}"] = {'sect': sect, 'amount': info['steps'] + stepsToIntersection}
        else:
          # if it does, add the new amount of steps to the old rec's stepcount
          intersectionsWithAmount[f"{sect[0]}|{sect[1]}"]['amount'] += info['steps'] + stepsToIntersection

# empty dict to hold our intersection values with amounts
intersectionsWithAmount = {}

# re-loop over instructions for each wire
# total and update amount of steps after each move/intersection check
for instruction in wire1:
  move(instruction, wire1info)
  checkIntersections(wire1info)
  wire1info['steps'] += wire1info['lastSteps']

for instruction in wire2:
  move(instruction, wire2info)
  checkIntersections(wire2info)
  wire2info['steps'] += wire2info['lastSteps']

# loop over our intersections with amounts dictionary
for key in intersectionsWithAmount:
  # check if we have a steps variable in global scope
  # if not, first amount is our new lowest amount
  if 'steps' not in globals():
    steps = intersectionsWithAmount[key]['amount']
  else:
    # else check if next amount is lower, if so it's the new lowest
    if (steps > intersectionsWithAmount[key]['amount']):
      steps = intersectionsWithAmount[key]['amount']

print(f'part 2 answer: {steps}')