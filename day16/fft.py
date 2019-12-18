with open('./input.txt') as _file:
  input_string = _file.read()

# input_string = "12345678"
# input_string = "80871224585914546619083218645595" # Should output 24176176
# input_string = "19617804207202209144916044189917" # Should output 73745418
# input_string = "69317163492948606335995924319873" # Should output 52432133

signal = [int(char) for char in input_string]
base_pattern = [0, 1, 0, -1]

phases = 100
# phases = 1

signal_length = len(signal)
for _ in range(phases):
  new_signal = []
  for i in range(signal_length):
    new_value = 0
    for j in range(i, signal_length):
      base_pattern_index = (j + 1) // (i + 1) % len(base_pattern)
      # print(base_pattern[base_pattern_index])
      phase_value = base_pattern[base_pattern_index]
      new_value += signal[j] * phase_value
    new_signal.append(abs(new_value) % 10)
  signal = new_signal

signal = [str(x) for x in signal]
signal = "".join(signal)
signal = signal[:8]
print(f"signal after {phases} phases: {signal}")
