from typing import Callable, TypeVar, Optional, List
from problem import Problem
from importlib import import_module
import argparse

# Notice that in all these files we use type definitions to help make the code safer

State = TypeVar("State")
Action = TypeVar("Action")

# This is a type definition for a search function that take a problem and optionally an initial state and return a list of actions or None
SearchFunction = Callable[[Problem[State,Action], Optional[State]], Optional[List[Action]]]

def count_calls(fn):
    def decorated(*args, **kwargs):
        decorated.count += 1
        return fn(*args, **kwargs)
    setattr(decorated, 'count', 0)
    return decorated

def main(args):
    module_name, problem_name = args.problem.split('.')
    module = import_module(module_name) # Dynamically load the problem module (this equivalent to "import module_name as module" but module_name is a string)
    problem_class: Problem = getattr(module, problem_name) # get the problem class from the module

    module_name, search_name = args.search.split('.')
    module = import_module(module_name) # Dynamically load the search module
    search_fn: SearchFunction = getattr(module, search_name) # get the search function from the module

    problem = problem_class.read_from_file(args.test_file) # read the problem from a file

    # decorate 'get_successor' to count function calls
    setattr(problem_class, 'get_successor', count_calls(getattr(problem_class, 'get_successor')))

    initial_state = problem.initial_state
    print("Initial State:")
    print(initial_state)
    print("Heuristic:", problem.heuristic(initial_state))

    print("Searching for a solution...")
    solution = search_fn(problem, initial_state)
    
    if solution is None:
        print("No solution was found")
    else:
        path_cost = 0
        current_state = initial_state
        for idx, action in enumerate(solution):
            print(f'Action-{idx+1}:', action)
            current_state, cost = problem.get_successor(current_state, action)
            path_cost += cost
            print(current_state)
            print("Cost:", cost)
            print("Heuristic:", problem.heuristic(current_state))
        print("Solution found with", len(solution), "steps:", solution)
        print("Total Path Cost:", path_cost)
    print('"get_successor" was called', problem_class.get_successor.count, 'time(s)')

# This part will only be called if the file is called directly from python (no imported).
if __name__ == "__main__":
    # The argument parser helps us parse the arguments written by the user in the commandline
    # The following setup reads 3 arguments in order:
    # "problem" which contains the problem module and class (e.g. maze.Maze)
    # "search" which contains the search module and function (e.g. search.bfs)
    # "test_file" which contains the path to the test case file (e.g. maze_test_cases/test1.txt)
    parser = argparse.ArgumentParser("Problem Solver")
    parser.add_argument("problem")
    parser.add_argument("search")
    parser.add_argument("test_file")
    args = parser.parse_args()

    main(args)