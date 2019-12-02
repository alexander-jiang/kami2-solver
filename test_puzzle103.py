import statespace as kami2
import informed_search

puzzle103_graph = {
    1: frozenset([2]),
    2: frozenset([1, 3, 10, 11]),
    3: frozenset([2, 4]),
    4: frozenset([3, 5]),
    5: frozenset([4, 6, 12, 13]),
    6: frozenset([5, 7]),
    7: frozenset([6, 8]),
    8: frozenset([7, 9, 14, 15]),
    9: frozenset([8]),
    10: frozenset([2, 11, 16]),
    11: frozenset([2, 10, 12, 17]),
    12: frozenset([5, 11, 13, 17]),
    13: frozenset([5, 12, 14, 18]),
    14: frozenset([8, 13, 15, 18]),
    15: frozenset([8, 14, 19]),
    16: frozenset([10, 20]),
    17: frozenset([11, 12, 21, 22]),
    18: frozenset([13, 14, 23, 24]),
    19: frozenset([15, 25]),
    20: frozenset([16, 21, 26]),
    21: frozenset([17, 20, 22, 26]),
    22: frozenset([17, 21, 23, 27]),
    23: frozenset([18, 22, 24, 27]),
    24: frozenset([18, 23, 25, 28]),
    25: frozenset([19, 24, 28]),
    26: frozenset([20, 21, 29, 30]),
    27: frozenset([22, 23, 31, 32]),
    28: frozenset([24, 25, 33, 34]),
    29: frozenset([26, 30, 35]),
    30: frozenset([26, 29, 31, 36]),
    31: frozenset([27, 30, 32, 36]),
    32: frozenset([27, 31, 33, 37]),
    33: frozenset([28, 32, 34, 37]),
    34: frozenset([28, 33, 38]),
    35: frozenset([29, 39]),
    36: frozenset([30, 31, 40, 41]),
    37: frozenset([32, 33, 42, 43]),
    38: frozenset([34, 44]),
    39: frozenset([35, 40, 45]),
    40: frozenset([36, 39, 41, 45]),
    41: frozenset([36, 40, 42, 46]),
    42: frozenset([37, 41, 43, 46]),
    43: frozenset([37, 42, 44, 47]),
    44: frozenset([38, 43, 47]),
    45: frozenset([39, 40, 48, 49]),
    46: frozenset([41, 42, 50, 51]),
    47: frozenset([43, 44, 52, 53]),
    48: frozenset([45]),
    49: frozenset([45, 50]),
    50: frozenset([46, 49]),
    51: frozenset([46, 52]),
    52: frozenset([47, 51]),
    53: frozenset([47])
}
puzzle103_node_colors = {
    1: 'w',
    2: 'b',
    3: 'r',
    4: 'w',
    5: 'b',
    6: 'r',
    7: 'w',
    8: 'b',
    9: 'r',
    10: 'r',
    11: 'w',
    12: 'r',
    13: 'w',
    14: 'r',
    15: 'w',
    16: 'b',
    17: 'b',
    18: 'b',
    19: 'b',
    20: 'w',
    21: 'r',
    22: 'w',
    23: 'r',
    24: 'w',
    25: 'r',
    26: 'b',
    27: 'b',
    28: 'b',
    29: 'r',
    30: 'w',
    31: 'r',
    32: 'w',
    33: 'r',
    34: 'w',
    35: 'b',
    36: 'b',
    37: 'b',
    38: 'b',
    39: 'w',
    40: 'r',
    41: 'w',
    42: 'r',
    43: 'w',
    44: 'r',
    45: 'b',
    46: 'b',
    47: 'b',
    48: 'r',
    49: 'w',
    50: 'r',
    51: 'w',
    52: 'r',
    53: 'w'
}
puzzle103_moves_left = 8

puzzle103_step0 = kami2.PuzzleState(puzzle103_graph, puzzle103_node_colors, puzzle103_moves_left)
puzzle103 = kami2.Kami2Puzzle(puzzle103_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle103)

    # print("Solving using A* (# colors heuristic):")
    # informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle103)

    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle103)

if __name__ == "__main__":
    main()
