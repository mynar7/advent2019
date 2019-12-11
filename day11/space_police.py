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
  if (opcode == 99):
    return (opcode, None, None, None)

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
    (opcode, param1, param2, param3) = getInputs(program, index, relative_base)
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

# after a turn, robot moves forward one panel
class PaintRobot:
  facing = 'UP'
  positionX = 0
  positionY = 0
  painted_panels = {'0|0': 1}

  painting = True

  def print_panel_count(self):
    # print(self.painted_panels)
    print(len(self.painted_panels))

  def print_current_position(self):
    print(f"current position {self.positionX}, {self.positionY}")

  def print_picture(self):
    maxX = 0
    maxY = 0
    for position in self.painted_panels:
      (_x, _y) = self.split_point(position)
      x = int(_x)
      y = int(_y)
      if x > maxX:
        maxX = x
      if y > maxY:
        maxY = y

    painting = [['.' for _ in range(maxX + 1)] for _ in range(maxY + 1)]
    for position in self.painted_panels:
      (x, y) = self.split_point(position)
      paint = self.painted_panels[position]
      paint = '#' if paint == 1 else '.'
      painting[y][x] = paint
    for row in painting:
      _row = []
      for char in row:
        _row.append(str(char))
      print(" ".join(_row))

  def get_panel_color(self):
    x = self.positionX
    y = self.positionY
    position = f"{x}|{y}"
    # self.print_current_position()
    if position in self.painted_panels:
      return self.painted_panels[position]
    else:
      return 0

  def split_point(self, point):
    (x, y) = point.split('|')
    return (int(x), int(y))

  def receive_input(self, intcode_input):
    if self.painting:
      self.paint(intcode_input)
      self.painting = False
    else:
      self.move(intcode_input)
      self.painting = True

  def paint(self, color):
    x = self.positionX
    y = self.positionY
    position = f"{x}|{y}"
    self.painted_panels[position] = color

  # 0 means turn left, 1 means turn right
  def move(self, direction):
    if self.facing == 'UP':
      self.facing = 'LEFT' if direction == 0 else 'RIGHT'
    elif self.facing == 'LEFT':
      self.facing = 'DOWN' if direction == 0 else 'UP'
    elif self.facing == 'RIGHT':
      self.facing = 'UP' if direction == 0 else 'DOWN'
    elif self.facing == 'DOWN':
      self.facing = 'RIGHT' if direction == 0 else 'LEFT'

    if self.facing == 'UP':
      dx = 0
      dy = -1
    elif self.facing == 'DOWN':
      dx = 0
      dy = 1
    elif self.facing == 'LEFT':
      dx = -1
      dy = 0
    elif self.facing == 'RIGHT':
      dx = 1
      dy = 0

    self.positionX += dx
    self.positionY += dy

bot1 = PaintRobot()

intcode(inputs, bot1.get_panel_color, bot1.receive_input)
bot1.print_panel_count()
bot1.print_current_position()
bot1.print_picture()
