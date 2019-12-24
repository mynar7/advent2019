import os

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
  # 99 / 3 opcodes don't care about immediate v position mode
  if (opcode == 99):
    return (opcode, None, None, None)

  # if (opcode == 3):
  #   param1 = program[index + 1]
  #   return (opcode, param1, None, None)

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
  for _ in range(100000):
    program.append(0)
  relative_base = 0
  while index >= 0:
    # print(index)
    (opcode, param1, param2, param3) = getInputs(program, index, relative_base)
    # print(f'opcode {opcode}, p1 {param1} p2 {param2} p3 {param3}')
    # print(program)
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
      # if (inputValue is not False):
      program[param1] = inputValue
      index += 2
      # else:
      #   return index
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


def detect_beam(x:int = 0, y:int = 0):
  coords = [y, x]
  beam_result = None

  def inputter():
    return coords.pop()

  def outputter(_beam_result):
    nonlocal beam_result
    beam_result = _beam_result

  intcode(inputs.copy(), inputter, outputter)
  return True if beam_result == 1 else False

x = 50
y = 50

found_square_top_left = False

while not found_square_top_left:
  beam_detected = detect_beam(x, y)
  if beam_detected:
    beam_start_left = (x, y)
    right_side_in_beam = detect_beam(x + 99, y)
    while right_side_in_beam:
      bottom_left_in_beam = detect_beam(x, y + 99)
      if bottom_left_in_beam:
        found_square_top_left = True
        print(x * 10000 + y)
      x += 1
      right_side_in_beam = detect_beam(x + 99, y)
    y += 1
  else:
    x += 1