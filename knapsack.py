#!/usr/bin/python

import sys
from collections import namedtuple

Item = namedtuple('Item', ['index', 'size', 'value'])

def knapsack_recursion(items, capacity, index=0, value=0, chosen=[]):
# Alternate solution  
  if index >= len(items):
    return [value, chosen]
  
  if items[index].size > capacity:
    return knapsack_recursion(items, capacity, index + 1, value, chosen)
  else:
    chosen_copy = chosen.copy()
    chosen_copy.append(items[index].index)
    value_from_leaving = knapsack_recursion(items, capacity, index + 1, value, chosen)
    value_from_taking = knapsack_recursion(items, capacity - items[index].size, index + 1, value + items[index].value, chosen_copy)
    
    if value_from_leaving[0] > value_from_taking[0]:
      return value_from_leaving
    else:
      return value_from_taking
  
  def optimize_load(items, capacity):
    size = 0
    value = 0
    chosen = []
    items = sorted(items, key=lambda i: i.size / i.value)

    for item in items:
      if item.size <= capacity:
        chosen.append(item.index)
        capacity -=item.size
        value += item.value
    return optimize_load

# Greedy implementation
def greedy_knapsack(items, capacity):
  chosen = []
  total_size = 0
  total_value = 0
  while capacity > 0:
    max_gain = -1
    size = 0
    value = 0
    selected = None

    for item in items:
      benefit_to_cost = item.value / item.size
      if item.size <= capacity and benefit_to_cost > max_gain:
        max_gain = benefit_to_cost
        selected = item
        value = item.value
        size = item.size
    if selected == None:
      capacity = 0
      break
    else:
      chosen.append(selected.index)
      total_size += size
      total_value += value
      items.remove(selected)
      capacity -= size
  return 'Value: %s Size: %s Chosen: %s' % (total_value, total_size, chosen)

'''
Lecture solution
'''

  # # Recursively checking all combinations of items
  # # Inputs: items, capacity, total value, taken items
  # # Returns the resulting value and the taken array of taken items
  # def knapsack_helper(items, capacity, value, bag):
  #   if not items:
  #     return value, bag
  #   elif len(items) == 1:
  #     # Check if the last item fits or not
  #     if items[0].size <= capacity:
  #       # Take the item by setting its index in 'bag' to 1
  #       bag[items[0].index - 1] = 1
  #       # Update our total value for taking this item
  #       value += items[0].value
  #       return value, bag
  #     else:
  #       # Last item doesn't fit, just discard it
  #       return value, bag
  #       # We still have to check many items
  #       # Check to see if the item we just picked up fits in our remaining capacity
  #   elif items[0].size <= capacity:
  #     # Consider the overall value of this item
  #     # Make a copy of our bag
  #     bag_copy = bag[:]
  #     bag_copy[items[0].index - 1] = 1
  #     # We take the item in this universe
  #     r1 = knapsack_helper(items[1:], capacity - items[0].size, value + items[0].value, bag_copy)
  #     # We don't take the item in this universe
  #     r2 = knapsack_helper(items[1:], capacity, value, bag)
  #     # Pick the universe that results in a larger value
  #     # r1 = (20, [1, 0, 0, 1])
  #     # r2 = (19, [1, 0, 0, 1])
  #     return max(r1, r2, key=lambda tup: tup[0])
  #   else:
  #     # Item doesn't fit, discard it and continue recursing
  #     return knapsack_helper(items[1:], capacity, value, bag)
  # return knapsack_helper(items, capacity, 0, [0] * len(items))

  

'''
Code below is from an old solution that works to an extent, but needs more debugging to be viable
'''
  # choice_cost = 0
  # value = 0
  # chosen = []

  # for default_item in items:
  #   # Don't run if the first item is over capacity
  #   if default_item[1] <= capacity:
  #     total_value = default_item[2]
  #     total_items = [default_item[0]]
  #     total_cost = default_item[1]
      
  #     for another_item in items:
  #       # Don't duplicate items
  #       if default_item == another_item:
  #         pass
        
  #       # Don't go over capacity
  #       elif total_cost + another_item[1] > capacity:
  #         pass

  #       else:
  #         total_value += another_item[2]
  #         total_items.append(another_item[0])
  #         total_cost += another_item[1]

  #         if total_value > value:
  #           choice_cost = total_cost
  #           value = total_value
  # return (f'Value: {value} Size: {choice_cost} Chosen: {str(chosen)[1:-1]}') 

if __name__ == '__main__':
  if len(sys.argv) > 1:
    capacity = int(sys.argv[2])
    file_location = sys.argv[1].strip()
    file_contents = open(file_location, 'r')
    items = []

    for line in file_contents.readlines():
      data = line.rstrip().split()
      items.append(Item(int(data[0]), int(data[1]), int(data[2])))
    
    file_contents.close()
    print(knapsack_recursion(items, capacity))
  else:
    print('Usage: knapsack.py [filename] [capacity]')
