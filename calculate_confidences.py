#!/cygdrive/c/Python27/python.exe
import fractions
import os

from units import *


if __name__ == '__main__':
  for file_name in os.listdir( '../data/tournaments' ):
    #print path
    path = os.path.join( '../data/tournaments', file_name )
    #prior = calculate_prior_probability_of_true_judgement(get_lines_from_file(path))
    #print prior
    
    if os.path.getsize(path) > 5000:
      continue
    
    calculate_testimonial_cost = close_testimonial_cost(fractions.Fraction(11,20))
    print "%s %f" % ( file_name, estimate_confidence_for_probability_function(path,calculate_testimonial_cost,100) )
    
    #print "%s %f" % ( file_name, estimate_confidence_for_bojar(path,1000) )