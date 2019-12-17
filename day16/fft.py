with open('./input.txt') as _file:
  input_string = _file.read()

# input_string = "12345678"
# input_string = "80871224585914546619083218645595" # Should output 24176176
# input_string = "19617804207202209144916044189917" # Should output 73745418
# input_string = "69317163492948606335995924319873" # Should output 52432133

signal = [int(char) for char in input_string]
# print(signal)
base_pattern = [0, 1, 0, -1]

phases = 100
# phases = 4

# loop phases
for i in range(1, phases + 1):
  new_signal = []
  # in 5346: 1, then 2, then 3
  for signal_digit in range(1, len(signal) + 1):
    new_value = 0
    # make phase pattern for this digit
    phase_pattern = []
    for j in range(len(base_pattern)):
      phase_pattern_number = base_pattern[j]
      for _ in range(signal_digit):
        phase_pattern.append(phase_pattern_number)
    # loop over entire signal for this digit in the phase
    for index, num in enumerate(signal):
      phase_index = (index + 1) % len(phase_pattern)
      phase_value = phase_pattern[phase_index]
      new_value += num * phase_value
    new_signal.append(abs(new_value) % 10)
  signal = new_signal

signal = [str(x) for x in signal]
signal = "".join(signal)
signal = signal[:8]
print(f"signal after {phases} phases: {signal}")
