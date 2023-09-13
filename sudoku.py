from sudoku_constraints9x9 import constraint9x9
from sudoku_constraints4x4 import constraint4x4
from sudoku_constraints6x6 import constraint6x6
from puzzles import *
from copy import deepcopy
from collections import OrderedDict
from flask import Flask, render_template, request, Request

class ConstraintProblem:
    '''
    Values- The actual value of the original board. This is either 1 number, or None. Stored as a Dictionary.
    Domains- The range of values the cell can be. Stored as a Dictionary.
    Constraints- The constraints the values can be.
    '''
    def __init__(self, puzzle: list[list[int]], constraints: dict, size: int):
        '''
        Constructor
        Takes in a puzzle (2D list) and constraints (Dictionary from import)
        '''
        domains = {}
        values = {}
        for i, arri in enumerate(puzzle):
            for j, arrj in enumerate(arri):
                key = 'C' + str(i+1) + str(j+1)
                if arrj is None:
                    domains[key] = list(range(1,size+1))
                else:
                    domains[key] = [arrj]
                values[key] = arrj
        self.values = values
        self.domains = domains
        self.constraints = constraints

'''
CSP4x4 = ConstraintProblem(puzzle4x4,constraint4x4,4)
CSPpuzzle1 = ConstraintProblem(puzzle1,constraint9x9,9)
CSPpuzzle2 = ConstraintProblem(puzzle2,constraint9x9,9)
CSPpuzzle3 = ConstraintProblem(puzzle3,constraint9x9,9)
CSPpuzzle4 = ConstraintProblem(puzzle4,constraint9x9,9)
CSPpuzzle5 = ConstraintProblem(puzzle5,constraint9x9,9)
'''

def revise(CSP: ConstraintProblem, C1: str, C2: str) -> bool:
    '''
    Params:
        CSP- A Constraint Satisfactory Problem.
        C1- A string, representing the first cell.
        C2, string, representing the second cell.
    Returns
        A boolean, whether a value in the first cell was removed from the puzzle.
    Desc:
        Checks whether the passed in cells satisfy the constraints in the CSP.
        If they do not, C1s value is removed.
    '''
    #Get Constraint, C1 and C2 may be out of order
    constraint = CSP.constraints[(min(C1, C2), max(C1, C2))]

    revised = False
    for i in CSP.domains[C1]:
        success = False

        for j in CSP.domains[C2]:
            if [i,j] in constraint:
                success = True
                break
        #Could not find a C1 for C2
        if not success:
            CSP.domains[C1].remove(i)
            revised = True
    return revised

def AC3(CSP: ConstraintProblem) -> bool:
    '''
    Params:
        CSP- A Constraint Satisfactory Problem.
    Returns:
        A boolean, whether all cells in the CSP have a value left.
    Desc:
        Checks all of the cells in the CSP and removes ALL inconsistent values using the AC-3 algorithm.
    '''
    #Begin queue with all constraints
    queue = list(CSP.constraints.keys())

    while queue != []:
        constraint = queue.pop()

        #Revise, change 1st
        if revise(CSP, constraint[0], constraint[1]):
            if not CSP.domains[constraint[0]]:
                return False
            for i in CSP.constraints:
                if constraint[0] in i:
                    queue.append(i)

        #Revise, change 2nd
        if revise(CSP, constraint[1], constraint[0]):
            if not CSP.domains[constraint[1]]:
                return False
            for i in CSP.constraints:
                if constraint[1] in i:
                    queue.append(i)
    return True

def minimumRemainingValues(CSP: ConstraintProblem, assignments: dict) -> str:
    '''
    Params:
        CSP- A Constraint Satisfactory Problem.
        assignments- A dictionary of variable assignments from backtracking.
    Returns:
        A string, the variable with the fewest values including the variable assignments.
    Desc:
        Returns the earliest cell with the least amount of values that has not been assigned.
    '''
    #Starting value, gets changed into the first value that is not assigned
    minCell = ''
    for key, value in CSP.domains.items():
        if key not in assignments and not CSP.values[key]:
            if minCell == '' or len(value) < len(CSP.domains[minCell]):
                minCell = key
    return minCell

def backtrack(CSP: ConstraintProblem) -> OrderedDict:
    '''
    Params:
        CSP- A Constraint Satisfactory Problem.
    Returns:
        An Ordered Dictionary with the value of each solution
    Desc:
        A backtracking search that finds a valid assignment for all cells in the CSP should it exist.
        Uses the AC-3 as well as the minimumRemainingValues as its heuristic.
        If not all cells are filled, the domains should be returned.
    '''
    def backtracking(CSP: ConstraintProblem, assignments: OrderedDict) -> OrderedDict:
        '''
        Params:
            CSP- A Constraint Satisfactory Problem.
            assignments- Ordered dictionary of variable assignments. Starts blank.
        '''
        
        #Complete assignment
        allFilled = True
        for key in CSP.domains:
            if not CSP.values[key]and key not in assignments:
                allFilled = False
                break
        if allFilled:
            return assignments
    
        parentDomain = deepcopy(CSP.domains)
        var = minimumRemainingValues(CSP,assignments)
        for value in parentDomain[var]:
            #Assignment and domain updated 
            assignments[var] = value
            CSP.domains[var] = [value]
            #Domains updated inside AC3 function
            if AC3(CSP):
                result = backtracking(CSP,assignments)
                if result:
                    return result
            #Revert all changes from AC3 if failure
            del assignments[var]
            CSP.domains = parentDomain

    #Start of backtrack
    #Running AC3 before var for better accuracy
    if not AC3(CSP):
        return
    return backtracking(CSP,OrderedDict())
'''
#Testing
print("4x4 Puzzle")
try:
    for key, value in backtrack(CSP4x4).items():
        print(key, value)
    print()
    print("Puzzle 1")
    try:
        for key, value in backtrack(CSPpuzzle1).items():
            print(key, value)
    except:
        print("Failed")
    print()
    print("Puzzle 2")
    try:
        for key, value in backtrack(CSPpuzzle2).items():
            print(key, value)
    except:
        print("Failed")
    print()
    print("Puzzle 3")
    try:
        for key, value in backtrack(CSPpuzzle3).items():
            print(key, value)
    except:
        print("Failed")
    print()
    print("Puzzle 4")
    try:    
        for key, value in backtrack(CSPpuzzle4).items():
            print(key, value)
    except:
        print("Failed")
    print()
    print("Puzzle 5")
    try:
        for key, value in backtrack(CSPpuzzle5).items():
            print(key, value)
    except:
        print("Failed")
    print()
except:
    print("Failed 4x4")
'''

app = Flask(__name__,static_folder='static')
@app.route('/')
def website():
    '''
    Params:
        None
    Returns:
        None
    Desc:
        A webapp using Flask.
        The user inputs whether 4x4 or 9x9 should be solved
        The user inputs a sudoku puzzle on the site and then presses a button.
        The puzzle is then generated into a CSP and a solution is found with the backtrack function.
        If backtrack returns an ordered assignment dictionary, each step is shown on the site.
        n missing values will have n steps.
        If None is returned, "No Answer" will display on the site.
    '''
    return render_template('start.html')

def generateBoard(size: int, request: Request) -> list[list[int]]|str:
    '''
    Params:
        size, an integer of the board size
        request, a request object passed into the function
    Returns:
        a list of list, the board
        or a string, an error
    '''
    if request.method == 'GET':
        return "Input a puzzle."
    elif request.method == 'POST':
        numArr = list(range(1,size+1))
        custom = [[None for i in range(size)] for j in range(size)]
        form = request.form
        for i in form:
            if form[i] != '' and i[-1] != 'G':
                try:
                    if int(form[i]) not in numArr:
                        return "Invalid number in a cell."
                except ValueError:
                    return "Invalid value in a cell."
                custom[int(i[1])-1][int(i[2])-1] = int(form[i])
    return custom

#TODO Normalize constraints to genrate constraints upon loading.
def generateConstraints(groups: list[str], size: int) -> dict:
    '''
    Params:
        Groups: a list of strings defining cells in each group
        Size: an integer representing how big the board is
    Returns:
        A dictionary, the constraints generated by the function
    Desc:
        Generates any kind of constraint, (but mainly used for the 9x9 Irregular)
    '''
    init = []
    constraints = []
    for i in range(1,size+1):
        for j in range(1,size+1):
            init.append('C' + str(i) + str(j))
    for i in range(1,size+1):
        for j in range(1,size+1):
            if i != j:
                constraints.append([i,j])
    result = {}
    for i in range(len(init)):
        for j in range(len(init)):
            if init[0] != init[j]:
                if init[0][1] == init[j][1] or init[0][2] == init[j][2]:
                    result[(init[0],init[j])] = constraints
                else:
                    for group in groups:
                        if init[0] in groups[group] and init[j] in groups[group]:
                            result[(init[0],init[j])] = constraints
        init.pop(0)
    return result


@app.route('/4x4', methods=['GET','POST'])
def board4x4():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('4x4.html')

@app.route('/4x4/solve', methods=['GET','POST'])
def solve4x4():
    custom = generateBoard(4, request)
    if type(custom) is str:
        return custom
    result = backtrack(ConstraintProblem(custom,constraint4x4,4))
    if result != None:
        return render_template('solve4x4.html', data=result, original=custom)
    return "No Answer."

@app.route('/6x6', methods=['GET','POST'])
def board6x6():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('6x6.html')

@app.route('/6x6/solve', methods=['GET','POST'])
def solve6x6():
    custom = generateBoard(6, request)
    if type(custom) is str:
        return custom
    result = backtrack(ConstraintProblem(custom,constraint6x6,6))
    if result != None:
        return render_template('solve6x6.html', data=result, original=custom)
    return "No Answer."
if __name__ == "__main__":
    app.run(host='localhost')

@app.route('/9x9', methods=['GET','POST'])
def board9x9():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('9x9.html')

@app.route('/9x9/solve', methods=['GET','POST'])
def solve9x9():
    custom = generateBoard(9, request)
    if type(custom) is str:
        return custom
    result = backtrack(ConstraintProblem(custom,constraint9x9,9))
    if result != None:
        return render_template('solve9x9.html', data=result, original=custom)
    return "No Answer."

@app.route('/9x9I', methods=['GET','POST'])
def board9x9I():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('9x9I.html')
    
@app.route('/9x9I/solve', methods=['GET','POST'])
def solve9x9Irregular():
    form = request.form
    groups = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': []}
    for i in form:
        if i[-1] == 'G':
            if not form[i]:
                return "All cells must belong to a group"
            else:
                groups[form[i]].append(i[:3])
    for value in groups.values():
        if len(value) != 9:
            return "All groups must have 9 squares" 
    custom = generateBoard(9, request)
    if type(custom) is str:
        return custom
    result = backtrack(ConstraintProblem(custom,generateConstraints(groups,9),9))
    if result != None:
        return render_template('solve9x9I.html', data=result, original=custom, groups=groups)
    return "No Answer."

if __name__ == "__main__":
    app.run(host='localhost')