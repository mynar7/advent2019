with open('./input.txt', 'r') as _file:
  strInputs = _file.read().split(',')

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


def intcode(program, inputValues, outputMethod = print):
  index = 0
  currentInputIndex = 0
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
      program[param1] = inputValues[currentInputIndex]
      currentInputIndex += 1
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

inputs = list(map(lambda str: int(str), strInputs))

# # should output 43210
# sequence = [4,3,2,1,0]
# inputs = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]

# #should output 54321
# sequence = [0,1,2,3,4]
# inputs = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]

# # should output 65210
# sequence = [1,0,4,3,2]
# inputs = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

# first input is phase setting
# second input is input signal
# first input to first amplifier is 0

# find all permutations of a sequence of numbers
def permutations(arr):
  if len(arr) == 1:
    return [arr]
  combos = []
  for num in arr:
    remainingNums = list(filter(lambda x: x != num, arr))
    allCombinations = permutations(remainingNums)
    for combo in allCombinations:
      combo.insert(0, num)
      combos.append(combo)
  return combos

# find max signal, let each amp pull from signal in higher-level scope
def getOutput(sequence, initialSignal = 0):
  signal = initialSignal
  def setSignal(newSignal):
    nonlocal signal
    signal = newSignal
  for num in sequence:
    inputCopy = inputs.copy()
    intcode(inputCopy, [num, signal], setSignal)
  return signal

sequences = permutations([0,1,2,3,4])
signal = 0

# loop over all sequences to find max output
for sequence in sequences:
  output = getOutput(sequence)
  if (output > signal):
    signal = output

print(signal)