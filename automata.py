'''
Created on Apr 21, 2014

@author: geek
'''

from TimedDesign import *


# Check if a list is subset of another



def contains(small, big):
    for i in xrange(1 + len(big) - len(small)):
        if small == big[i:i+len(small)]:
            return True
    return False
            
            
        
        


class automata(object):
    def __init__(self,locations,inputs, outputs, initial_state, transitions,ls, lt):
        self.locations = locations
        self.inputs= inputs
        self.outputs = outputs
        self.initial_state = initial_state
        self.transtisions = transitions
        self.ls = ls
        self.lt = lt

''' This function checks two given interface and environment,
     which is represented by labeled automata, by using algorithm checking plugability '''

def check_plugability (interface,environment):
    
    # convert interface sets into lists
                
    interface_locations = list(interface.locations)
    interface_transitions = list(interface.transtisions)
    
    # convert environment sets into list
    
    environment_locations = list(environment.locations)
    environment_transitions = list(environment.transtisions)
    check = True
    t = ()
    f = [(interface.initial_state, environment.initial_state)]
    d = {f[0]:"unmarked"}
    while check is True:
        for key in d.keys():          # Check if exist an unmarked pair
            if (d[key] is "unmarked"):
                check = True
                t = key
                break
            else:
                check = False
        if (check is False):                # No unmarked pair found
            print "Yes"
            return
        
        # Get tuple (p,q)
        q = t[0]
        p = t[1]
        d[t] = "marked"
        # Get timed design from state q
        timed_design_i = interface.ls[q]
        timed_design_e = environment.ls[p]
    
        
        # Check if ls(q) is refinement of ls(q')
        
        if check_refine_ls(timed_design_i,timed_design_e) is False:
            print "No"
            return
        else:
            # iterate locations in environment
            for r2 in enumerate(environment_locations):
                if (r2 is not p and contains([p,r2],environment_transitions) is True):
                    _lt2 = environment.transtisions[(p,r2)] 
                    expr2 = timed_design_e.precondition + ", " + timed_design_i.postcondition + ", " + _lt2 # F(p,r2) = p /\ R /\ l't(p,r2)
                    for r1 in enumerate(interface_locations):
                        if (r1 is not q and contains([q,r1],interface_transitions) is True):
                            # lt(q,r1) /\ F(p,r2) is satisfiable
                            _lt1 = interface.transtisions[(q,r1)]
                            expr1 = _lt1 + ", " + expr2
                            expr = "And(" + expr1 + ")"
                            if (check_sat(expr) is True):
                                # check if expr2 => lt(q,r1) is false
                                
                                s = "Implies(" + expr2 + "," + _lt1 + ")"
                                if (check_sat(s) is False):
                                    print "No"
                                    return
                                else:
                                    d.update({(r2,r1):"unmarked"}) 
                                    


            
          
        


    
'''def check_refinement(interface1, interface2):
    
    # convert interface sets into lists
                
    interface1_locations = list(interface1.locations)
    interface1_transitions = list(interface1.transtisions)
    
    # convert environment sets into list
    
    interface2_locations = list(interface2.locations)
    interface2_transitions = list(interface2.transtisions)
    q = interface1.initial_state
    p = interface2.initial_state
    f = {p : q}  # initiate f(p0) = {q0)
        
    for k in f.keys():
        for v in f.values():
            if (f[k] is v):
                _ls1 = interface1.ls[v]
                _ls2 = interface2.ls[k]
                if check_refine_ls(_ls1,_ls2) is True:
                    for r2 in enumerate(interface2_locations):
                        if(r2 is not p and contains((p,r2), interface2_transitions)):    # Get every transition start with state p
                            _lt2 = interface2.transtisions[(p,r2)]
                            expr1 = "And(" + _ls2.precondition + "," + _ls1.postcondition + "," + _lt2 + ")"
                            if(check_sat(expr1) is True):  '''
            
    
    






