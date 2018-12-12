import statespace as kami2
import deterministic_search as search
import informed_search

puzzle71_graph = {
    1: frozenset([2]),
    2: frozenset([1, 3, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]),
    3: frozenset([2, 4, 5, 6, 7, 8, 9]),
    4: frozenset([3, 12, 13, 14, 28, 29, 34, 35, 36]),
    5: frozenset([3, 14, 15, 16, 29, 30, 35, 36, 37, 38]),
    6: frozenset([3, 16, 17, 18, 30, 31, 37, 38, 39, 40]),
    7: frozenset([3, 18, 19, 20, 31, 32, 39, 40, 41, 42]),
    8: frozenset([3, 20, 32, 33, 41, 42, 43]),
    9: frozenset([3, 43]),
    10: frozenset([11, 12, 34]),
    11: frozenset([10, 21]),
    12: frozenset([4, 10, 21]),
    13: frozenset([4, 21]),
    14: frozenset([4, 5, 21]),
    15: frozenset([5, 21]),
    16: frozenset([5, 6, 21]),
    17: frozenset([6, 21]),
    18: frozenset([6, 7, 21]),
    19: frozenset([7, 21]),
    20: frozenset([7, 8, 21]),
    21: frozenset([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27]),
    22: frozenset([21]),
    23: frozenset([21]),
    24: frozenset([21]),
    25: frozenset([21]),
    26: frozenset([21]),
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
    53: frozenset([2, 48])
}
puzzle71_node_colors = {
    1: 'y',
    2: 'r',
    3: 'g',
    4: 'y',
    5: 'y',
    6: 'y',
    7: 'y',
    8: 'y',
    9: 'y',
    10: 'y',
    11: 'g',
    12: 'g',
    13: 'g',
    14: 'g',
    15: 'g',
    16: 'g',
    17: 'g',
    18: 'g',
    19: 'g',
    20: 'g',
    21: 'r',
    22: 'g',
    23: 'g',
    24: 'g',
    25: 'g',
    26: 'g',
    27: 'g',
    28: 'g',
    29: 'g',
    30: 'g',
    31: 'g',
    32: 'g',
    33: 'g',
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
    53: 'y'
}
puzzle71_moves_left = 5

puzzle71_step0 = kami2.PuzzleState(puzzle71_graph, puzzle71_node_colors, puzzle71_moves_left)
puzzle71 = kami2.Kami2Puzzle(puzzle71_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle71)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle71)

    # 6242 states explored, solution:  [(2, 'g'), (2, 'y'), (12, 'y'), (12, 'r'), (12, 'g')]
    # print("Solving using A* (# colors heuristic):")
    # informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle71)

    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle71)

if __name__ == "__main__":
    main()
