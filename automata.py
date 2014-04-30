''' This function checks two given interface and environment,
     which is represented by labeled automata, by using algorithm checking plugability 
Created on Apr 21, 2014

@author: geek
'''

from TimedDesign import *

class automata(object):
    def __init__(self,locations,inputs, outputs, initial_state, transitions,ls, lt):
        self.locations = locations
        self.inputs= inputs
        self.outputs = outputs
        self.initial_state = initial_state
        self.transitions = transitions
        self.ls = ls
        self.lt = lt

def contains(small, big):
    for value in big:
        if small == value:
            return True
    return False
            
def has_unmarked_index(location_pairs):
    for key in location_pairs.keys():          # Check if exist an unmarked pair
        if (location_pairs[key] is "unmarked"):
            return key
    return False

def is_transition(location1,location2,transitions):
    if (location1 != location2 and contains((location1,location2),transitions)):
        return True
    return False

def get_timed_design(location, automata):
    return automata.ls[location]

def get_guard_formula(transition,automata):
    return automata.lt[transition]

# F(p,r2) = p /\ R /\ l't(p,r2)

def get_f_constraint(e_location1,e_location2,i_location,interface,environment):
    timed_design_i = get_timed_design(i_location,interface)
    timed_design_e = get_timed_design(e_location1,environment)
    if (is_transition(e_location1,e_location2,list(environment.transitions)) == True):
        lt = get_guard_formula((e_location1,e_location2),environment)
        condition1 = timed_design_e.precondition
        condition2 = timed_design_i.postcondition
        constraint = "And(" + condition1 + "," + condition2 + "," + lt + ")"
        return constraint

# lt(q,r1) /\ F(p,r2)

def get_lt(i_location1, i_location2,interface):
    if (is_transition(i_location1,i_location2,list(interface.transitions)) == True):
        lt = interface.lt[i_location1,i_location2]
        return lt

def existed_pair(location1,location2,location_pairs):
    for key in location_pairs.keys():
        if ((location1,location2) == key):
            return True
    return False

def check_plugability (interface,environment):
    index = ()
    f = [(interface.initial_state, environment.initial_state)]
    location_pairs = {(interface.initial_state,environment.initial_state):"unmarked"}
    while True:
        index = has_unmarked_index(location_pairs)
        if (index == False):                          # no unmarked found
            print "Yes"                
            return
        # Get tuple of locations (q,p)
        
        q = index[0]
        p = index[1]
        location_pairs[index] = "marked"
      
        # Get timed design corresponding to q and p state
        
        timed_design_i = interface.ls[q]
        timed_design_e = environment.ls[p]
      
        # Check if ls(q) is refinement of ls(q')
    
        if check_refine_ls(timed_design_i,timed_design_e) is False:
            print "No"
            return
        else:
            # iterate locations in environment
            for e_location in environment.locations:
                if(is_transition(p,e_location,environment.transitions)):
                    f = get_f_constraint(p,e_location,q,interface,environment)
                    if(check_sat(f) == True):
                        for i_location in interface.locations:
                            if(is_transition(q,i_location,interface.transitions)):
                                lt = get_lt(q,i_location,interface)
                                constraint = get_and_constraint(lt,f)
                                if (check_sat(constraint) is True):
                                    constraint = get_imply_constraint(f,lt)
                                    if (check_sat(constraint) is False):
                                        print "No"
                                        return
                                    elif (existed_pair(i_location,e_location,location_pairs) == False):
                                        location_pairs.update({(i_location,e_location):"unmarked"})
                                        
                                                                               
    
    

    






