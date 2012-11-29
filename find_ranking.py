#!/usr/bin/python
import sys
from datetime import datetime
from units import *

cost_functions = dict(
  MFAS=calculate_MFAS_cost,
  win_percentage=calculate_winning_percentage_cost
)

if len(sys.argv) > 1 and sys.argv[1] in cost_functions:
  cost_function = cost_functions[sys.argv[1]]
else:
  cost_function = calculate_winning_percentage_cost
  

start_time = datetime.now()

lines = read_lines_from_stdin()
contestants = extract_contestants_from_tournament_file(lines)
comparison_data = extract_comparison_data_from_tournament_file(lines)
costs = calculate_costs(contestants,comparison_data,cost_function)
sorted_list_of_costs = make_sorted_list_of_costs(contestants,costs)

path, nodes_explored = search_for_ranking(contestants,costs)

print extract_ranking(path,path.actual_cost)
print datetime.now() - start_time
print "nodes explored: %d" % nodes_explored
print 'actual cost: %f' % path.actual_cost
print 'heuristic cost: %f' % path.cost
