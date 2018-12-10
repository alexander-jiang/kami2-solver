import statespace as kami2
import deterministic_search as search
import informed_search

puzzle18_graph = {
    1: frozenset([2, 8]),
    2: frozenset([1, 3]),
    3: frozenset([2, 4, 8]),
    4: frozenset([3, 5, 8]),
    5: frozenset([4, 6]),
    6: frozenset([5, 7, 9, 13, 17, 18, 19, 20, 26]),
    7: frozenset([6, 9, 17]),
    8: frozenset([1, 3, 4, 10, 11, 12, 13, 15]),
    9: frozenset([6, 7]),
    10: frozenset([8, 14]),
    11: frozenset([8, 12, 14]),
    12: frozenset([8, 11, 14, 15, 16, 18, 21, 23]),
    13: frozenset([6, 8, 15]),
    14: frozenset([10, 11, 12, 16]),
    15: frozenset([8, 12, 13, 18]),
    16: frozenset([12, 14, 21]),
    17: frozenset([6, 7, 26]),
    18: frozenset([6, 12, 15, 19, 20, 22, 24, 25]),
    19: frozenset([6, 18]),
    20: frozenset([6, 18]),
    21: frozenset([12, 16]),
    22: frozenset([18, 23]),
    23: frozenset([12, 22]),
    24: frozenset([18,]),
    25: frozenset([18,]),
    26: frozenset([6, 17])
}
puzzle18_node_colors = {
    1: 'w',
    2: 'o',
    3: 'b',
    4: 'w',
    5: 'o',
    6: 'b',
    7: 'w',
    8: 'c',
    9: 'o',
    10: 'w',
    11: 'o',
    12: 'b',
    13: 'o',
    14: 'c',
    15: 'w',
    16: 'o',
    17: 'c',
    18: 'o',
    19: 'c',
    20: 'c',
    21: 'w',
    22: 'w',
    23: 'o',
    24: 'b',
    25: 'w',
    26: 'w'
}
puzzle18_moves_left = 5

puzzle18_step0 = kami2.PuzzleState(puzzle18_graph, puzzle18_node_colors, puzzle18_moves_left)
puzzle18 = kami2.Kami2Puzzle(puzzle18_step0)

# print("Solving using DFS:")
# search.DepthFirstSearch().solve(puzzle18)
#
# print("Solving using UCS:")
# search.UniformCostSearch().solve(puzzle18)

print("Solving using A* (# colors heuristic):")
informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle18)

# color distance heuristic is too slow...
# print("Solving using A* (color distance heuristic):")
# informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle18)
