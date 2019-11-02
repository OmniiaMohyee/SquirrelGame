from typing import TypeVar, List, Tuple, MutableSet, MutableMapping, Optional
from problem import Problem
from queue import PriorityQueue
import math 
import copy 

State = TypeVar("State")
Action = TypeVar("Action")

# A Breadth First Search Implementation which takes a problem and optionally an initial state
# and returns a list of actions to reach the nearest goal or None if there is no solution
def bfs(problem: Problem[State, Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: List[State] = [initial_state]
    visited: MutableSet[State] = set()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    while len(frontier) > 0:
        current_state = frontier.pop(0)
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, _ = problem.get_successor(current_state, action)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                frontier.append(successor)
    return None

def ucs(problem: Problem[State,Action], initial_state: Optional[State] = None) -> Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: PriorityQueue
    visited : MutableSet[state] = set()
    frontier = PriorityQueue()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    frontier.put((0,initial_state))
    while not(frontier.empty()):
        tmp = frontier.get()
        current_state = tmp[1]
        cost = tmp[0]
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        else:
            visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, _ = problem.get_successor(current_state, action)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                tmp = cost + problem.get_cost(successor)
                frontier.put((tmp,successor))
    return None
        
def g_bfs(problem: Problem[State,Action], initial_state: Optional[State] = None)->Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: PriorityQueue
    visited : MutableSet[state] = set()
    frontier = PriorityQueue()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    frontier.put((0,initial_state))
    while not(frontier.empty()):
        tmp = frontier.get()
        current_state = tmp[1]
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        else:
            visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, _ = problem.get_successor(current_state, action)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                tmp = problem.heuristic(successor)
                frontier.put((tmp,successor))
    return None

def A_star(problem: Problem[State,Action], initial_state: Optional[State] = None)->Optional[List[Action]]:
    initial_state = initial_state or problem.initial_state
    frontier: PriorityQueue
    visited : MutableSet[state] = set()
    frontier = PriorityQueue()
    predecessor: MutableMapping[State, Tuple[State, Action]] = {initial_state: (None, None)}
    frontier.put((0,initial_state))
    while not(frontier.empty()):
        tmp = frontier.get()
        current_state = tmp[1]
        cost = tmp[0]
        if problem.is_goal(current_state):
            solution = []
            while True:
                current_state, action = predecessor[current_state]
                if action is None:
                    return solution
                else:
                    solution.insert(0, action)
        if current_state in visited:
            continue
        else:
            visited.add(current_state)
        for action in problem.get_actions(current_state):
            successor, _ = problem.get_successor(current_state, action)
            if successor not in predecessor:
                predecessor[successor] = (current_state, action)
                tmp = cost + problem.get_cost(current_state) + problem.heuristic(successor)
                frontier.put((tmp,successor))
    return None            
            
