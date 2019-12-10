with open('./input.txt', 'r') as _file:
  str = _file.read()

inputs = []

for char in str:
  num = int(char)
  inputs.append(num)

# 25 pixels wide, 6 pixels tall
# 1 layer = 25 * 6 = 150

layers = []
for i in range(len(inputs)):
  pixel = inputs[i]
  # if we hit a multiple of 150, we're at a new layer
  if i % 150 == 0:
    layers.append([])
  layers[-1].append(pixel)

# count 0s, 1s, and 2s in each layer
for layer in layers:
  num0 = 0
  num1 = 0
  num2 = 0
  for pixel in layer:
    if (pixel is 0):
      num0 += 1
    if (pixel is 1):
      num1 += 1
    if (pixel is 2):
      num2 += 1
  if ('minZeros' not in globals() or num0 < minZeros):
    minZeros = num0
    onesTimesTwos = num1 * num2
    # print(f'minZeros {minZeros} num1 {num1} num2 {num2}')

print(onesTimesTwos)
