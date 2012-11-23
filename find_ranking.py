#!/usr/bin/python
import sys
from datetime import datetime
from units import *

cost_functions = dict(
  MFAS=calculate_MFAS_cost,
  win_percentage=calculate_winning_percentage_cost
)

# This script takes one, optional, command-line argument: the name of the cost function to use.
# It uses "win_percentage" by default.  This script processes comparison data in the same format as the
# files in wmt-ranking/data/tournaments; it reads the data from stdin, just like mfas_solver.py.

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
heuristic_costs = calculate_heuristic_costs(contestants,sorted_list_of_costs)

# Uncomment this line to remove the heuristic; this should generate the same results as the original mfas_solver.py.
#heuristic_costs = map( lambda x: 0.0, heuristic_costs )

path, nodes_explored = search_for_ranking(contestants,costs,heuristic_costs)

# These are alternative versions of the search.
#
# search_for_ranking_without_fancy_priority_queue is the same as search_for_ranking, except it doesn't use
# PriorityQueueForSearch.  It's there to ensure that PriorityQueueForSearch isn't affecting the search results.
#
# search_for_ranking_consistent_heuristic uses the heuristic that eliminates costs from the sorted list of
# costs as they are added to a search path.  It does not return correct results.
#
#path, nodes_explored = search_for_ranking_without_fancy_priority_queue(contestants,costs,heuristic_costs)
#path, nodes_explored = search_for_ranking_consistent_heuristic(contestants,costs)

print extract_ranking(path)
print datetime.now() - start_time
print "nodes explored: %d" % nodes_explored
print 'actual cost: %f' % path.actual_cost
print 'heuristic cost: %f' % path.cost
