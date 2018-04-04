from sudoku import Sudoku
from copy import deepcopy
import numpy as np



class CSP_Solver(object):
    """
    This class is used to solve the CSP with backtracking using the minimum value remaining heuristic.
    HINT: you will likely want to implement functions in the backtracking sudo code in figure 6.5 in the text book.
            We have provided some prototypes that might be helpful. You are not required to use any functions defined
            here and can modify any function other than the solve method. We will test your code with the solve method
            and so it must have no parameters and return the type it says. 
         
    """
    def __init__(self, puzzle_file):
        '''
        Initialize the solver instance. The lower the number of the puzzle file the easier it is. 
        It is a good idea to start with the easy puzzles and verify that your solution is correct manually. 
        You should run on the hard puzzles to make sure you aren't violating corner cases that come up.
        Harder puzzles will take longer to solve.
        :param puzzle_file: the puzzle file to solve 
        '''
        self.sudoku = Sudoku(puzzle_file) # this line has to be here to initialize the puzzle
        # print ("Sudoku", Sudoku.board_str(self.sudoku))
        # print("board", self.sudoku.board) - List of Lists 
        self.num_guesses = 0
        # self.unassigned = deque()
        self.assignment = {}
        
        # make domian the Given Puzzle
        self.domains = deepcopy(self.sudoku.board)
        # Overwrite 0's with their possiblilities.
        for row in range(0,9):
            for col in range(0,9):
                # extract value
                value = self.sudoku.board[row][col]
                if value == 0:
                    self.domains[row][col] = [1,2,3,4,5,6,7,8,9]
                    # add this index to unassigned for faster look ups
                    # self.unassigned.append((row,col))
                else: 
                    self.domains[row][col] = value
                    self.assignment[(row, col)] = value

        vars=[]
        # self.csp = CSP(vars, self.domains)

    ################################################################
    ### YOU MUST EDIT THIS FUNCTION!!!!!
    ### We will test your code by constructing a csp_solver instance
    ### e.g.,
    ### csp_solver = CSP_Solver('puz-001.txt')
    ### solved_board, num_guesses = csp_solver.solve()
    ### so your `solve' method must return these two items.
    ################################################################
    def free_variables(self, var):
        # given a variable it finds the number of free values in the domian, and the possiblities 
        # var[0]= row, var[1]= col
        possible_domain=[1,2,3,4,5,6,7,8,9]

        # Row check
        vrow=var[0]
        vcol=var[1]

        for col in [x for x in range(0,9) if x!= vcol]:
            board_value= self.sudoku.board[vrow][col]
            if board_value!=0 and board_value in possible_domain:
                possible_domain.remove(board_value)

        # Column Check
        for row in [x for x in range(0,9) if x!= vrow]:
            board_value= self.sudoku.board[row][vcol]
            if board_value!=0 and board_value in possible_domain:
                possible_domain.remove(board_value)

        # Box Check
        row_start= vrow//3 * 3
        col_start= vcol//3 * 3

        for row in [x for x in range(row_start, row_start+3) if x!= vrow]:
            for col in [x for x in range(col_start,col_start+3) if x!= vcol]:
                board_value= self.sudoku.board[row][col]
                if board_value!=0 and board_value in possible_domain:
                    possible_domain.remove(board_value)

        return len(possible_domain),possible_domain


    def select_unassigned_var(self, board):
        '''
        Function that should select an unassigned variable to assign next
        You do not have to use this
        :param board: list of lists
        :return: variable
        '''

        # returns the idex of the first missing tile 
        leastval_pos=None # to store a tuple with (row,col) value of the least domain
        least_domain=[]
        nleast=9


        for row in range(0,9):
            for col in range(0,9):
                val= self.sudoku.board[row][col]
                if val == 0:
                    p_length, p_domain =self.free_variables((row,col))
                    # finding the coordinates of the least domain
                    if(p_length< nleast):
                        nleast= p_length
                        leastval_pos=(row, col)
                        least_domain=p_domain
        return leastval_pos, least_domain


    def consistent(self, var, value):
        '''
        This function checks to see if assigning value to var on board violates any of the constraints
        You do not need to use this function
        :param var: variable to be assigned, tuple (row col) 
        :param value: value to assign to var
        :param board: board state (list of list)
        :param constraints: to check to see if they are violated
        :return: True if consistent False otherwise
        '''

        # Row check
        vrow=var[0]
        vcol=var[1]

        for col in [x for x in range(0,9) if x!= vcol]:
            board_value= self.sudoku.board[vrow][col]
            if board_value == value:
                return False

        # Column Check
        for row in [x for x in range(0,9) if x!= vrow]:
            board_value= self.sudoku.board[row][vcol]
            if board_value == value:
                return False

        # Box Check
        row_start= vrow//3 * 3
        col_start= vcol//3 * 3

        for row in [x for x in range(row_start, row_start+3) if x!= vrow]:
            for col in [x for x in range(col_start,col_start+3) if x!= vcol]:
                board_value= self.sudoku.board[row][col]
                if board_value == value:
                    return False

        return True

    def solve(self):
        '''
        This method solves the puzzle initialized in self.sudoku 
        You should define backtracking search methods that this function calls
        The return from this function NEEDS to match the correct type
        Return None, number of guesses no solution is found
        :return: tuple (list of list (ie [[]]), number of guesses
        '''
        self.backtracking_search()
        print ("board", self.sudoku.board)
        print("num",self.num_guesses)
        return self.sudoku.board, self.num_guesses

    def backtracking_search(self):
        '''
        This function might be helpful to initialize a recursive backtracking search function
        You do not have to use it.
        
        :param sudoku: Sudoku class instance
        :param csp: CSP class instance
        :return: board state (list of lists), num guesses 
        '''

        return self.recursive_backtracking(self.assignment)

    def recursive_backtracking(self, assignment):
        '''
        recursive backtracking search function.
        You do not have to use this
        :param sudoku: Sudoku class instance
        :param csp: CSP class instance
        :return: board state (list of lists)
        '''
        # return a solution or failure
        # if assignment is complete then return the assignment
        if self.sudoku.complete():
            return self.assignment
        # var ← SELECT-UNASSIGNED-VARIABLE(csp)

        var, var_domain= self.select_unassigned_var(self.assignment)
        for d in var_domain:
            # Increment the number of guesses
            self.num_guesses+=1
            # if value is consistent with assignment then 
            # add {var = value} to assignment 
            if self.consistent(var,d):
                assignment[var] = d
                self.sudoku.board[var[0]][var[1]] = d
            result= self.recursive_backtracking(assignment)
            if result is not None:
                return result
            assignment.pop(var)
            self.sudoku.board[var[0]][var[1]] = 0
        return None


    

if __name__ == '__main__':
    csp_solver = CSP_Solver('puz-001.txt')
    solution, guesses = csp_solver.solve()

