with open('./input.txt', 'r') as _file:
  strInputs = _file.read().split(',')

inputs = list(map(lambda str: int(str), strInputs))

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

  if (parsedOpcode < 3):
    param1 = program[index + 1]
    param2 = program[index + 2]
    param3 = program[index + 3]
    param1 =  param1 if int(modes[0]) == 1 else program[param1]
    param2 =  param2 if int(modes[1]) == 1 else program[param2]
    return (parsedOpcode, param1, param2, param3)

  if (parsedOpcode == 4):
    param1 = program[index + 1]
    param1 =  param1 if int(modes[0]) == 1 else program[param1]
    return (parsedOpcode, param1, None, None)


def intcode(program, inputValue, index = 0, outputMethod = print):
  (opcode, param1, param2, param3) = getInputs(program, index)

  if opcode == 99:
    return

  if opcode == 1:
    program[param3] = param1 + param2
    index += 4
    return intcode(program, inputValue, index, outputMethod)
  if opcode == 2:
    program[param3] = param1 * param2
    index += 4
    return intcode(program, inputValue, index, outputMethod)
  if opcode == 3:
    # take the input and save it to position
    program[param1] = inputValue
    index += 2
    return intcode(program, inputValue, index, outputMethod)
  if opcode == 4:
    # take parameter and output it
    outputMethod(param1)
    # do whatever with output
    index += 2
    return intcode(program, inputValue, index, outputMethod)

intcode(inputs, 1)