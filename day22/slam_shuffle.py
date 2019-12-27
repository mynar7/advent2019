# with open('./input.txt') as _file:
#   inputs = _file.read().splitlines()

# deck = [x for x in range(10007)]

# def deal_into_new_stack(deck):
#   new_deck = deck.copy()
#   new_deck.reverse()
#   return new_deck

# def cut_n_cards(deck, n):
#   new_deck = deck[n:] + deck[:n]
#   return new_deck

# def deal_with_increment_n(deck, n):
#   assert n > 0
#   deck_length = len(deck)
#   new_deck = deck.copy()
#   _deck = deck.copy()
#   _deck.reverse()
#   count_by_n = 0
#   while len(_deck) > 0:
#     index = 0 if count_by_n == 0 else count_by_n % deck_length
#     new_deck[index] = _deck.pop()
#     count_by_n += n
#   return new_deck

# def parse_inputs(inputs, deck):
#   _deck = deck.copy()
#   for command in inputs:
#     command_list = command.split(" ")
#     first_word =  command_list[0]
#     last_word =  command_list[-1]

#     if command == 'deal into new stack':
#       _deck = deal_into_new_stack(_deck)
#     elif first_word == 'cut':
#       n = int(last_word)
#       _deck = cut_n_cards(_deck, n)
#     elif first_word == 'deal' and last_word != 'stack':
#       n = int(last_word)
#       _deck = deal_with_increment_n(_deck, n)

#   return _deck

# new_deck = parse_inputs(inputs, deck)
# print(new_deck.index(2019))

with open('./input.txt') as _file:
  inputs = _file.read().splitlines()

deck_size = 10007

def deal_into_new_stack(position):
  return (deck_size - position - 1) % deck_size

def cut_n_cards(position, n):
  return (position - n) % deck_size

def deal_with_increment_n(position, n):
  assert n > 0
  return (n * position) % deck_size

def parse_inputs(inputs, position):
  _position = position
  for command in inputs:
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

print(parse_inputs(inputs, 2019))