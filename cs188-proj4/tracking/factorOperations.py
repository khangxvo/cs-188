# factorOperations.py
# -------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from typing import List
from bayesNet import Factor
import functools
from util import raiseNotDefined

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors: List[Factor], joinVariable: str):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print("Factor failed joinFactorsByVariable typecheck: ", factor)
            raise ValueError("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()

########### ########### ###########
########### QUESTION 2  ###########
########### ########### ###########

def joinFactors(factors: List[Factor]):
    """
    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = functools.reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print("Factor failed joinFactors typecheck: ", factor)
            raise ValueError("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) + 
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))


    "*** YOUR CODE HERE ***"


    condi_var = []
    uncondi_var = []
    var_domain_dict = []
    factors_list = [i for i in factors]
    var_domain_dict = factors_list[0].variableDomainsDict()

    # print(var_domain_dict)

    for f in factors:

        
        # var_domain_dict = f.variableDomainsDict()
        
        # get alll the conditional variable
        for i in f.conditionedVariables():
            if i not in condi_var:
                condi_var.append(i)

        # get all unconditional variable
        for i in f.unconditionedVariables():
            if i not in uncondi_var:
                uncondi_var.append(i)

    # filter condition factor since we computing joint factor
    for var in uncondi_var:
        if var in condi_var:
            condi_var.remove(var)

    # create a new Factor
    newFactor = Factor(uncondi_var, condi_var, var_domain_dict)

    assignments = newFactor.getAllPossibleAssignmentDicts()
    # print("all assingment")
    # print(assignments)
    for a in assignments:
        prob = 1
        
        # print("an assigment")
        # print(a)
        
        #* for each assignment, compute the product of their factors
        
        #* for example factor = {P(D|W), P(W)}, assignment = {D=dry, W=wet}
        #* => prob = P(D=dry | W=wet) * P(W=wet)
        for f in factors:

            # print("a factor")
            # print(f)

            # print("a probability of current assigment")
            # print(f.getProbability(a))
            prob *= f.getProbability(a)

        newFactor.setProbability(a, prob)

    return newFactor


    # verion 2
    # factors_list = [i for i in factors]
    # unconditioned_variables = []
    # conditioned_variables = []
    # variablesDomainDict = factors_list[0].variableDomainsDict()

    # # Fill up our unconditioned_variables and conditioned_variables lists
    # for factor in factors_list:
    #     unconditioned_variables += [i for i in factor.unconditionedVariables() if i not in unconditioned_variables]

    #     conditioned_variables += [i for i in factor.conditionedVariables() if i not in conditioned_variables]

    # # Filters the conditioned_varaibles list
    # for variable in unconditioned_variables:
    #     if variable in conditioned_variables:
    #         conditioned_variables.remove(variable)

    # retFactor = Factor(unconditioned_variables, conditioned_variables, variablesDomainDict)

    # # Getting and calculating the probabilities
    # assignments = retFactor.getAllPossibleAssignmentDicts()
    # for assignment in assignments:
    #     probability = 1
    #     for factor in factors_list:
    #         probability = probability * factor.getProbability(assignment)

    #     retFactor.setProbability(assignment, probability)
    
    # return retFactor

    "*** END YOUR CODE HERE ***"

########### ########### ###########
########### QUESTION 3  ###########
########### ########### ###########

def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor: Factor, eliminationVariable: str):
        """
        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print("Factor failed eliminate typecheck: ", factor)
            raise ValueError("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"

        # get all variable domain
        variable_domain_dict = factor.variableDomainsDict()

        # get the domain of eliminate var
        eliminate_var_domain = variable_domain_dict[eliminationVariable]

        # get the condi var list
        cond_var = factor.conditionedVariables()

        # get uncond var list and remove elimiateVar
        uncond_var = factor.unconditionedVariables()
        uncond_var.remove(eliminationVariable)

        # create a new factor
        newFactor = Factor(uncond_var, cond_var, variable_domain_dict)
        newFactorAssginment = newFactor.getAllPossibleAssignmentDicts()

        oldFactorAssignment = factor.getAllPossibleAssignmentDicts()

        #// print(oldFactorAssignment)

        for newA in newFactorAssginment:
            '''
            for each factor in the new assignments,
            group together the old assignments that have the 
            all {key: val} pairs similar to the new assignments
            '''
            cur = []
            newAKeys = list(newA.keys())
            #// print("1st loop")
            #// print(newAKeys)
            
            for oldA in oldFactorAssignment:
                
                #// print("2nd loop")
                #// print(oldA)
                #// print(newA)

                # there may be multiple keys so this flag
                # make sure that we only add if all keys match
                addThisAssignment = True

                for k in newAKeys:
                    
                    if newA[k] != oldA[k]:
                        # if the val not match, we break immediately and do not add
                        addThisAssignment = False
                        break

                if addThisAssignment:
                    cur.append(oldA)
                    #// print("add oldA")
                    #// print(cur)
                #// print(cur)
            
            #// groups.append(cur)

            # We start eliminate var once we finished grouping.
            # I also start calculate the prob for new factor here.
            prob = 0
            for a in cur:
                prob += factor.getProbability(a)

            # Set new factor value
            newFactor.setProbability(newA, prob)
                

        #// print(groups)
        return newFactor






        # groups = []
        # all_assignments = factor.getAllPossibleAssignmentDicts()

        # for domain in eliminate_var_domain:
            
        #     cur = []
        #     for a in all_assignments:
        #         if a[eliminationVariable] == domain:
        #             cur.append(a)

        #     groups.append(cur)

        # print(groups)

        
        "*** END YOUR CODE HERE ***"

    return eliminate

eliminate = eliminateWithCallTracking()

