import random
import numpy as np
import math

def fitness_function(configuration):
    """Compute the fitness function for a given board configuration.

    Arguments:
        configuration (list[int]): N-Queen board configuration represented as a list of row indices.

    Returns:
        The fitness function value (number of attacking pairs)

    TODO: Implement 
    """
    # print (self.configuration)
    clashes=0
    #row-col clashes= subtract the unique length of array from the total length of the array,
    rc_clash= abs(len(configuration)-len(np.unique(configuration)))
    # print ("Number of row clashes", rc_clash)
    clashes+= rc_clash
    
    for i in range (0, len(configuration)):
        #running a loop over the list
        for j in range (i+1, len(configuration)):
            offset= j-i
            if(configuration[i] == configuration[j]-offset or configuration[i] == configuration[j]+offset):
               clashes+=1


    #diagonal clashes
    #The ideal case can yield 28 arrangements of non attacking pairs. Therefore max fitness is 28.
    # print("Board Configuration", configuration)
    # print("Number of clashes", clashes)
    return clashes

class Board():
    """Chess board for N-Queens.

    Arguments:
        size (int): The size of the board.
        threshold_steps (int): parameter controlling early quit in case of local minima.
    """

    def __init__(self, size = 8, threshold_steps = 10000):
        self.size = size
        self.threshold_steps = threshold_steps
        self.found_solution = False
        self.configuration=[3,2,3,0]

        """
        TODO:
        1. The following property can be initialized to any list type (numpy array, list etc.)
        """
        #creates a list of unique numbers from 0-8, might not be necerssary but this way column collision is minimized
        # self.configuration = random.sample(range(0,size),size)
#        self.configuration=[]
#        for i in range(size):
#            self.configuration.append(random.randint(0,size-1))
#        print("Before running Algorithm",self.configuration)

    def run_hill_climbing(self):
        """Run the hill climbing algorithm.

        TODO:
        1. This function should update self.configuration and self.found_solution appropriately as you run the algorithm. 
        2. This function should make iterative calls to self.make_hill_climbing_move for each step.
        """

        step=0
        while (fitness_function(self.configuration) > 0 and not self.found_solution):
            self.configuration= self.make_hill_climbing_move()
            # new_fitness= fitness_function(self.configuration)
            #making sure tht the temperature doesnt get very low
            if step > self.threshold_steps:
                break

        if(fitness_function(self.configuration)== 0):
            self.found_solution= True
        else:
            self.found_solution=False
        
        

    def make_hill_climbing_move(self):
        """Make one move using hill climbing.

        TODO:
        1. This function should update self.configuration by one step using fitness_function.
        """
        # print ("Current Fitness",fitness_function( self.configuration))
        # if(fitness_function(self.configuration) == 0):
        #     #no queens are attacking
        #     self.found_solution=True
        #     return self.configuration


        #how do we know which one to move?
        moves = {}
        for col in range(len(self.configuration)):
            
            for row in range(len(self.configuration)):
            
                copy_configuration= list(self.configuration)
                #Move the queen to the new row
                copy_configuration[col]=row
                moves[(col,row)] = fitness_function(copy_configuration)
        bestmoves=[]

        curr_fitness= fitness_function(self.configuration)

        for k,v in moves.items():
            #finds the first good move
            if v < curr_fitness:
                curr_fitness=v
                if(len(bestmoves)==0):
                    bestmoves.append(k)
                else:
                    bestmoves.pop(0)
                    bestmoves.append(k)

       # Move is happening here

        if len(bestmoves)==0:
            self.found_solution=True
            return self.configuration

        else:
            col=bestmoves[0][0]
            row=bestmoves[0][1]
            bestmoves.pop(0)
            self.configuration[col]= row
            print("Next Move", self.configuration)

        return self.configuration



    def run_simulated_annealing(self, temperature, anneal_rate):
        """Run the simulated annealing algorithm.

        Arguments: 
            temperature (float): Initial temperature for simulated annealing.
            anneal_rate (float): The rate at which the temperature is annealed.

        TODO:
        1. This function should update self.configuration and self.found_solution appropriately as you run the algorithm. 
        2. This function should make iterative calls to self.make_annealing_move for each step.
        """

        step=0
        while fitness_function(self.configuration) > 0:
            self.configuration= self.make_annealing_move(temperature)
            new_fitness= fitness_function(self.configuration)
            #making sure tht the temperature doesnt get very low
            new_temperature = max(temperature * anneal_rate,0.01)
            temperature=new_temperature
            if step > self.threshold_steps:
                break

    def make_annealing_move(self, temperature):
        """Make one move using simulated annealing.

        Arguments:
            temperature (float): Current temperature.

        TODO:
        1. This function should update self.configuration by one step using fitness_function.
        """

        board_copy=list(self.configuration)
        found_move=False
        # Random move
        nrow= random.randint(0,len(board_copy)-1)
        ncol= random.randint(0,len(board_copy)-1)
        board_copy[ncol]=nrow
        n_fitness=fitness_function(board_copy)

        # if better definately choose this step
        if n_fitness < fitness_function(self.configuration):
            found_move=True
        else:
            #Can we still consider the choice even though it was bad (Based on Probability)
            delta_energy = fitness_function(self.configuration) - n_fitness
            #Probability can never exceed 1
            accept_probability = min(1,math.exp(delta_energy/temperature))
            found_move = random.random() <= accept_probability
   
        return board_copy




def main():
    n = 8
    threshold_steps = 10000

    board1 = Board(n, threshold_steps)
    # print("Board1 before hill climbing",board1)
    board1.run_hill_climbing()
    
    print("After running Hillclimbing",board1.configuration)
    # print ("Found Solution? or stuck at local max",board1.found_solution)
    board2 = Board(n, threshold_steps)
    board2.run_simulated_annealing(n**2, 0.95)
    print("After running Simulated Annealing",board2.configuration)
    # print ("Found Solution? or stuck at local max",board2.found_solution)

if __name__ == '__main__':
    main()
