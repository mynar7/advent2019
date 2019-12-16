from math import ceil

with open('./input.txt') as _file:
  inputs = _file.read()

# example 3
# inputs = """157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

# example 4
# inputs = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
# 17 NVRVD, 3 JNWZP => 8 VPVL
# 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
# 22 VJHF, 37 MNCFX => 5 FWMGM
# 139 ORE => 4 NVRVD
# 144 ORE => 7 JNWZP
# 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
# 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
# 145 ORE => 6 MNCFX
# 1 NVRVD => 8 CXFTF
# 1 VJHF, 6 MNCFX => 4 RFSQX
# 176 ORE => 6 VJHF"""

# example 5
# inputs = """171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX"""

formulas = {}

for line in inputs.splitlines():
  (molecules, molecule) = line.split(' => ')
  (amount, molecule) = molecule.split(' ')
  formulas[molecule] = { "min_amount": int(amount), "formula": {} }
  for ingredient in molecules.split(', '):
    (amount, ingredient) = ingredient.split(' ')
    formulas[molecule]["formula"][ingredient] = int(amount)


# for formula in formulas.items():
#   print(formula)

def get_cost_and_extra(element, amount):
  min_amount = formulas[element]['min_amount']
  times_to_run = ceil(amount / min_amount)
  final_amount = times_to_run * min_amount
  if final_amount > amount:
    extra_amount = final_amount - amount
  else:
    extra_amount = 0

  cost = {}
  for ingredient in formulas[element]['formula']:
    cost[ingredient] = formulas[element]['formula'][ingredient] * times_to_run

  return ( cost, extra_amount )

def reduce_formula(element, amount):
  ( cost, _ ) = get_cost_and_extra(element, amount)
  total_ore = 0
  extras = {}
  while True:
    # print(f"cost: {cost}, extras: {extras}")
    for element in cost:
      if element in extras:
        if extras[element] > cost[element]:
          extras[element] -= cost[element]
          del cost[element]
          break
        elif extras[element] < cost[element]:
          cost[element] -= extras[element]
          del extras[element]
        else:
          del cost[element]
          del extras[element]
          break

      if 'ORE' in formulas[element]['formula']:
        (element_cost, extra) = get_cost_and_extra(element, cost[element])
        total_ore += element_cost['ORE']
        if extra > 0:
          if element in extras:
            extras[element] += extra
          else:
            extras[element] = extra
        del cost[element]
        break
      else:
        (element_cost, extra) = get_cost_and_extra(element, cost[element])
        del cost[element]
        if extra > 0:
          if element in extras:
            extras[element] += extra
          else:
            extras[element] = extra
        for ingredient in element_cost:
          if ingredient in cost:
            cost[ingredient] += element_cost[ingredient]
          else:
            cost[ingredient] = element_cost[ingredient]
        break
    if len(cost) == 0:
      return total_ore

collected_ore = 1000000000000

def guess_fuel(ore):
  ore_cost = 0
  fuel = 1
  magnitude = 2
  while ore_cost < ore:
    fuel *= magnitude
    ore_cost = reduce_formula('FUEL', fuel)
    if ore_cost > ore:
      # gone over
      # fuel overage amount = fuel
      # prev fuel amount = fuel / magnitude
      print(f"guessing lower {fuel // magnitude}, upper {fuel}")
      return guess_fuel_split(ore, fuel // magnitude, fuel)

def guess_fuel_split(ore_limit, lower, upper):
  middle = lower + ((upper - lower) // 2)
  ore_cost = reduce_formula('FUEL', middle)
  if ore_cost > ore_limit:
    return guess_fuel_split(ore_limit, lower, middle)
  else:
    next_cost = reduce_formula('FUEL', middle + 1)
    if next_cost > ore_limit:
      return middle
    else:
      return guess_fuel_split(ore_limit, middle, upper)


print(guess_fuel(collected_ore))
