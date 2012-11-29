#!/cygdrive/c/Python27/python.exe
import argparse
import random
import distributions

from units import *

def get_command_line_arguments():
  parser = argparse.ArgumentParser()
  
  parser.add_argument(
    '--mean_winning_percentage',
    type=float,
    default=0.711097,
    help='the mean percent of comparisons won in a pairwise comparison by the winning contestant')
  
  parser.add_argument(
    '--mean_contests',
    type=float,
    default=25.658462,
    help='the mean of the number of contests between two contestants')
  
  parser.add_argument(
    '--stdev_contests',
    type=float,
    default=5.886906,
    help='the standard deviation in the number of contests between two contestants')
  
  parser.add_argument(
    '--contestants',
    type=str,
    default='1,2,3,4,5,6,7,8,9',
    help='a list of names of contestants, delimited by commas, or a number of contestants')
  
  return parser.parse_args()

if __name__ == '__main__':
  for line in generate_tournament_text(get_command_line_arguments()):
    print line
  
      
  
  