from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem)

        # TODO: implement backtracking search. 

        assignment = {}
        decision_stack = []
        
        while True:
            assignment, domains = self.propagate(assignment, domains)
            
            if (-1, -1) not in assignment:
                if self.all_assigned(assignment):
                    return self.solution(assignment)
                else:
                    assignment, decision_spot, domains = self.make_decision(assignment, domains, decision_stack)
            else:
                if not decision_stack:
                    return None
                else:
                    assignment, domains = self.backtrack(decision_stack)

    # TODO: add any supporting function you need
    
    def propagate(self, assignment, domains):
        while True:
            changed = []
            for spot in domains:
                if len(domains[spot]) == 1 and spot not in assignment:
                    assignment[spot] = domains[spot][0]
                    changed.append(spot)
            for spot in assignment:
                if len(domains[spot]) > 1:
                    domains[spot] = [assignment[spot]]
                    changed.append(spot)
            for spot in domains:
                if len(domains[spot]) == 0:
                    assignment[(-1, -1)] = -1
                    return assignment, domains

            consistent = True
            for i in changed:
                value = assignment[i]
                for j in sd_peers[i]:
                    if value in domains[j]:
                        domains[j].remove(value)
                        consistent = False
            if consistent:
                return assignment, domains

    def all_assigned(self, assignment):
        return set(sd_spots) == set(assignment.keys())

    def solution(self, assignment):
        return {spot: [value] for spot, value in assignment.items()}

    def make_decision(self, assignment, domains, decision_stack):
        #creates a list of all spots that haven't been assigned a value yet.
        unassigned_spots = [s for s in sd_spots if s not in assignment]
        #select the spot that has the fewest possible values left in its domain. 
        decision_spot = min(unassigned_spots, key=lambda spot: len(domains[spot]))
        #assign the first value in decision_spot's domain to decision_spot.
        assignment[decision_spot] = domains[decision_spot][0]
        #add the current assignment, decision spot, and domains to the decision stack.
        decision_stack.append((copy.deepcopy(assignment), decision_spot, copy.deepcopy(domains)))
        return assignment, decision_spot, domains

    def backtrack(self, decision_stack):
        assignment, decision_spot, domains = decision_stack.pop()
        a = assignment[decision_spot]
        assignment.pop(decision_spot)
        domains[decision_spot].remove(a)
        return assignment, domains


    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
