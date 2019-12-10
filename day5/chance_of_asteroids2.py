with open('./input.txt', 'r') as _file:
  strInputs = _file.read().split(',')

inputs = list(map(lambda str: int(str), strInputs))

# test input that takes one number, outputs 1000 if num is 9, 999 below 8, 1001 above 8
# inputs = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
#           0  1 2 3  4   5 6  7    8   9
# inputs = [101,-1,8,8,1005,8,0,104,1000,99]

def getInputs(program, index):
  opcode = program[index]
  # 99 / 3 opcodes don't care about immediate v position mode
  if (opcode == 99):
    return (opcode, None, None, None)

  if (opcode == 3):
    param1 = program[index + 1]
    return (opcode, param1, None, None)

  opcode = str(opcode)

  if (len(opcode) < 3):
    # opcode < 3 means no modes given, all should be 0
    parsedOpcode = int(opcode)
    modes = '00'
  else:
    # opcode is last 2 digits
    parsedOpcode = int(opcode[-2:])
    if (len(opcode) == 3):
      modes = opcode[0] + '0'
    if (len(opcode) == 4):
      # grab all but last 2
      modes = opcode[:-2]
      # reverse digits so they're in order of params left
      modes = modes[::-1]

  if (parsedOpcode < 3 or parsedOpcode > 6):
    param1 = program[index + 1]
    param2 = program[index + 2]
    param3 = program[index + 3]
    param1 =  param1 if int(modes[0]) == 1 else program[param1]
    param2 =  param2 if int(modes[1]) == 1 else program[param2]
    return (parsedOpcode, param1, param2, param3)

  if (parsedOpcode == 5 or parsedOpcode == 6):
    param1 = program[index + 1]
    param2 = program[index + 2]
    param1 =  param1 if int(modes[0]) == 1 else program[param1]
    param2 =  param2 if int(modes[1]) == 1 else program[param2]
    return (parsedOpcode, param1, param2, None)
  if (parsedOpcode == 4):
    param1 = program[index + 1]
    param1 =  param1 if int(modes[0]) == 1 else program[param1]
    return (parsedOpcode, param1, None, None)


def intcode(program, inputValue, index = 0, outputMethod = print):
  while index >= 0:
    (opcode, param1, param2, param3) = getInputs(program, index)

    if opcode == 99:
      index = -1

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
      program[param1] = inputValue
      index += 2
    # output
    if opcode == 4:
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

intcode(inputs, 5)