from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush
from queue import Queue, PriorityQueue

# Define possible actions for movement
ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

# Define the AI class
class AI:
    # Constructor: initializes the AI object with a grid and a search type
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    # Set search type (dfs, bfs, ucs, or astar)
    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    # Heuristic function: calculates Manhattan distance between a node and the goal
    def heuristic(self, node):
        return abs(node[0] - self.grid.goal[0]) + abs(node[1] - self.grid.goal[1])
    
    # Set search: Initializes the search algorithm based on the chosen type
    def set_search(self):
        # Common variables for all search types
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}
    

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = Queue()
            self.frontier.put(self.grid.start)
            self.explored = []
        elif self.type == "ucs":
            self.frontier = []
            heappush(self.frontier, (0, self.grid.start))
            self.explored = []
        elif self.type == "astar":
            self.frontier = PriorityQueue()
            self.frontier.put((self.heuristic(self.grid.start), 0, self.grid.start))
            self.explored = set()

    # Check if a node is in the frontier
    def is_in_frontier(self, node):
        return node in self.frontier_nodes
    
    # Get result: calculate the total cost of the path found by the search algorithm
    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    # Make step: execute one step of the chosen search algorithm
    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: 
    def dfs_step(self):
        # If the frontier is empty, the search has failed
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # Pop the current node from the frontier
        current = self.frontier.pop()
        self.explored.append(current)

        # If the current node is the goal, the search is finished
        if current == self.grid.goal :
            self.finished = True
            return

       
        # Generate children nodes by applying actions  
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        # Check if children are valid and not already explored or in the frontier
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    if n == self.grid.goal:
                        self.previous[n] = current
                        self.finished = True
                        return
                    if not n in self.explored and not n in self.frontier:
                        self.previous[n] = current
                        self.frontier.append(n)
                        self.grid.nodes[n].color_frontier = True

    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):
        # If the frontier is empty, the search has failed
        if self.frontier.empty():
            self.failed = True
            self.finished = True
            print("no path")
            return
        # Get the current node from the frontier
        current = self.frontier.get()

        # If the current node is the goal, the search is finished
        if current == self.grid.goal:
            self.finished = True
            return
        
        # Check if the current node has not been explored before
        if current not in self.explored:
            self.explored.append(current)
            children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
            self.grid.nodes[current].color_checked = True
            self.grid.nodes[current].color_frontier = False

        # Check if children are valid and not already explored or in the frontier
            for n in children:
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range) and n not in self.explored and n not in (item for item in self.frontier.queue):
                    if not self.grid.nodes[n].puddle:
                        self.previous[n] = current
                        self.frontier.put(n)
                        self.grid.nodes[n].color_frontier = True

    def ucs_step(self):
        # If the frontier is empty, the search has failed
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # Pop the current node and its cost from the frontier
        cost, current = heappop(self.frontier)

        # If the current node is the goal, the search is finished
        if current == self.grid.goal:
            self.finished = True
            return

        # Check if the current node has not been explored before
        if current not in self.explored:
            self.explored.append(current)
            children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
            self.grid.nodes[current].color_checked = True
            self.grid.nodes[current].color_frontier = False

        # Check if children are valid and update their costs
            for n in children:
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                        child_cost = cost + self.grid.nodes[n].cost()
                        child_in_frontier = next((item for item in self.frontier if item[1] == n), None)
                        # Check if the child node is not explored and not in the frontier
                        if n not in self.explored and child_in_frontier is None:
                            heappush(self.frontier, (child_cost, n))
                            self.previous[n] = current
                            self.grid.nodes[n].color_frontier = True
                        # If the child node is in the frontier but has a lower cost, update the cost
                        elif child_in_frontier and child_cost < child_in_frontier[0]:
                            self.frontier.remove(child_in_frontier)
                            heappush(self.frontier, (child_cost, n))
                            self.previous[n] = current
                            self.grid.nodes[n].color_frontier = True

    def astar_step(self):
        # If the frontier is empty, the search has failed
        if self.frontier.empty():
            self.failed = True
            self.finished = True
            print("no path")
            return
        
        # Get the current node, its cost, and total cost from the frontier
        total_cost, cost, current = self.frontier.get()

        # If the current node is the goal, the search is finished
        if current == self.grid.goal:
            self.finished = True
            return
        
        # Check if the current node has not been explored before
        if current not in self.explored:
            self.explored.add(current)
            children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
            self.grid.nodes[current].color_checked = True
            self.grid.nodes[current].color_frontier = False

            # Check if children are valid and update their costs
            for n in children:
                if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                    if not self.grid.nodes[n].puddle:
                        new_cost = cost + self.grid.nodes[n].cost()
                        heuristic_cost = self.heuristic(n)
                        total_new_cost = new_cost + heuristic_cost
                        # Check if the child node is not explored and not in the frontier
                        if n not in self.explored and n not in [item[2] for item in self.frontier.queue]:
                            self.previous[n] = current
                            self.frontier.put((total_new_cost, new_cost, n))
                            self.grid.nodes[n].color_frontier = True
                        # If the child node is in the frontier but has a lower total cost, update the cost
                        elif n in [item[2] for item in self.frontier.queue]:
                            for idx, (old_total_cost, old_cost, old_node) in enumerate(self.frontier.queue):
                                if old_node == n and total_new_cost < old_total_cost:
                                    self.previous[n] = current
                                    self.frontier.queue[idx] = (total_new_cost, new_cost, n)
                                    self.frontier.queue.sort()
                                    break