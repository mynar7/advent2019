const fs = require('fs')

fs.readFile('./input.txt', 'UTF-8', function(err, data) {
  if (err) return console.log(err)
  const valuesArr = data.split("\r\n")
  const answer = valuesArr
  .map(str => Number(str))
  .reduce((acc, current) => acc + Math.floor(current / 3) - 2, 0)
  console.log(answer);
})

fs.readFile('./input.txt', 'UTF-8', function(err, data) {
  if (err) return console.log(err)
  const valuesArr = data.split("\r\n")
  function getFuel(num) {
    const fuel = Math.floor(num / 3) - 2
    return fuel > 0 ? fuel + getFuel(fuel) : 0
  }
  const answer = valuesArr
  .map(str => Number(str))
  .reduce((acc, current) => acc + getFuel(current), 0)
  console.log(answer);
})
