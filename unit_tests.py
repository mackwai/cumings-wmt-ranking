#!/usr/bin/python
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
    [21,21,15,6,0],
    calculate_heuristic_costs( contestants, sorted_list_of_costs ) )
  
def test_search_for_ranking():
  '''intended ranking: 1,3,2'''
  contestants = set([1,2,3])
  costs = {
    1:{2:0,3:2},
    2:{1:4,3:1},
    3:{1:6,2:0} }
  heuristic_costs = make_sorted_list_of_costs(contestants,costs)
  h, nodes_searched = search_for_ranking(contestants,costs,heuristic_costs)
  
  return compare_results(
    ["1","3","2"],
    extract_ranking(h).strip().split("\n") )
  

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
  