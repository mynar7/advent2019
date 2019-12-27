with open('./input.txt') as _file:
  inputs = _file.read().splitlines()

deck_size = 10007

def deal_into_new_stack(position):
  return (deck_size - position - 1) % deck_size

def cut_n_cards(position, n):
  return (position + n) % deck_size

def deal_with_increment_n(position, n):
  assert n > 0
  return pow(n, deck_size - 2, deck_size) * position % deck_size

def parse_inputs(inputs, position):
  _position = position
  for command in inputs[::-1]:
    command_list = command.split(" ")
    first_word =  command_list[0]
    last_word =  command_list[-1]

    if command == 'deal into new stack':
      position = deal_into_new_stack(position)
    elif first_word == 'cut':
      n = int(last_word)
      position = cut_n_cards(position, n)
    elif first_word == 'deal' and last_word != 'stack':
      n = int(last_word)
      position = deal_with_increment_n(position, n)

  return position

print(parse_inputs(inputs, 6978))
