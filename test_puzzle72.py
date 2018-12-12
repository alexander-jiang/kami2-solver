import statespace as kami2
import deterministic_search as search
import informed_search

puzzle72_graph = {
    1: frozenset([2]),
    2: frozenset([1, 3, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]),
    3: frozenset([2, 4, 5, 6, 7, 8, 9]),
    4: frozenset([3, 28, 29, 34, 35, 36, 55, 56]),
    5: frozenset([3, 29, 30, 35, 36, 37, 38, 57, 58]),
    6: frozenset([3, 30, 31, 37, 38, 39, 40, 59, 60]),
    7: frozenset([3, 31, 32, 39, 40, 41, 42, 61, 62]),
    8: frozenset([3, 32, 33, 41, 42, 43, 63]),
    9: frozenset([3, 43]),
    10: frozenset([34, 54]),
    11: frozenset([54, 21]),
    12: frozenset([54, 55, 21]),
    13: frozenset([55, 56, 21]),
    14: frozenset([56, 57, 21]),
    15: frozenset([57, 58, 21]),
    16: frozenset([58, 59, 21]),
    17: frozenset([59, 60, 21]),
    18: frozenset([60, 61, 21]),
    19: frozenset([61, 62, 21]),
    20: frozenset([62, 63, 64]),
    21: frozenset([11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27]),
    22: frozenset([21]),
    23: frozenset([21]),
    24: frozenset([21]),
    25: frozenset([21]),
    26: frozenset([21, 64]),
    27: frozenset([21]),
    28: frozenset([4, 34]),
    29: frozenset([4, 5, 35, 36]),
    30: frozenset([5, 6, 37, 38]),
    31: frozenset([6, 7, 39, 40]),
    32: frozenset([7, 8, 41, 42]),
    33: frozenset([8, 43]),
    34: frozenset([4, 10, 28]),
    35: frozenset([4, 5, 29]),
    36: frozenset([4, 5, 29]),
    37: frozenset([5, 6, 30]),
    38: frozenset([5, 6, 30]),
    39: frozenset([6, 7, 31]),
    40: frozenset([6, 7, 31]),
    41: frozenset([7, 8, 32]),
    42: frozenset([7, 8, 32]),
    43: frozenset([8, 9, 33]),
    44: frozenset([2, 49]),
    45: frozenset([2, 50]),
    46: frozenset([2, 51]),
    47: frozenset([2, 52]),
    48: frozenset([2, 53]),
    49: frozenset([2, 44]),
    50: frozenset([2, 45]),
    51: frozenset([2, 46]),
    52: frozenset([2, 47]),
    53: frozenset([2, 48]),
    54: frozenset([10, 11, 12]),
    55: frozenset([12, 13, 4]),
    56: frozenset([13, 14, 4]),
    57: frozenset([14, 15, 5]),
    58: frozenset([15, 16, 5]),
    59: frozenset([16, 17, 6]),
    60: frozenset([17, 18, 6]),
    61: frozenset([18, 19, 7]),
    62: frozenset([19, 20, 7]),
    63: frozenset([20, 8]),
    64: frozenset([20, 26])
}
puzzle72_node_colors = {
    1: 't',
    2: 'r',
    3: 'g',
    4: 'y',
    5: 'y',
    6: 'y',
    7: 'y',
    8: 'y',
    9: 'y',
    10: 'y',
    11: 'y',
    12: 'y',
    13: 'y',
    14: 'y',
    15: 'y',
    16: 'y',
    17: 'y',
    18: 'y',
    19: 'y',
    20: 'y',
    21: 'r',
    22: 't',
    23: 't',
    24: 't',
    25: 't',
    26: 't',
    27: 'g',
    28: 't',
    29: 't',
    30: 't',
    31: 't',
    32: 't',
    33: 't',
    34: 'r',
    35: 'r',
    36: 'r',
    37: 'r',
    38: 'r',
    39: 'r',
    40: 'r',
    41: 'r',
    42: 'r',
    43: 'r',
    44: 'g',
    45: 'g',
    46: 'g',
    47: 'g',
    48: 'g',
    49: 'y',
    50: 'y',
    51: 'y',
    52: 'y',
    53: 'y',
    54: 'g',
    55: 'g',
    56: 'g',
    57: 'g',
    58: 'g',
    59: 'g',
    60: 'g',
    61: 'g',
    62: 'g',
    63: 'g',
    64: 'r'
}
puzzle72_moves_left = 6

puzzle72_step0 = kami2.PuzzleState(puzzle72_graph, puzzle72_node_colors, puzzle72_moves_left)
puzzle72 = kami2.Kami2Puzzle(puzzle72_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle72)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle72)

    # print("Solving using A* (# colors heuristic):")
    # informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle72)

    # 26 states explored, solution: [(3, 'y'), (62, 'y'), (62, 'r'), (62, 't'), (62, 'y'), (62, 'g')]
    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle72)

if __name__ == "__main__":
    main()
