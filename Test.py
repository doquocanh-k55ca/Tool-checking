'''
Created on Apr 24, 2014

@author: geek
'''


from automata import *
from TimedDesign import *

# timed designs and guard formulas for interface

timed_design1 = timed_design("x > 5","y >= x", (4,7))
timed_design2 = timed_design("x>10", "y > 5", (4,5))
timed_design3 = timed_design("x >= 12", "y > x", (1,6))
guard_formula1 = "Not(x==y)"
guard_formula2 = "x>y"
guard_formula3 = "x+y > 5"

        
interface = automata(locations = set(["q1","q2","q3"]),
                     inputs = set(["x"]),
                     outputs = set(["y"]),
                     initial_state = "q1",
                     transitions = set([("q1","q2"),("q2","q3"),("q3","q1")]),
                     ls = {"q1" : timed_design1, "q2" : timed_design2, "q3" : timed_design3},
                     lt = {("q1","q2") : guard_formula1,("q2","q3") : guard_formula2,("q3","q1") : guard_formula3 }
                     )

# timed designs and guard formulas for environment

timed_design4 = timed_design("x < 4","y >= x", (3,7))
timed_design5 = timed_design("x>10", "y > 5", (2,5))
timed_design6 = timed_design("x >= 12", "y > x", (4,6))
guard_formula4 = "Not(x==y)"
guard_formula5 = "x>y"
guard_formula6 = "x+y > 5"


environment = automata(locations = set(["h1","h2","h3"]),
                     inputs = set(["x"]),
                     outputs = set(["y"]),
                     initial_state = "h1",
                     transitions = set([("h1","h2"),("h2","h3"),("h3","h1")]),
                     ls = {"h1" : timed_design4,"h2" : timed_design5,"h3" : timed_design6},
                     lt = {("h1","h2") : guard_formula4,("h2","h3") : guard_formula5,("h3","h1") : guard_formula6}
                     )

check_plugability(interface,environment)

