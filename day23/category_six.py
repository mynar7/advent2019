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
  pause_code_given = 0
  relative_base = 0
  while index >= 0:
    if pause_code_given > 1:
      return index
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
      if (inputValue == -1):
        pause_code_given += 1
      program[param1] = inputValue
      index += 2
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
for _ in range(100000):
  inputs.append(0)


class Intcode_computer:
  index = 0
  state = 'INITIAL'
  output_dict = {
    'address': None,
    'X': None,
    'Y': None
  }

  def __init__(self, program, address, send_func):
    self.program = program.copy()
    self.address = address
    self.input_buffer = [address]
    self.send_func = send_func

  def start(self):
    self.state = 'RUNNING'
    self.index = intcode(
      self.program,
      self.inputter,
      self.outputter,
      self.index
    )
    if self.index == 'done':
      self.state = 'HALTED'
    else:
      self.state = 'PAUSED'

  def queue_inputs(self, value):
    self.input_buffer.insert(0, value)

  def inputter(self):
    if len(self.input_buffer) == 0:
      return -1
    else:
      return self.input_buffer.pop()

  def outputter(self, output_value):
    if self.output_dict['address'] is None:
      self.output_dict['address'] = output_value
    elif self.output_dict['X'] is None:
      self.output_dict['X'] = output_value
    elif self.output_dict['Y'] is None:
      self.output_dict['Y'] = output_value

    if (
      self.output_dict['address'] is not None and
      self.output_dict['X'] is not None and
      self.output_dict['Y'] is not None
    ):
      address = self.output_dict['address']
      X = self.output_dict['X']
      Y = self.output_dict['Y']

      self.send_func(address, X, Y)

      self.output_dict['address'] = None
      self.output_dict['X'] = None
      self.output_dict['Y'] = None

class NIC:
  intcode_dict = {}
  NAT = None
  NAT_y_values = set()
  done = False

  def __init__(self):
    for i in range(50):
      self.intcode_dict[i] = Intcode_computer(inputs, i, self.send_to_address)
    for i in range(50):
      self.intcode_dict[i].start()
    def run_loop():
      n = 0
      while n < 10:
        for i in range(50):
          if self.intcode_dict[i].state == 'PAUSED':
            self.intcode_dict[i].start()
        n += 1
      if self.NAT[1] not in self.NAT_y_values:
        self.NAT_y_values.add(self.NAT[1])
        self.send_to_address(0, self.NAT[0], self.NAT[1])
        run_loop()
      else:
        print(f"PT2: {self.NAT[1]}")

    run_loop()

  def send_to_address(self, address, x, y):
    if address == 255:
      if self.NAT is None:
        print(f'PT1: {y}')
      self.NAT = (x, y)
      return
    # print(f"address {address}, x {x}, y {y}")
    self.intcode_dict[address].queue_inputs(x)
    self.intcode_dict[address].queue_inputs(y)

nic = NIC()