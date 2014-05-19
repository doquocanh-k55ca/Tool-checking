''' This function checks two given interface and environment,
     which is represented by labeled automata, by using algorithm checking plugability 
Created on Apr 21, 2014

@author: geek
'''

from timed_design import *

class automata(object):
    def __init__(self, locations, inputs, outputs, initial_state, transitions, ls, lt):
        self.locations = locations
        self.inputs = inputs
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
    for key in location_pairs.keys():  # Check if exist an unmarked pair
        if (location_pairs[key] is "unmarked"):
            return key
    return False

def is_transition(location1, location2, transitions):
    if (location1 != location2 and contains((location1, location2), transitions)):
        return True
    return False

def get_timed_design(location, automata):
    return automata.ls[location]

def get_guard_formula(transition, automata):
    return automata.lt[transition]

# F(p,r2) = p /\ R /\ l't(p,r2)

def get_f_constraint(environment_location1, environment_location2, interfacenvironment_location, interface, environment):
    timed_design_interface = get_timed_design(interfacenvironment_location, interface)
    timed_design_environment = get_timed_design(environment_location1, environment)
    if (is_transition(environment_location1, environment_location2, list(environment.transitions)) == True):
        lt = get_guard_formula((environment_location1, environment_location2), environment)
        condition1 = timed_design_environment.precondition
        condition2 = timed_design_interface.postcondition
        constraint = "And(" + condition1 + "," + condition2 + "," + lt + ")"
        return constraint

# lt(q,r1) /\ F(p,r2)

def get_lt(interfacenvironment_location1, interfacenvironment_location2, interface):
    if (is_transition(interfacenvironment_location1, interfacenvironment_location2, list(interface.transitions)) == True):
        lt = interface.lt[interfacenvironment_location1, interfacenvironment_location2]
        return lt

def find_all_phi_q(p, q, listROne, interface, environment):
    dictROneNPhiQ = {}
    for rOne in listROne:
        listPhiQ = []
        f = get_f_constraint(p, rOne, q, interface, environment)
        #Get ListPhiQ
        for interface_location in interface.locations:
            if is_transition(q,interface_location, interface.transitions) is True:
                #Get Lt(q,r)
                lt = get_lt(q, interface_location, interface)
                #Get F(q',rOne)
                # Get Constraint between fl and f
                constraint = get_and_constraint(lt, f)
                if (check_satisfiability(constraint) is True):
                    listPhiQ.append(interface_location)

        # Check Satisfi
        constraintLT = get_or_constraint(q,listPhiQ,interface)
        if check_satisfiability(get_imply_constraint(f,constraintLT)) is False:
            #Not plug
            return {}
        else:       
            dictROneNPhiQ[rOne] = listPhiQ
    return dictROneNPhiQ

def update_transition_status(listROne, dictROneNPhiQ,location_pairs):
    print listROne
    for rOne in listROne:
        for phiQ in dictROneNPhiQ[rOne]:
            if (rOne, phiQ) in location_pairs.keys():
                if location_pairs[(rOne,phiQ)] is not "marked":
                    location_pairs.update({(rOne, phiQ):"unmarked"})
            else:
                location_pairs.update({(rOne, phiQ):"unmarked"})


def get_or_constraint(q,listPhiQ, interface):
    stringLTOfPhiQ = "Or("
    for phiQ in listPhiQ:
        stringLTOfPhiQ += get_lt(q,phiQ,interface) + ','

    #remove the last comma    
    return stringLTOfPhiQ[:-1] + ")"

def find_all_r_one(p, q, interface, environment):
    #ROne is r'
    ROne = []
    for environment_location in environment.locations:
        if(is_transition(p, environment_location, environment.transitions)):
            f = get_f_constraint(p, environment_location, q, interface, environment)
            if(check_satisfiability(f) == True):
                ROne.append(environment_location)
    return ROne

def check_plugability (interface, environment):
    index = ()
    location_pairs = {(environment.initial_state,interface.initial_state):"unmarked"}
    while True:
        index = has_unmarked_index(location_pairs)
        if (index == False):  # no unmarked found
            return True
        # Get tuple of locations (q,p)
        
        q = index[1]
        
        p = index[0]
        
        print index
        
        location_pairs[index] = "marked"
      
        # Get timed design corresponding to q and p state
        
        timed_design_interface = interface.ls[q]
        timed_design_environment = environment.ls[p]
      
        # Check if ls(q) is refinement of ls(q')
    
        if check_refine_ls(timed_design_interface, timed_design_environment) is False:
            return False
        else:
            listROne = find_all_r_one(p,q,interface,environment)
            dictROneNPhiQ = find_all_phi_q(p,q,listROne,interface,environment)
            #Check dictionary Empty
            if not dictROneNPhiQ:
                return False
            else:
                update_transition_status(listROne,dictROneNPhiQ,location_pairs)

