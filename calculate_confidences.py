#!/cygdrive/c/Python27/python.exe
import os
from units import *


if __name__ == '__main__':
  for file_name in os.listdir( '../data/tournaments' ):
    #print path
    path = os.path.join( '../data/tournaments', file_name )
    prior = calculate_prior_probability_of_true_judgement(get_lines_from_file(path))
    print prior
    calculate_testimonial_cost = close_testimonial_cost(0.51)
    print "%s %f" % ( file_name, estimate_confidence(path,calculate_testimonial_cost,10) )