input = '347312-805915'

lowerLimit = int(input.split('-')[0])
upperLimit = int(input.split('-')[1])

numPossible = 0

def checkIncreasing(num):
  pword = str(num)
  passes = False
  highestNum = int(pword[0])
  for i in range(1, len(pword)):
    currentNum = int(pword[i])
    if(currentNum >= highestNum):
      passes = True
      highestNum = currentNum
    else:
      passes = False
      break
  return passes

def checkOneDub(num):
  pword = str(num)
  digitCount = 1
  prevDigit = pword[0]
  for i in range(1, len(pword)):
    current = pword[i]
    if (current == prevDigit):
      digitCount += 1
    else:
      if (digitCount == 2):
        return True
      digitCount = 1
    prevDigit = current
  return digitCount == 2


for i in range(lowerLimit, upperLimit + 1):
  passIncreasing = checkIncreasing(i)
  passOneDub = checkOneDub(i)
  if (passIncreasing and passOneDub):
    numPossible += 1

print(numPossible)