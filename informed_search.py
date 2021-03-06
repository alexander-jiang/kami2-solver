import copy

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
    # if any color has only one node left, we're done
    if num_colors_heuristic(state) == state.num_colors() - 1:
        # print("color with only one node")
        return state.num_colors() - 1

    # how many moves to contract one color to a single node?
    moves_to_contract = state.moves_left

    max_dist_for_color = state.get_max_dist_for_color()
    for color in state.colors:
        # print("max dist for color %s = %d" % (color, max_dist_for_color[color]))
        optimistic_num_moves = (max_dist_for_color[color] + 1) // 2
        if optimistic_num_moves < moves_to_contract:
            moves_to_contract = optimistic_num_moves
    return moves_to_contract + state.num_colors() - 1


# Returns a transformed problem such that running UCS on the transformed problem
# is equivalent to running A* on the original problem with the given heuristic.
def transform_a_star_to_ucs(problem, heuristic):
    class NewKami2Puzzle(kami2.Kami2Puzzle):

        ## TODO how to avoid recomputing the heuristic multiple times?
        ## maybe store the terminal state boolean in the state?
        def is_terminal_state(self, state):
            """
            Returns 1 if the given state is a goal state (i.e. all nodes are the
            same color and number of moves remaining is >= 0), returns -1 if given
            state cannot lead to a solution (e.g. number of moves remaining < 0,
            not enough moves to solve even in best case, etc.), and returns 0 otherwise.
            """
            state_heuristic_val = state.update_heuristic_value(heuristic)

            if state.moves_left >= 0 and state.num_colors() == 1:
                return 1
            elif state.moves_left < 0 or state_heuristic_val > state.moves_left:
                ## print if using the specific heuristic check would have pruned
                ## this state where the generic num_colors check would not have
                # if state_heuristic_val > state.moves_left and not (state.num_colors() > state.moves_left + 1):
                #     print(f"heuristic = {state_heuristic_val} but only {state.moves_left} moves left!")
                return -1
            else:
                return 0

        def actions_and_costs(self, state):
            actions_costs = problem.actions_and_costs(state)
            ## TODO use a "soft heuristic" to order the different actions
            ## e.g. average of the graph diameter for each color

            prev_state_heuristic = state.update_heuristic_value(heuristic)
            for i in range(len(actions_costs)):
                action, new_state, cost = actions_costs[i]
                new_state_heuristic = new_state.update_heuristic_value(heuristic)
                new_cost = cost + new_state_heuristic - prev_state_heuristic
                # if new_state_heuristic < prev_state_heuristic:
                #     print(f"new state after action {action}:")
                #     print(f"nodes {[node for node in state.graph if node not in new_state.graph]} removed")
                #     # for node in state.graph:
                #     #     if node not in new_state.graph:
                #     #         print(f"node {node} removed")
                #     #     else:
                #     #         if node in new_state.graph and state.graph[node] != new_state.graph[node]:
                #     #             print(f"neighbors of node {node}: {state.graph[node]} -> {new_state.graph[node]}")
                #     print(f"current state vs initial state:")
                #     print(f"nodes {[node for node in problem.start_state().graph if node not in state.graph]} removed")
                #     print(f"heuristic of new state = {heuristic(new_state)} vs current state = {heuristic(state)}")
                #     print(f"new state: {new_state.moves_left} moves left")
                #     input("enter to continue...")
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
