import statespace as kami2
import deterministic_search as search
import copy

def num_colors_heuristic(state):
    """
    If there are more nodes than colors, then at least one color must be
    in multiple nodes, so an optimistic estimate is that it will take 1
    move to contract a single color to a single node, and that all
    subsequent moves will be able to simultaneously eliminate a color and
    contract one of the remaining colors to a single node.
    Otherwise, if all colors are all already contracted to one node each,
    then it takes exactly (# colors) - 1 moves to solve the puzzle.
    """
    if len(state.nodes()) > state.num_colors():
        return state.num_colors()
    else:
        return state.num_colors() - 1

# Returns a transformed problem such that running UCS on the transformed problem
# is equivalent to running A* on the original problem with the given heuristic.
def transform_a_star_to_ucs(problem, heuristic):
    class NewKami2Puzzle(kami2.Kami2Puzzle):
        def actions_and_costs(self, state):
            actions_costs = problem.actions_and_costs(state)
            for i in range(len(actions_costs)):
                action, new_state, cost = actions_costs[i]
                new_cost = cost + heuristic(new_state) - heuristic(state)
                actions_costs[i] = action, new_state, new_cost
            return actions_costs
    new_problem = NewKami2Puzzle(problem.start_state())
    return new_problem

class AStarSearch:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def solve(self, problem):
        new_problem = transform_a_star_to_ucs(problem, self.heuristic)
        algorithm = search.UniformCostSearch()
        algorithm.solve(new_problem)

        # Get solution from UCS
        self.actions = algorithm.actions
        if algorithm.total_cost != None:
            self.total_cost = algorithm.total_cost + self.heuristic(problem.start_state())
        else:
            self.total_cost = None
        self.num_states_explored = algorithm.num_states_explored
