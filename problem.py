from typing import TypeVar, Generic, List, Tuple

State = TypeVar("State")
Action = TypeVar("Action")

# This is a generic base class for Problems
class Problem(Generic[State, Action]):

    # Class methods are similar to static methods but can be run from both the class and its instances
    @classmethod
    def read_from_file(cls, file_path: str) -> 'Problem':
        return Problem()

    # Returns the initial state
    @property
    def initial_state(self) -> State:
        return None

    # Returns a list of possible actions from the given state
    def get_actions(self, state: State) -> List[Action]:
        return []

    # Given a state and a valid action, return the next state and the action cost
    def get_successor(self, state: State, action: Action) -> Tuple[State, float]:
        return state, 0

    # Checks if the given state is a goal
    def is_goal(self, state: State) -> bool:
        return False
    
    # Calculate the heuristic of the given state
    def heuristic(self, state: State) -> float:
        return 0

