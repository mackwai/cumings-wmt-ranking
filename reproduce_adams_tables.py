from units import *

# This script reproduces the MFAS and Bojar rankings in tables
# 2, 3 and 4 of Adam's paper.  It takes files from
# the tournaments folder as input.  The functions that
# parse the data from the files' text are
# units.extract_contestants_from_tournament_file and
# units.extract_comparison_data_from_tournament_file
# If you want to get this code to work for inputs of a
# different format, you'll need to change those functions.
# extract_contestants_from_tournament_file returns a set
# contestants' names.  extract_comparison_data_from_tournament_file
# returns a defaultdict of ComparionDatum objects that are keyed
# on pairs of contestants' names.  The first item in the pair
# is the name of the winner of the 'wins' in the ComparisonDatum and the
# second item in the pair is the name of the loser of the 'losses' in
# the ComparisonDatum object.

print '\nTable 2\n'
print 'MFAS'
czech_english_task_2011 = filter(
  lambda line: not '_ref' in line,
  get_lines_from_file('../data/tournaments/wmt11.English,Czech.individual') )
print find_ranking(czech_english_task_2011,calculate_MFAS_cost)
print 'Bojar'
print bojar_ranking(czech_english_task_2011)

print '\nTable 3\n'
print 'MFAS ("optimal ranking")'
french_english_task_2010 = filter(
  lambda line: not '_ref' in line,
  get_lines_from_file('../data/tournaments/wmt10.French,English') )
print find_ranking(french_english_task_2010,calculate_MFAS_cost)

print '\nTable 4\n'
print 'MFAS Ranking'
tunable_metrics_2011 = filter(
  lambda line: not '_ref' in line,
  get_lines_from_file('../data/tournaments/wmt11.Urdu,English.tunablemetrics') )
print find_ranking(tunable_metrics_2011,calculate_MFAS_cost)