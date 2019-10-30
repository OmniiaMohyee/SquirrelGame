from typing import Any, List, Tuple
from problem import Problem
from vector import Vector
from map2d import Map2D
import math

Directions = {
    "UP": Vector(0, -1),
    "DOWN": Vector(0, 1),
    "LEFT": Vector(-1, 0),
    "RIGHT": Vector(1, 0)
}

GROUND_SYMBOL = "."
WALL_SYMBOL = "#"
GOAL_SYMBOL = "X"
AGENT_SYMBOL = "@"

class Maze(Problem['Maze.State', str]):

    @classmethod
    def read_from_file(cls, file_path: str) -> 'Maze':
        with open(file_path, 'r') as f:
            grid = [[cell for cell in line.strip()] for line in f.readlines()]
            
            height = len(grid)
            assert height > 0, "Map height must be greater than zero"
            width = max(len(row) for row in grid)
            assert width > 0, "Map width must be greater than zero"

            positions = [Vector(x,y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == AGENT_SYMBOL]
            assert len(positions) == 1, "There must be one agent in the maze"
            initial_position = positions[0]
            
            grid[initial_position[1]][initial_position[0]] = GROUND_SYMBOL
            for row in grid:
                row.extend([WALL_SYMBOL]*(width - len(row)))
            return Maze(Map2D(grid), initial_position)

    # Define a state of the Maze problem. This class is immutable and hashable so that it can be used by the search function
    class State:
        __slots__ = ("problem", "position")
        problem: 'Maze'
        position: Vector


        def __init__(self, problem: 'Maze', position: Vector):
            super().__setattr__("problem", problem)
            super().__setattr__("position", position)
        
        def __setattr__(self, name: str, value: Any):
            raise NotImplementedError("Maze.State is immutable")

        def __hash__(self):
            return hash(self.position)
        
        def __lt__(self, value: 'Maze.State') -> bool:
            return False

        def __eq__(self, value: 'Maze.State') -> bool:
            return self.position == value.position
        
        def __str__(self) -> str:
            return '\n'.join(''.join(AGENT_SYMBOL if self.position == (x,y) else cell for x, cell in enumerate(row)) for y, row in enumerate(self.problem.grid))
            

    def __init__(self, grid: Map2D, initial_position: Vector):
        super().__init__()
        self.grid = grid
        self.initial_position = initial_position
    
    @property
    def initial_state(self) -> 'Maze.State':
        return Maze.State(self, self.initial_position)
    
    def get_actions(self, state: 'Maze.State') -> List[str]:
        return [name for name, direction in Directions.items() if self.grid.inside(state.position+direction) and self.grid[state.position+direction] != WALL_SYMBOL]

    def get_successor(self, state: 'Maze.State', action: str) -> Tuple['Maze.State', float]:
        return Maze.State(self, state.position+Directions[action]), 1

    def is_goal(self, state: 'Maze.State') -> bool:
        return self.grid[state.position] == GOAL_SYMBOL
    
    def heuristic(self, state: 'Maze.State'):
        distance_fn = lambda v1, v2: abs(v1.x - v2.x) + abs(v1.y - v2.y)
        goal_positions = [Vector(x,y) for y, row in enumerate(self.grid) for x, cell in enumerate(row) if cell == GOAL_SYMBOL]
        min_distance = min((distance_fn(state.position, goal) for goal in goal_positions), default=math.inf)
        return min_distance