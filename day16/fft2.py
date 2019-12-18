with open('./input.txt') as _file:
  input_string = _file.read()

# input_string = "12345678"

# input_string = "03036732577212944063491565474664" # becomes 84462026.
# input_string = "02935109699940807407585447034323" # becomes 78725270.
# input_string = "03081770884921959731165446850517" # becomes 53553731.

amount_to_skip = int(input_string[:7])
new_input_string = ""
for _ in range(10000):
  new_input_string += input_string

input_string = new_input_string
input_string = input_string[amount_to_skip:]

signal = [int(char) for char in input_string]

phases = 100

for _ in range(phases):
  new_value = None
  second_half_signal = []
  # print('phase second half')
  for i in range(len(signal) - 1, -1, -1):
    if new_value is None:
      new_value = signal[i]
    else:
      new_value += signal[i]
    second_half_signal.append(new_value % 10)
  second_half_signal.reverse()
  signal = second_half_signal

signal = [str(x) for x in signal]
signal = "".join(signal)
signal = signal[:8]
print(f"signal after {phases} phases: {signal}")

