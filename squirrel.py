from typing import Any, List, Tuple
from problem import Problem
from vector import Vector
from map2d import Map2D

import math
import copy

#Action should modify position, nut count and stash count.
Actions = {
    
    "UP": Vector(0,-1),
    "DOWN": Vector(0,1),
    "LEFT": Vector(-1,0),
    "RIGHT": Vector(1,0),
    "HIDE" : Vector(0,0),
    "TAKE" : Vector(0,0)
    
}

GROUND_SYMBOL = "."
WALL_SYMBOL = "#"
AGENT_SYMBOL = "@"
NUT_SYMBOL = "N"
STASH_SYMBOL = "X"



class Squirrel(Problem):

    def __init__(self, grid: Map2D, initial_position: Vector, nut_count: int,stash_count:int, load:int ):
        super().__init__()
        self.initial_position = initial_position
        self.grid = grid
        self.load = load
        self.stash_count = stash_count
        self.nut_count = nut_count

        


    @classmethod
    def read_from_file(cls, file_path: str) -> 'Problem':
        with open(file_path, 'r') as f:
            grid = [[cell for cell in line.strip()] for line in f.readlines()]
            
            height = len(grid)
            assert height > 0, "Map height must be greater than zero"
            width = max(len(row) for row in grid)
            assert width > 0, "Map width must be greater than zero"

            positions = [Vector(x,y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == AGENT_SYMBOL]
            assert len(positions) == 1, "There must be one agent in the Squirrel"
            initial_position = positions[0]
            positions = [Vector(x,y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == NUT_SYMBOL]
            nut_count = len(positions)
            positions = [Vector(x,y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == STASH_SYMBOL]
            stash_count = len(positions)
            
            grid[initial_position[1]][initial_position[0]] = GROUND_SYMBOL
            for row in grid:
                row.extend([WALL_SYMBOL]*(width - len(row)))
            return Squirrel(Map2D(grid),initial_position,nut_count,stash_count,0)

    class State:
        __slots__ = ("problem","grid" ,"position","nut_count","stash_count","load")
        problem: 'Squirrel'
        position: Vector
        nut_count: int
        stash_count: int
        load : int
        grid : Map2D


        def __init__(self, grid: Map2D ,problem: 'Squirrel', position: Vector, nut_count : int, stash_count : int , load :int):
            super().__setattr__("problem", problem)
            super().__setattr__("position", position)
            super().__setattr__("nut_count",nut_count)
            super().__setattr__("stash_count",stash_count)
            super().__setattr__("load",load)
            super().__setattr__("grid",grid)
            

        
        def __setattr__(self, name: str, value: Any):
            raise NotImplementedError("Squirrel.State is immutable")

        def __hash__(self):
            return hash((self.position,self.grid,self.problem,self.nut_count,self.stash_count,self.load))
        
        def __lt__(self, value: 'Squirrel.State') -> bool:
            return False

        def __eq__(self, value: 'Squirrel.State') -> bool:
            return self.stash_count == value.stash_count and self.grid == value.grid and self.nut_count == value.nut_count and self.position == value.position and self.load == value.load
        
        def __str__(self) -> str:
            return '\n'.join(''.join(AGENT_SYMBOL if self.position == (x,y) else cell for x, cell in enumerate(row)) for y, row in enumerate(self.problem.grid))

 
    @property
    def initial_state(self) -> 'Squirrel.State':
        return Squirrel.State(copy.deepcopy(self.grid),self,self.initial_position, self.nut_count,self.stash_count,self.load)
    
    def get_actions(self, state: 'Squirrel.State') -> List[str]:
        l = [name for name, direction in Actions.items() if state.grid.inside(state.position+direction) and state.grid[state.position+direction] != WALL_SYMBOL]
        if(state.grid[state.position] != NUT_SYMBOL):
            l.remove('TAKE')
        if(state.grid[state.position] != STASH_SYMBOL):
            l.remove('HIDE')
        return l

    def get_successor(self, state: 'Squirrel.State', action: str) -> Tuple['Squirrel.State', float]:
        nut_count = copy.deepcopy(state.nut_count)
        stash_count = copy.deepcopy(state.stash_count)
        load = copy.deepcopy(state.load)
        cost = self.get_cost(state)
        grid = copy.deepcopy(state.grid)

        if(action == "HIDE" and load != 0):
            grid[state.position] = GROUND_SYMBOL
            stash_count -= 1
            load -= 1
            cost = 1
             
        elif(action == "TAKE"):
            grid[state.position] = GROUND_SYMBOL
            nut_count -=1
            load += 1
            cost = 1

        return Squirrel.State(grid,self, state.position+Actions[action],nut_count,stash_count,load), cost

    def is_goal(self, state: 'Squirrel.State') -> bool:
        return state.nut_count == 0 and state.load == 0
    
    def get_cost(self,state: 'Squirrel.State') -> int:
        return sum(range(state.load +1)) + 1

    # def heuristic(self, state: 'Maze.State'):
    #     distance_fn = lambda v1, v2: abs(v1.x - v2.x) + abs(v1.y - v2.y)
    #     stash_positions = [Vector(x,y) for y, row in enumerate(state.grid) for x, cell in enumerate(row) if cell == STASH_SYMBOL]
    #     nut_positions = [Vector(x,y) for y, row in enumerate(state.grid) for x, cell in enumerate(row) if cell == NUT_SYMBOL]
    #     load = copy.deepcopy(state.load)
    #     for nut_position in nut_positions:
    #         min_distance = min((distance_fn(nut_position, stash_position) for stash_position in stash_positions), default=math.inf)
    #     nearest_nut_distance=min((distance_fn(state.position, nut_position) for nut_position in nut_positions), default=math.inf)
    #     nearest_stash_distance=min((distance_fn(state.position, stash_position) for stash_position in stash_positions), default=math.inf)
    #     f=1
    #     if(state.load ==0 )
    #         f=1000
    #     heuristic = min_distance+ min(distance_fn(state.position,nearest_nut_distance),f*distance_fn(state.position,nearest_stash_distance))+get_cost(state.load)+get_cost(state.nut_count)
    #     return heuristic

    
