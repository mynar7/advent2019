with open('./input.txt') as _file:
  (wire1, wire2) = _file.read().splitlines()

wire1 = wire1.split(',')
# wire1 = ['R8','U5','L5','D3']

wire2 = wire2.split(',')
# wire2 = ['U7','R6','D4','L4']

# create dictionaries for wire1/2 to track info
wire1info = {
  'hLines': [],
  'vLines': [],
  'pos': [0, 0]
}
wire2info = {
  'hLines': [],
  'vLines': [],
  'pos': [0, 0]
}

intersections = []

def splitInput(input):
  direction = input[0]
  amount = int(input[1:])
  return (direction, amount)

# move function determines the line segment created
# by moving from the current position to the new position
# after determining direction
# then adds that line segment to the wire1/2info object that
# was passed in
def move(input, info):
  (direction, amount) = splitInput(input)
  origin = info['pos']
  # R means positive change in X
  # creates horizontal line
  if direction == 'R':
    # endpoint will equal [currentX + amount, currentY]
    end = [info['pos'][0] + amount, info['pos'][1]]
    # new line will be [[startx, starty], [endx, endy]]
    newLine = [origin, end]
    # add to wire's horizontal lines
    info['hLines'].append(newLine)

  # L means negative change in X
  if direction == 'L':
    # endpoint will equal [currentX - amount, currentY]
    end = [info['pos'][0] - amount, info['pos'][1]]
    newLine = [origin, end]
    info['hLines'].append(newLine)
  # U means positive change in Y

  if direction == 'U':
    end = [info['pos'][0], info['pos'][1] + amount]
    newLine = [origin, end]
    info['vLines'].append(newLine)
  # D means negative change in Y

  if direction == 'D':
    end = [info['pos'][0], info['pos'][1] - amount]
    newLine = [origin, end]
    info['vLines'].append(newLine)

  # lastly update the current position to the end point
  info['pos'] = end

# loop over instructions for each wire
for instruction in wire1:
  move(instruction, wire1info)
for instruction in wire2:
  move(instruction, wire2info)

# loop over line segments and compare horizontal to vertical in each
# dictionary
for hLine in wire1info['hLines']:
  for vLine in wire2info['vLines']:
    # if horiz line's y is between vertical line's y values and
    # vertical line's x is between horizontal line's x values
    if ((hLine[0][1] <= max(vLine[0][1], vLine[1][1]) and
    hLine[0][1] >= min(vLine[0][1], vLine[1][1])) and
    (vLine[0][0] <= max(hLine[0][0], hLine[1][0]) and
    vLine[0][0] >= min(hLine[0][0], hLine[1][0]))):
      # check that point is not origin
      if(vLine[0][0] != 0 and hLine[0][1] != 0):
        intersections.append([vLine[0][0], hLine[0][1]])

for hLine in wire2info['hLines']:
  for vLine in wire1info['vLines']:
    # same check as above, should refactor to DRY
    if ((hLine[0][1] <= max(vLine[0][1], vLine[1][1]) and
    hLine[0][1] >= min(vLine[0][1], vLine[1][1])) and
    (vLine[0][0] <= max(hLine[0][0], hLine[1][0]) and
    vLine[0][0] >= min(hLine[0][0], hLine[1][0]))):
      # check that point is not origin
      # also same as above
      if(vLine[0][0] != 0 and hLine[0][1] != 0):
        intersections.append([vLine[0][0], hLine[0][1]])

# loop over intersections
# calc manhattan distance against origin, which is the absolute
# value of the x and y of an intersection added together
for sect in intersections:
  newAnswer = abs(sect[0]) + abs(sect[1])
  if ('answer' in globals() and newAnswer < answer):
    answer = newAnswer
  else:
    answer = newAnswer

print(f'part 1 answer: {answer}')

