'''
Created on Apr 24, 2014

@author: geek
'''
from z3 import *

class timed_design(object):
    def __init__(self,precondition,postcondition,time_interval):
        self.precondition = precondition
        self.postcondition = postcondition
        self.time_interval = time_interval
        
def check_sat(s):
    x = Int('x')
    y = Int('y')
    s = eval(s)
    solver = Solver()
    solver.add(s)
    str_convert = str(solver.check())
    if str_convert is "sat":
        return True
    return False

def check_refine_ls(timed_design1,timed_design2):
    exp1 = "Implies(" + timed_design2.precondition + "," + timed_design1.precondition +")"
    exp2 = "And(" + timed_design2.precondition + "," + timed_design1.postcondition + ")"
    exp3 = "Implies(" + exp2 + "," + timed_design2.postcondition + ")"
    exp = "And(" + exp1 + "," + exp3 + ")"
   
    if (check_sat(exp) is True):
        if (timed_design1.time_interval[0] >= timed_design2.time_interval[0] and timed_design1.time_interval[1] <= timed_design2.time_interval[1]):
            return True
        else:
            return False
    else:
        return False
