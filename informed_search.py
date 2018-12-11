import copy
import itertools

import statespace as kami2
import deterministic_search as search

def num_colors_heuristic(state):
    """
    If any color is only in one node, then an optimistic estimate is that all
    subsequent moves will be able to simultaneously eliminate a color and
    contract one of the remaining colors to a single node i.e. it must take at
    least (# colors) - 1 moves to solve the puzzle.
    If not, then we optimistically assume that a color can be contracted to a
    single node in one move, and then one color can be eliminated per move after
    that i.e. it must take at least (# colors) moves to solve the puzzle.
    """
    color_counts = {}
    for color in state.colors:
        color_counts[color] = 0
    for node in state.nodes():
        color_counts[state.get_color(node)] += 1

    for color in state.colors:
        if color_counts[color] == 1:
            return state.num_colors() - 1
    return state.num_colors()

def color_distance_heuristic(state):
    """
    Consider all of the nodes of each color. If you know the maximum of the
    pairwise distances between any two nodes of the same color, then the
    optimistic estimate is that the color can be contracted to a single node
    in half (rounded up) of that max distance. But you should pick the color
    that is easiest to contract first, as doing so could help contract other
    colors.
    """
    # print("WARNING This heuristic is *really* slow...")
    nodes = state.nodes()
    # how many moves to contract one color to a single node?
    moves_to_contract = state.moves_left

    pairwise_distances = state.get_pairwise_distances()
    for color in state.colors:
        max_dist_for_color = -float('inf')
        color_nodes = []
        for node in nodes:
            if state.get_color(node) == color:
                color_nodes.append(node)

        for (node1, node2) in itertools.combinations(color_nodes, 2):
            distance = pairwise_distances[node1][node2]
            # print("distance between %d & %d = %d" % (node1, node2, distance))
            optimistic_num_moves = (distance + 1) // 2
            if optimistic_num_moves > max_dist_for_color:
                max_dist_for_color = optimistic_num_moves
        # print("moves to contract color %s = %d" % (color, max_dist_for_color))
        if max_dist_for_color < moves_to_contract:
            moves_to_contract = max_dist_for_color
    return moves_to_contract + state.num_colors() - 1


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
