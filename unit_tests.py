#!/usr/bin/python
import os
import sys

from units import *

def compare_results(expected_results,actual_results):
  success = True
  for i in xrange(max(len(expected_results),len(actual_results))):
    try:
      if expected_results[i] != actual_results[i]:
        success = False
        print 'Case %d failed.' % i
        print 'Expected result:'
        print expected_results[i]
        print 'Actual result:'
        print actual_results[i]
    except IndexError:
      print "Expected Results: %d" % len(expected_results)
      print "Actual Results: %d" % len(actual_results)
      raise
  return success

def print_result(unit_name,result):
  print '%s %s' % (unit_name,'passed' if result else 'failed')

def test_bitmap():
  return compare_results(
    [0,1,2,4,9],
    map( bitmap, [[],[0],[1],[2],[3,0]] ) )
  
def test_bitmap2str():
  return compare_results(
    ['.....','o....','.o...','..o..','o..o.'],
    map( lambda b: bitmap2str(b,5), [0,1,2,4,9] ) )
  
def test_indexes():
  return compare_results(
    [[],[0],[1],[2],[0,3]],
    map( indexes, [0,1,2,4,9] ) )
  
def test_count_set_bits():
  return compare_results(
    [0,1,1,1,2,3],
    map( count_set_bits, [0,1,2,4,9,14] ) )
  
def test_read_lines_from_stdin():
  strings = ['ring\n','ring\n','ring\n','hello\n']
  sys.stdin = open('test_file.txt','w')
  sys.stdin.writelines(strings)
  sys.stdin.close()
  sys.stdin = open('test_file.txt','r')
  return compare_results( strings, read_lines_from_stdin() )

def test_extract_contestants_from_tournament_file():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
     33 _ref upv-prhlt-combo <
    225 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
    225 upv-prhlt-combo _ref <
     33 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines(
  )
  return compare_results( ['_ref','cmu-heafield-combo','upv-prhlt-combo'], sorted(extract_contestants_from_tournament_file(lines)) )

def test_extract_comparison_data_from_tournament_file():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
     33 _ref upv-prhlt-combo <
    225 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
    225 upv-prhlt-combo _ref <
     33 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines(
  )
  return compare_results(
    [ (('_ref','cmu-heafield-combo'), ComparisonDatum(wins=219,losses=32)),
      (('_ref','upv-prhlt-combo'), ComparisonDatum(wins=225,losses=33)),
      (('cmu-heafield-combo','_ref'), ComparisonDatum(wins=32,losses=219)),
      (('cmu-heafield-combo','upv-prhlt-combo'), ComparisonDatum(wins=111,losses=66)),
      (('upv-prhlt-combo','_ref'), ComparisonDatum(wins=33,losses=225)),
      (('upv-prhlt-combo','cmu-heafield-combo'), ComparisonDatum(wins=66,losses=111)) ],
    sorted(extract_comparison_data_from_tournament_file(lines).iteritems()) )
  
def test_calculate_MFAS_cost():
  return compare_results(
    [34,0,1,0,0],
    map( calculate_MFAS_cost, [
      ComparisonDatum(wins=33,losses=67),
      ComparisonDatum(wins=88,losses=22),
      ComparisonDatum(wins=0,losses=1),
      ComparisonDatum(wins=1,losses=0),
      ComparisonDatum(wins=100,losses=100) ] ) )
  
def test_calculate_winning_percentage_cost():
  return compare_results(
    [1.1086626245216111, 0.2231435513142097, 10.0, -0.0, 0.6931471805599453],
    map( calculate_winning_percentage_cost, [
      ComparisonDatum(wins=33,losses=67),
      ComparisonDatum(wins=88,losses=22),
      ComparisonDatum(wins=0,losses=1),
      ComparisonDatum(wins=1,losses=0),
      ComparisonDatum(wins=100,losses=100) ] ) )
  
def test_calculate_costs():
  comparison_data = defaultdict(ComparisonDatum)
  comparison_data[(1,2)] = ComparisonDatum(wins=10,losses=4)
  comparison_data[(2,1)] = ComparisonDatum(wins=4,losses=10)
  comparison_data[(2,3)] = ComparisonDatum(wins=3,losses=11)
  comparison_data[(3,2)] = ComparisonDatum(wins=11,losses=3)
  costs = calculate_costs(set([1,2,3]),comparison_data,lambda datum: 2*datum.wins-datum.losses)
  return compare_results(
    [16,0,-2,-5,0,19],
    [
      costs[1][2],
      costs[1][3],
      costs[2][1],
      costs[2][3],
      costs[3][1],
      costs[3][2] ] )

def test_make_sorted_list_of_costs():
  comparison_data = defaultdict(ComparisonDatum)
  comparison_data[(1,2)] = ComparisonDatum(wins=10,losses=4)
  comparison_data[(2,1)] = ComparisonDatum(wins=4,losses=10)
  comparison_data[(2,3)] = ComparisonDatum(wins=3,losses=11)
  comparison_data[(3,2)] = ComparisonDatum(wins=11,losses=3)
  costs = calculate_costs(set([1,2,3]),comparison_data,lambda datum: 2*datum.wins-datum.losses)
  return compare_results( [-5, -2, 0, 0, 16, 19], make_sorted_list_of_costs( set([1,2,3]), costs ) )
  
def test_triangular_number():
  return compare_results(
    [0,0,1,3,6,10,15,21],
    map( triangular_number, [-1,-0,1,2,3,4,5,6] ) )
  
def test_calculate_heuristic_costs():
  contestants = set([1,2,3,4])
  sorted_list_of_costs = [1,2,3,4,5,6]
  return compare_results(
    [21,6,1,0,0],
    calculate_heuristic_costs( contestants, sorted_list_of_costs ) )
  
def test_search_for_ranking():
  '''intended ranking: 1,3,2'''
  contestants = set([1,2,3])
  costs = {
    1:{2:0,3:2},
    2:{1:4,3:1},
    3:{1:6,2:0} }
  h, nodes_searched = search_for_ranking(contestants,costs)
  
  return compare_results(
    ["1","3","2"],
    extract_ranking(h).strip().split("\n") )
  
def test_simple_astar_heuristic():
  path_to_tournaments = '../data/tournaments'
  heuristic_costs = [0.0]*32
  for file_name in os.listdir( path_to_tournaments ):
    path = os.path.join(path_to_tournaments,file_name)
    if os.path.getsize(path) > 15000:
      continue
    if file_name == 'wmt11.English,Spanish.individual':
      #Ignore this one because there is a tie in the ranking.
      continue
    lines = get_lines_from_file(path)
    contestants = extract_contestants_from_tournament_file(lines)
    comparison_data = extract_comparison_data_from_tournament_file(lines)
    costs = calculate_costs(contestants,comparison_data,calculate_winning_percentage_cost)
    sorted_list_of_costs = make_sorted_list_of_costs(contestants,costs)
    h, nodes_explored = search_for_ranking_constant_heuristic_costs(contestants,costs,heuristic_costs)

    expected_ranking = extract_ranking(h)
    
    h, nodes_explored = search_for_ranking_constant_heuristic_costs(contestants,costs,calculate_heuristic_costs(contestants,sorted_list_of_costs))
    actual_ranking = extract_ranking(h)
    
    if ( expected_ranking != actual_ranking ):
      print 'Bad ranking for %s' % file_name
      print expected_ranking
      print actual_ranking
      return False
  
  return True
  
def test_astar_heuristic():
  path_to_tournaments = '../data/tournaments'
  heuristic_costs = [0.0]*32
  for file_name in os.listdir( path_to_tournaments ):
    path = os.path.join(path_to_tournaments,file_name)
    if os.path.getsize(path) > 15000:
      continue
    if file_name == 'wmt11.English,Spanish.individual':
      #Ignore this one because there is a tie in the ranking.
      continue
    lines = get_lines_from_file(path)
    contestants = extract_contestants_from_tournament_file(lines)
    comparison_data = extract_comparison_data_from_tournament_file(lines)
    costs = calculate_costs(contestants,comparison_data,calculate_winning_percentage_cost)
    sorted_list_of_costs = make_sorted_list_of_costs(contestants,costs)
    h, nodes_explored = search_for_ranking_constant_heuristic_costs(contestants,costs,heuristic_costs)

    expected_ranking = extract_ranking(h)
    
    if ( expected_ranking != find_ranking(lines,calculate_winning_percentage_cost) ):
      print 'Bad ranking for %s' % file_name
      print expected_ranking
      print find_ranking(lines,calculate_winning_percentage_cost)
      return False
  
  return True

def test_generate_random_wins():
  return compare_results(
    [0,1,100],
    [generate_random_wins(100,0.0),generate_random_wins(1,1.0),generate_random_wins(100,1.0)] )
  
def test_generate_lines_of_tournament_text():
  wins_and_losses = {
    'winner' : { 'middle': (100,10) },
    'winner' : { 'loser': (100,0) },
    'middle' : { 'loser': (11,1) } }
  
  return "\n".join(generate_lines_of_tournament_text(wins_and_losses)) == """     11 loser middle <
      1 loser middle >
    100 loser winner <
      0 loser winner >
      1 middle loser <
     11 middle loser >
      0 winner loser <
    100 winner loser >"""
    
def test_count_comparisons():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
     33 _ref upv-prhlt-combo <
    225 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
    225 upv-prhlt-combo _ref <
     33 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines(
  )
  return count_comparisons(lines) == 686

def test_find_fewest_false_judgements_possible():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
    225 _ref upv-prhlt-combo <
     33 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
     33 upv-prhlt-combo _ref <
    225 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines()
  return find_fewest_false_judgements_possible(lines) == 111

def test_bojar_statistic():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
     33 _ref upv-prhlt-combo <
    225 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
    225 upv-prhlt-combo _ref <
     33 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines()
  contestants = extract_contestants_from_tournament_file(lines)
  comparison_data = extract_comparison_data_from_tournament_file(lines)
  comparisons = count_comparisons(lines)
  
  return compare_results(
    map( lambda x: float(x)/686.0, [444,143,99] ),
    map(
      lambda contestant: bojar_statistic(contestant, contestants, comparison_data, comparisons),
      sorted(contestants) ) )
  
def test_bojar_ranking():
  lines = '''     32 _ref cmu-heafield-combo <
    219 _ref cmu-heafield-combo >
     33 _ref upv-prhlt-combo <
    225 _ref upv-prhlt-combo >
    219 cmu-heafield-combo _ref <
     32 cmu-heafield-combo _ref >
     66 cmu-heafield-combo upv-prhlt-combo <
    111 cmu-heafield-combo upv-prhlt-combo >
    225 upv-prhlt-combo _ref <
     33 upv-prhlt-combo _ref >
    111 upv-prhlt-combo cmu-heafield-combo <
     66 upv-prhlt-combo cmu-heafield-combo >
'''.splitlines()
  
  return bojar_ranking(lines) == '''_ref
cmu-heafield-combo
upv-prhlt-combo
'''

def test_are_significantly_different():
  return compare_results(
    [False,True,False,True,False,True,False],
    map( lambda tuple: are_significantly_different( tuple[0], tuple[1], tuple[2], tuple[2] ),
      [
        (999,1000,1000),
        (500,750,1000),
        (970,980,1000),
        (703,743,1000),
        (703,742,1000),
        (0,100,100),
        (100,100,100),
      ] ) )
  

if __name__ == '__main__':
  print 'Running unit tests...'
  print_result('bitmap',test_bitmap())
  print_result('bitmap2str',test_bitmap2str())
  print_result('indexes',test_indexes())
  print_result('count_set_bits',test_count_set_bits())
  print_result('read_lines_from_stdin',test_read_lines_from_stdin())
  print_result('extract_contestants_from_tournament_file',test_extract_contestants_from_tournament_file())
  print_result('extract_comparison_data_from_tournament_file',test_extract_comparison_data_from_tournament_file())
  print_result('calculate_MFAS_cost',test_calculate_MFAS_cost())
  print_result('calculate_winning_percentage_cost',test_calculate_winning_percentage_cost())
  print_result('make_sorted_list_of_costs',test_make_sorted_list_of_costs())
  print_result('triangular_number',test_triangular_number())
  print_result('calculate_heuristic_costs',test_calculate_heuristic_costs())
  print_result('search_for_ranking',test_search_for_ranking())
  #print_result('A* heuristic',test_astar_heuristic())
  #print_result('simple A* heuristic',test_simple_astar_heuristic())
  print_result('generate_random_wins',test_generate_random_wins())
  print_result('generate_lines_of_tournament_text',test_generate_lines_of_tournament_text())
  print_result('count_comparisons',test_count_comparisons())
  print_result('find_fewest_false_judgements_possible',test_find_fewest_false_judgements_possible())
  print_result('bojar_statistic',test_bojar_statistic())
  print_result('bojar_ranking',test_bojar_ranking())
  print_result('are_significantly_different',test_are_significantly_different())
  
  