with open('./input.txt', 'r') as _file:
  input_string = _file.read()

# input_string = '0222112222120000'
inputs = []
for char in input_string:
  num = int(char)
  inputs.append(num)

height = 6
# height = 2
width = 25
# width = 2
# image = [[2, 2], [2,2]]
# image = [[5, 6], [7,8]]
# make an empty 2d list without shared reference madness
image = [[None for _ in range(width)] for _ in range(height)]
pixelIndex = 0
row = 0
col = 0
while pixelIndex < len(inputs):
  if image[row][col] == 2 or image[row][col] is None:
    image[row][col] = inputs[pixelIndex]
  col += 1
  if col % width == 0:
    col = 0
    row += 1
    if row % height == 0:
      row = 0
  pixelIndex += 1

for row in image:
  for char in row:
    print(char, end=" ")
  print('\r')