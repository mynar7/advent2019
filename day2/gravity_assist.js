const fs = require('fs')

const strInput = fs.readFileSync('./input.txt', 'UTF-8')
const numInput = strInput.split(',').map(str => Number(str))

function intcode(arr, index = 0) {
  const opcode = arr[index]
  if (opcode === 99) return arr[0]
  const num1Index = arr[index + 1]
  const num2Index = arr[index + 2]
  const answerIndex = arr[index + 3]
  if (opcode === 1) {
    arr[answerIndex] = arr[num1Index] + arr[num2Index]
    index += 4
    return intcode(arr, index)
  }
  if (opcode === 2) {
    arr[answerIndex] = arr[num1Index] * arr[num2Index]
    index += 4
    return intcode(arr, index)
  }
}

function setIntcode(input, pos1, pos2) {
  inputCopy = input.map(x => x)
  inputCopy[1] = pos1
  inputCopy[2] = pos2
  return intcode(inputCopy)
}

// solution 1
console.log(setIntcode(numInput, 12, 2));

// solution 2

for(let i = 0; i < 100; i++) {
  for(let j = 0; j < 100; j++) {
    if (setIntcode(numInput, i, j) === 19690720) {
      console.log(100 * i + j)
    }
  }
}

