# credit: https://github.com/zedrdave/advent_of_code/blob/master/2019/22/__main__.py

deck_size = 119315717514047
n = 101741582076661
pos = 2020
shuffles = { 'deal with increment ': lambda x,deck_size,a,b: (a*x % deck_size, b*x % deck_size),
         'deal into new stack': lambda _,deck_size,a,b: (-a % deck_size, (deck_size-1-b) % deck_size),
         'cut ': lambda x,deck_size,a,b: (a, (b-x) % deck_size) }
a,b = 1,0
with open('./input.txt') as f:
  for s in f.read().strip().split('\n'):
    for name, fn in shuffles.items():
      if s.startswith(name):
        arg = int(s[len(name):]) if name[-1] == ' ' else 0
        a,b = fn(arg, deck_size, a, b)
        break

r = (b * pow(1-a, deck_size-2, deck_size)) % deck_size
print(f"Card at #{pos}: {((pos - r) * pow(a, n*(deck_size-2), deck_size) + r) % deck_size}")