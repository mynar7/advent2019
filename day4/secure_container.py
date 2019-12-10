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

def checkDubs(num):
  pword = str(num)
  passes = False
  lastNum = int(pword[0])
  for i in range(1, len(pword)):
    currentNum = int(pword[i])
    if (currentNum == lastNum):
      passes = True
      break
    lastNum = currentNum
  return passes

for i in range(lowerLimit, upperLimit + 1):
  passIncreasing = checkIncreasing(i)
  passDubs = checkDubs(i)
  if (passIncreasing and passDubs):
    numPossible += 1

print(numPossible)