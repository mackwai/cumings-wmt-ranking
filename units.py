import math
import sys
from collections import defaultdict
from collections import namedtuple
from PriorityQueueForSearch import PriorityQueueForSearch

def bitmap(sequence):
  """ Generate a coverage bitmap for a sequence of indexes """
#  return reduce(lambda x,y: x|y, [long('1'+'0'*i,2) for i in sequence], 0)
  bits = 0
  for i in sequence:
    bits |= 1 << i
  return bits

def bitmap2str(b, n, on='o', off='.'):
  """ Generate a length-n string representation of bitmap b """
  return '' if n==0 else (on if b&1==1 else off) + bitmap2str(b>>1, n-1, on, off)

def indexes(b, n=0):
  """ Generate a list of indexes that are turned on in a bitmap b """
  return [] if b==0 else ([n] if b&1==1 else []) + indexes(b>>1, n+1)

def count_set_bits(b):
  """ Count the number of bits set to 1 in the bitmap. """
  return 0 if b==0 else (1 if b&1==1 else 0) + count_set_bits(b>>1)

class ComparisonDatum:
  def __init__(self,wins=0,losses=0):
    self.wins = wins
    self.losses = losses
  def __eq__(self,other):
    return self.wins == other.wins and self.losses == other.losses
  def total(self):
    return self.wins + self.losses
    
def read_lines_from_stdin():
  lines = list()
  for line in sys.stdin:
    lines.append(line)
  return lines

def extract_contestants_from_tournament_file(lines):
  contestants = set()
  for line in lines:
    (count, sys1, sys2, order) = line.strip().split()
    contestants.add(sys1)
    contestants.add(sys2)
    
  return contestants

def extract_comparison_data_from_tournament_file(lines):
  comparison_data = defaultdict(ComparisonDatum)
  for line in lines:
    (count, sys1, sys2, order) = line.strip().split()
    if order == "<":
      comparison_data[(sys1,sys2)].losses = int(count)
    elif order == ">":
      comparison_data[(sys1,sys2)].wins = int(count)
  return comparison_data
      
def calculate_costs(contestants,comparison_data,cost_function):
  costs = dict()
  for u in contestants:
    costs[u] = dict()
    for v in contestants:
      if u == v:
        continue
      else:
        costs[u][v] = cost_function( comparison_data[(u,v)] )
  return costs
    
  return comparison_data

def calculate_MFAS_cost(datum):
  return 0 if datum.wins > datum.losses else datum.losses - datum.wins

def calculate_winning_percentage_cost(datum):
  if datum.total() == 0:
    return -math.log(0.5)
  elif datum.wins == 0:
    return 10.0
  
  percentage = float(datum.wins) / float(datum.total())
  #if percentage > 0.99:
  #  print 'hey'
  #  return -math.log1p(percentage - 1.0)
  #else:
  return -math.log( percentage )
  
def make_sorted_list_of_costs(contestants,costs):
  list_of_costs = list()
  for contestant1 in contestants:
    for contestant2 in contestants:
      if contestant1 == contestant2:
        continue
      list_of_costs.append(costs[contestant1][contestant2])
  return sorted(list_of_costs)

def triangular_number(n):
  return n*(n+1)/2 if n > 0 else 0

def calculate_heuristic_costs(contestants,sorted_list_of_costs):
  """Generate an array of heuristic costs for a search for a ranking.  Return an array where an index is the number
  of contestants in a partial ranking and the value is the heuristic cost to be added to
  the partial ranking's actual cost."""
  number_of_contestants = len(contestants)
  costs = [0.0]*(number_of_contestants+1)
  for i in range(0,number_of_contestants+1):
    costs[i] = heuristic_cost( number_of_contestants, i, sorted_list_of_costs )
    #costs[i] = math.fsum(sorted_list_of_costs[0:triangular_number(number_of_contestants-1)-triangular_number(i-1)]) #\
    # - math.fsum( sorted_list_of_costs[-triangular_number(number_of_contestants-1)-1:-1] )
    #if costs[i] < 0.0:
    #  costs[i] = 0.0
    #else:
    #  print 'one bigger than zero'
  return costs

def extract_ranking(h):
  return "" if h.predecessor is None else "%s%s\n" % (extract_ranking(h.predecessor), h.vertex)

def heuristic_cost(number_of_contestants,number_of_contestants_ranked,remaining_costs):
  cost = math.fsum(remaining_costs[0:triangular_number(number_of_contestants-1)-triangular_number(number_of_contestants_ranked-1)])
  #print cost
  return cost

def search_for_ranking_without_fancy_priority_queue(contestants,costs,heuristic_costs):
  contestants = list(contestants)
  number_of_contestants = len(contestants)
  hypothesis = namedtuple("hypothesis", "actual_cost, cost, state, predecessor, vertex")#remaining_costs, vertex")
  initial_hypothesis = hypothesis(
    actual_cost=0.0,
    cost=heuristic_costs[0],
    state=0,
    predecessor=None,
    vertex=None)
  
  agenda = {}
  agenda[0] = initial_hypothesis
  goal = bitmap(xrange(len(contestants)))

  nodes_explored = 0

  while len(agenda) > 0:
    h = sorted(agenda.itervalues(), key=lambda h: h.cost)[0]

    if h.state == goal:
      return h, nodes_explored
    del agenda[h.state]

    nodes_explored += 1
  
    for u in indexes(goal^h.state):
      new_state = h.state | bitmap([u])
      added_cost = 0.0
      number_of_contestants_ranked = count_set_bits(new_state)
      added_cost = math.fsum( map( lambda w: costs[contestants[u]][contestants[w]], indexes(goal^new_state) ) )
      new_h = hypothesis(
        actual_cost=h.actual_cost + added_cost,
        cost=h.actual_cost + added_cost + heuristic_costs[number_of_contestants_ranked],
        state=new_state,
        predecessor=h,
        vertex=contestants[u] )
      if new_state not in agenda or agenda[new_state].actual_cost > new_h.actual_cost:
        agenda[new_state] = new_h

def search_for_ranking_consistent_heuristic(contestants,costs,heuristic_costs):
  contestants = list(contestants)
  number_of_contestants = len(contestants)
  sorted_costs = make_sorted_list_of_costs(contestants, costs)
  hypothesis = namedtuple("hypothesis", "actual_cost, cost, state, predecessor, remaining_costs, vertex")
  initial_hypothesis = hypothesis(
    actual_cost=0.0,
    cost=heuristic_cost(number_of_contestants,0,sorted_costs),
    state=0,
    predecessor=None,
    remaining_costs=sorted_costs,
    vertex=None)
  
  agenda = PriorityQueueForSearch( lambda x,y: x.cost > y.cost )
  agenda.EnqueueIfBetter(initial_hypothesis)
  goal = bitmap(xrange(number_of_contestants))

  visited_states = dict()
  nodes_explored = 0

  while not agenda.IsEmpty():
    h = agenda.Dequeue()
    
    if h.state == goal:
      return h, nodes_explored

    nodes_explored += 1
    
    if not h.state in visited_states or visited_states[ h.state ].actual_cost > h.actual_cost:
      visited_states[ h.state ] = h

    for u in indexes(goal^h.state):
      new_state = h.state | bitmap([u])
      added_cost = 0.0
      number_of_contestants_ranked = count_set_bits(new_state)
      remaining_costs = list(h.remaining_costs)
      for v in indexes(goal^new_state):
        cost = costs[contestants[u]][contestants[v]]
        added_cost += cost
        remaining_costs.remove(cost)
        remaining_costs.remove(costs[contestants[v]][contestants[u]])
      new_h = hypothesis(
        actual_cost=h.actual_cost + added_cost,
        cost=h.actual_cost + added_cost + heuristic_cost(
          number_of_contestants,
          number_of_contestants_ranked,
          remaining_costs ),
        state=new_state,
        predecessor=h,
        remaining_costs=remaining_costs,
        vertex=contestants[u] )
      
      if not new_h.state in visited_states or visited_states[ new_h.state ].actual_cost > new_h.actual_cost:
        agenda.EnqueueIfBetter(new_h)
        
def search_for_ranking(contestants,costs,heuristic_costs):
  contestants = list(contestants)
  number_of_contestants = len(contestants)
  hypothesis = namedtuple("hypothesis", "actual_cost, cost, state, predecessor, vertex")
  initial_hypothesis = hypothesis(
    actual_cost=0.0,
    cost=heuristic_costs[0],
    state=0,
    predecessor=None,
    vertex=None)
  
  agenda = PriorityQueueForSearch( lambda x,y: x.cost > y.cost )
  agenda.EnqueueIfBetter(initial_hypothesis)
  
  goal = bitmap(xrange(len(contestants)))

  nodes_explored = 0

  while not agenda.IsEmpty():
    h = agenda.Dequeue()
    
    if h.state == goal:
      return h, nodes_explored

    nodes_explored += 1

    for u in indexes(goal^h.state):
      new_state = h.state | bitmap([u])
      added_cost = 0.0
      number_of_contestants_ranked = count_set_bits(new_state)
      added_cost = math.fsum( map( lambda w: costs[contestants[u]][contestants[w]], indexes(goal^new_state) ) )
      new_h = hypothesis(
        actual_cost=h.actual_cost + added_cost,
        cost=h.actual_cost + added_cost + heuristic_costs[number_of_contestants_ranked],
        state=new_state,
        predecessor=h,
        vertex=contestants[u] )
      
      agenda.EnqueueIfBetter(new_h)