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


def intcode(program, inputMethod, outputMethod = print, index = 0):
  while index >= 0:
    (opcode, param1, param2, param3) = getInputs(program, index)
    # print(f'opcode {opcode}')
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
      return index
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

# should output 139629729
# sequence = [9,8,7,6,5]
# inputs = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# should output 139629729
# sequence = [9,7,8,5,6]
# inputs = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]



# first input is phase setting
# second input is input signal
# first input to first amplifier is 0

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

def chainOutput(sequence, initialSignal = 0):
  signal = initialSignal
  ampDicts = []

  for i in range(len(sequence)):
    # make dictionary for each amplifier
    ampDict = {
      'inputs': inputs.copy(),
      'buffer': [],
      'index': 0,
    }
    phase = sequence[i]
    ampDict['phase'] = phase
    if i == 0:
      ampDict['buffer'].append(signal)
    ampDict['buffer'].append(phase)

    # create closure to ensure reference to correct buffer
    def inputMethod():
      index = i
      def _inputMethod():
        buffer = ampDicts[index]['buffer']
        if len(buffer) > 0:
          return buffer.pop()
        return False
      return _inputMethod

    # create closure to ensure reference to correct buffer
    def outputMethod():
      index = len(ampDicts) + 1 if len(ampDicts) + 1 < 5 else 0
      def _outputMethod(newSignal):
        buffer = ampDicts[index]['buffer']
        buffer.insert(0, newSignal)
      return _outputMethod

    ampDict['inputMethod'] = inputMethod()
    ampDict['outputMethod'] = outputMethod()

    ampDicts.append(ampDict)

  ampsRun = 0
  running = True
  while running:
    ampDict = ampDicts[ampsRun % 5]
    output = intcode(
      ampDict['inputs'],
      ampDict['inputMethod'],
      ampDict['outputMethod'],
      ampDict['index']
    )
    # final amp outputs halt
    if (output == 'done'):
      running = False
    else:
      ampDict['index'] = output
    ampsRun +=1
  # because last amp's output is tied to input of first amp,
  # print that first amp's buffer
  return ampDicts[0]['buffer'][0]

signal = 0
sequences = permutations([5,6,7,8,9])
for sequence in sequences:
  output = chainOutput(sequence)
  if (output > signal):
    signal = output

# signal = chainOutput(sequence)

print(signal)
