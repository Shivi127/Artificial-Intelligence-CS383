from eight_puzzle import Puzzle
import queue
import time
import math
import numpy as np
################################################################
### Node class and helper functions provided for your convience.
### DO NOT EDIT!
################################################################
class Node:
    """
    A class representing a node.
    - 'state' holds the state of the node.
    - 'parent' points to the node's parent.
    - 'action' is the action taken by the parent to produce this node.
    - 'path_cost' is the cost of the path from the root to this node.
    """
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def gen_child(self, problem, action):
        """
        Returns the child node resulting from applying 'action' to this node.
        """
        return Node(state=problem.transitions(self.state, action),
                    parent=self,
                    action=action,
                    path_cost=self.path_cost + problem.step_cost(self.state, action))

    @property
    def state_hashed(self):
        """
        Produces a hashed representation of the node's state for easy
        lookup in a python 'set'.
        """
        return hash(str(self.state))

################################################################
### Node class and helper functions provided for your convience.
### DO NOT EDIT!
################################################################
def retrieve_solution(node,num_explored,num_generated):
    """
    Returns the list of actions and the list of states on the
    path to the given goal_state node. Also returns the number
    of nodes explored and generated.
    """
    actions = []
    states = []
    while node.parent is not None:
        actions += [node.action]
        states += [node.state]
        node = node.parent
    states += [node.state]
    return actions[::-1], states[::-1], num_explored, num_generated

################################################################
### Node class and helper functions provided for your convience.
### DO NOT EDIT!
################################################################
def print_solution(solution):
    """
    Prints out the path from the initial state to the goal given
    a tuple of (actions,states) corresponding to the solution.
    """
    actions, states, num_explored, num_generated = solution
    print('Start')
    for step in range(len(actions)):
        print(puzzle.board_str(states[step]))
        print()
        print(actions[step])
        print()
    print('Goal')
    print(puzzle.board_str(states[-1]))
    print()
    print('Number of steps: {:d}'.format(len(actions)))
    print('Nodes explored: {:d}'.format(num_explored))
    print('Nodes generated: {:d}'.format(num_generated))


################################################################
### Skeleton code for your Astar implementation. Fill in here.
################################################################
class Astar:
    """
    A* search.
    - 'problem' is a Puzzle instance.
    """
    def __init__(self, problem):
        self.problem = problem
        self.init_state = problem.init_state
        self.num_explored = 0
        self.num_generated = 1

        
        
    def solve(self, method='man'):
        """
        Perform A* search and return a solution using `retrieve_solution'
        (if a solution exists).
        pass method to the heuristic function h 
        """
        node = Node(state=self.problem.init_state,
                    parent=None,
                    action=None,
                    path_cost=0)

        init_state = node.state
        goal_state = self.problem.goal_state
        if(set(init_state) != set(goal_state)):
            return None
        #print(" Board State : ",node.state)
        num_explored = int(0)
        num_generated = int(0)
        #print (node.state, "State")
        ################################################################
        ### Your code here.
        ################################################################
        pq= queue.PriorityQueue() #for finding the next node to explore
        explored= set() #to keep track of explored states
        frontier= set()


        pq.put((self.f(node, method),0,node)) #the priorityqueue stores a tuple with (f(n),node)
        frontier.add(node.state_hashed)
        
        while not pq.empty():
            #get the node with the highest priority, time to break ties, node is in the third place in the tuple
            current_node = pq.get()[2]
            
            explored.add(current_node.state_hashed)
      

            if(self.problem.goal_state == current_node.state):
                return retrieve_solution(current_node, len(explored), num_generated)
            num_explored+=1
            for action in self.problem.actions(current_node.state):
                #print("Inside Actions")
                generated_time=time.time()
                child= current_node.gen_child(self.problem,action)
                
                #print ("Child's State", child.state)
                not_in_q= True
                num_generated+=1


                if((child.state_hashed not in explored) and (child.state_hashed not in frontier)):
                        pq.put((self.f(child,method),generated_time,child))
                        frontier.add(current_node.state_hashed)

        print("Returning None")
        return None


    def f(self,node, method):
        '''
        Returns a lower bound estimate on the cost from root through node
        to the goal.
        '''
        return node.path_cost + self.h(node, method)

    def h(self,node, method='man'):
        '''
        Returns a lower bound estimate on the cost from node to the goal
        using the different heuristics. 
        '''
        ################################################################
        ### Your code here.

        ################################################################

        
        
    
        if method == 'man':
            #sum of horizontal and vertical distance

            init_state = node.state
            goal_state = self.problem.goal_state
            return sum(abs(b%3 - g%3) + abs(b//3 - g//3)
                       for b, g in ((init_state.index(i), goal_state.index(i)) for i in range(1, 9)))
 

        elif method == 'rowcol':
            rcCount=0

            frow=[0,1,2]
            srow=[3,4,5]
            trow=[6,7,8]
            for i in range (0,len(self.problem.goal_state)):
                #checking if in the right column or not
                if (node.state[i]%3) != (i%3):
                    rcCount+=1
                #checking for the right row or not
                if((node.state[i] <=2 and (node.state[i] not in frow))):
                   rcCount+=1
                elif(node.state[i] >=3 and node.state[i] <=5 and (node.state[i] not in srow)):
                   rcCount+=1
                elif(node.state[i]>=6 and node.state[i] not in trow):
                   rcCount+=1
                else:
                    continue
                   
            return rcCount
        # compute rowcol heuristic
        


        
        elif method == 'misplaced':
            mCount=0
            for i in range (0,len(self.problem.goal_state)):
                if node.state[i] != self.problem.goal_state[i]:
                    mCount+=1
            return mCount# compute misplaced tiles the number of tiles out of place

        
        elif method == 'null':
            return 0 # compute null heuristic
        else:
            return 0

    
    
    def method_stats(self, board, trials=10, method='man'):
        '''
        Returns an mean and standard deviation of the number of nodes expanded
        '''
        # write code here to randomly generate puzzles and
        # compute the mean and standard deviation of the number
        # nodes expanded. You can use np.mean() and np.std()

        expanded_mean = 0.
        expanded_std = 0.

        expanded_count=[]
        i=1
        for t in range(trials):
            puzzle = Puzzle(board).shuffle()
            solver = Astar(puzzle)
            actions, states, num_explored, num_generated = solver.solve(method=method)

            ############################################################
            ### Compute upper bound for branching factor and update b_hi
            ### Your code here.
            ############################################################
            #print("I am in here", i)
            expanded_count.append(num_generated)
            #i+=1

        expanded_mean=np.mean(expanded_count)
        expanded_std= np.std(expanded_count)
        return expanded_mean, expanded_std


if __name__ == '__main__':
    # Simple puzzle test
    board = [[3,1,2],
             [4,0,5],
             [6,7,8]]

    puzzle = Puzzle(board)
    solver = Astar(puzzle)
    solution = solver.solve()
    print_solution(solution)

   # Harder puzzle test
    board = [[7,2,4],
             [5,0,6],
             [8,3,1]]
    
    
    puzzle = Puzzle(board)
    solver = Astar(puzzle)
    solution = solver.solve()
    print(len(solution[0]))

   


    method='man'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))

      # branching factor test
    method='rowcol'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))


      # branching factor test
    method='misplaced'
    emean, estd = solver.method_stats(board, trials=100, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))


      # branching factor test
    method='null'
    emean, estd = solver.method_stats(board, trials=5, method=method)
    print('mean and standard deviation: {0:.2f}, {1:.2f} using heuristic: {2}'.format(emean, estd, method))
