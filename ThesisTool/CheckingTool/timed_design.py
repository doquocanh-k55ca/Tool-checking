'''
Created on Apr 24, 2014

@author: geek
'''
from z3 import *

class timed_design(object):    
    def __init__(self, precondition, postcondition, time_constraint):
        self.precondition = precondition
        self.postcondition = postcondition
        self.time_constraint = time_constraint
        
def check_satisfiability(s):
    x = Int('x')
    y = Int('y')
    s = eval(s)
    solver = Solver()
    solver.add(s)
    if solver.check() == sat:
        return True
    return False

def get_and_constraint(constraint1, constraint2):
    return "And(" + constraint1 + "," + constraint2 + ")"

def get_imply_constraint(constraint1, constraint2):
    return "Implies(" + constraint1 + "," + constraint2 + ")"

def check_satisfiability_time(timed_design1, timed_design2):
    return (timed_design1.time_constraint[0] >= timed_design2.time_constraint[0] and
             timed_design1.time_constraint[1] <= timed_design2.time_constraint[1])

def check_refine_ls(timed_design1, timed_design2):
    
    if (check_satisfiability_time(timed_design1, timed_design2) == False):
        return False
    expr1 = get_imply_constraint(timed_design2.precondition, timed_design1.precondition)
    expr2 = get_and_constraint(timed_design2.precondition, timed_design1.postcondition)
    expr3 = get_imply_constraint(expr2, timed_design2.postcondition)
    constraint = get_and_constraint(expr1, expr3)
   
    if (check_satisfiability(constraint) is True):
        return True
    return False
