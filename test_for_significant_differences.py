#!/cygdrive/c/Python27/python.exe
import sys
from units import *

def parse_successes(lines,iterations):
  successes = dict()
  for line in lines:
    contestant, confidence = line.split()
    successes[contestant] = int(float(confidence) * iterations)
  return successes


if __name__ == '__main__':
  iterations = int(sys.argv[3])
  successes1 = parse_successes(get_lines_from_file(sys.argv[1]),iterations)
  successes2 = parse_successes(get_lines_from_file(sys.argv[2]),iterations)
  
  common_contestants = set(successes1.iterkeys()).intersection(set(successes2.iterkeys()))
  
  for contestant in common_contestants:
    if are_significantly_different(successes1[contestant],successes2[contestant],iterations,iterations):
      print contestant