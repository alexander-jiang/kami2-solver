import statespace as kami2
import informed_search

puzzle98_graph = {
    1: frozenset([4]),
    2: frozenset([4]),
    3: frozenset([5]),
    4: frozenset([1, 2, 5]),
    5: frozenset([3, 4, 6, 7, 8]),
    6: frozenset([5, 9, 10, 14]),
    7: frozenset([5, 10, 11, 14]),
    8: frozenset([5, 11, 12, 13, 14]),
    9: frozenset([6, 14]),
    10: frozenset([6, 7, 14]),
    11: frozenset([7, 8, 14]),
    12: frozenset([8, 14]),
    13: frozenset([8, 14]),
    14: frozenset([6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]),
    15: frozenset([14]),
    16: frozenset([14]),
    17: frozenset([14]),
    18: frozenset([14]),
    19: frozenset([14]),
    20: frozenset([14]),
    21: frozenset([14]),
    22: frozenset([14]),
    23: frozenset([14]),
    24: frozenset([14]),
    25: frozenset([14, 26]),
    26: frozenset([25, 27]),
    27: frozenset([26, 28]),
    28: frozenset([27, 29]),
    29: frozenset([28])
}
puzzle98_node_colors = {
    1: 'p',
    2: 'p',
    3: 'y',
    4: 'y',
    5: 'r',
    6: 'y',
    7: 'y',
    8: 'y',
    9: 'r',
    10: 'r',
    11: 'r',
    12: 'r',
    13: 'r',
    14: 'g',
    15: 'dr',
    16: 'dr',
    17: 'dr',
    18: 'dr',
    19: 'dr',
    20: 'dr',
    21: 'dr',
    22: 'dr',
    23: 'dr',
    24: 'dr',
    25: 'p',
    26: 'g',
    27: 'p',
    28: 'r',
    29: 'dr'
}
puzzle98_moves_left = 6

puzzle98_step0 = kami2.PuzzleState(puzzle98_graph, puzzle98_node_colors, puzzle98_moves_left)
puzzle98 = kami2.Kami2Puzzle(puzzle98_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle98)

    # print("Solving using A* (# colors heuristic):")
    # informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle98)

    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle98)

if __name__ == "__main__":
    main()
