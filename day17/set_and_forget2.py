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
  for _ in range(10000):
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

inputs = [int(x) for x in strInputs]

inputs[0] = 2

movement_inputs = list('A,A,B,C,B,C,B,C,C,A\n')
mvmt_A = list('L,10,R,8,R,8\n')
mvmt_B = list('L,10,L,12,R,8,R,10\n')
mvmt_C = list('R,10,L,12,R,10\n')
video = list('y\n')

input_list = movement_inputs + mvmt_A + mvmt_B + mvmt_C + video

input_list.reverse()

def inputter():
  global input_list
  return ord(input_list.pop())

# print inputs into map
output_string = ""
lines_printed = 0
first_print = True

def outputter(charCode):

  if charCode > 999:
    print(f"Dust collected: {charCode}")
    return

  global output_string, lines_printed, first_print
  if charCode == 10:
    lines_printed += 1
  output_string += chr(charCode) + ' ' if charCode != 10 else chr(charCode)

  if lines_printed == 48 and first_print:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(output_string)
    lines_printed = 0
    output_string = ""
    first_print = False
  elif lines_printed == 42 and not first_print:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(output_string)
    lines_printed = 0
    output_string = ""

intcode(inputs, inputter, outputter)

