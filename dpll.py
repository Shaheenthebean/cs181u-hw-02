from propositional_logic import *

# replace v by e in all disjuncts
# and return resulting list of clauses
def replaceInAllDisjuncts(disjuncts, v, e):
	return [lit.replace1(v, e).simplify() for lit in disjuncts]

# replace v by e in all clauses
# and return resulting list of clauses
def replaceInAllClauses(clauses, v, e):
	return [replaceInAllDisjuncts(dis, v, e) for dis in clauses]

# check if all disjuncts are unsat
# and return True or False
def allDisjunctsUNSAT(disjuncts):
	return all([lit.simplify() == BoolConst(False) for lit in disjuncts])

# check if clauses contains an UNSAT clause
# and return True or False
def containsUNSATClause(clauses):
	return any([allDisjunctsUNSAT(dis) for dis in clauses])

# check if disjuncts has some satisfied disjunct
# and return True or False
def someDisjunctSatisfied(disjuncts):
	return any([lit.simplify() == BoolConst(True) for lit in disjuncts])

# check if all clauses are satisfied
# and return True or False
def allClausesSatisfied(clauses):
	return all([someDisjunctSatisfied(dis) for dis in clauses])

# the main dpll_sat funcion
# nothing to do here, it just calls the helper dpll
def dpll_sat(f):
	varlist = f.getVars()
	clauses = f.cnfListForm()
	return dpll(clauses, varlist)

def dpll(clauses, varlist):
	if containsUNSATClause(clauses):
		return False
	elif allClausesSatisfied(clauses):
		return True
	new_clausesT = replaceInAllClauses(clauses, varlist[0], BoolConst(True))
	new_clausesF = replaceInAllClauses(clauses, varlist[0], BoolConst(False))
	return dpll(new_clausesT, varlist[1:]) or dpll(new_clausesF, varlist[1:])

# the main dpll_model_count funcion
# nothing to do here, it just calls the helper dpll_count
def dpll_model_count(f):
	varlist = f.getVars()
	clauses = f.cnfListForm()
	return dpll_count(clauses, varlist, len(varlist))

def dpll_count(clauses, varlist, t):
	if containsUNSATClause(clauses):
		return 0
	elif allClausesSatisfied(clauses):
		return 2**t
	new_clausesT = replaceInAllClauses(clauses, varlist[0], BoolConst(True))
	new_clausesF = replaceInAllClauses(clauses, varlist[0], BoolConst(False))
	return dpll_count(new_clausesT, varlist[1:], t-1) + dpll_count(new_clausesF, varlist[1:], t-1)

def equiv_dpll(f1, f2):
	return not dpll(Not(Iff(f1, f2)))
