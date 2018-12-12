import statespace as kami2
import deterministic_search as search
import informed_search

puzzle54_graph = {
    1: frozenset([2, 3, 5]),
    2: frozenset([1, 4]),
    3: frozenset([1, 4, 6]),
    4: frozenset([2, 3, 5, 6, 7, 9, 11, 12]),
    5: frozenset([1, 4, 12, 13]),
    6: frozenset([3, 4, 7]),
    7: frozenset([4, 6, 8]),
    8: frozenset([7, 9]),
    9: frozenset([4, 8, 10]),
    10: frozenset([9, 11]),
    11: frozenset([4, 10, 12, 14]),
    12: frozenset([4, 5, 11]),
    13: frozenset([5, 15, 16, 18]),
    14: frozenset([11, 15, 16, 23]),
    15: frozenset([13, 14, 16]),
    16: frozenset([13, 14, 15, 17, 19, 20, 21, 22]),
    17: frozenset([16, 18]),
    18: frozenset([13, 17, 19]),
    19: frozenset([16, 18, 20, 24]),
    20: frozenset([16, 19, 21]),
    21: frozenset([16, 20, 23, 25]),
    22: frozenset([16, 23]),
    23: frozenset([14, 21, 22]),
    24: frozenset([19, 26, 27, 30]),
    25: frozenset([21, 26, 30, 35]),
    26: frozenset([24, 25, 30]),
    27: frozenset([24, 28]),
    28: frozenset([27, 29, 30]),
    29: frozenset([28, 31]),
    30: frozenset([24, 25, 26, 28, 31, 32, 33, 34]),
    31: frozenset([29, 30, 32]),
    32: frozenset([30, 31, 33]),
    33: frozenset([30, 32, 35]),
    34: frozenset([30, 35]),
    35: frozenset([25, 33, 34])
}
puzzle54_node_colors = {
    1: 'dg',
    2: 'g',
    3: 'y',
    4: 'r',
    5: 'y',
    6: 'dg',
    7: 'y',
    8: 'dg',
    9: 'g',
    10: 'dg',
    11: 'y',
    12: 'dg',
    13: 'r',
    14: 'r',
    15: 'g',
    16: 'dg',
    17: 'y',
    18: 'g',
    19: 'r',
    20: 'g',
    21: 'r',
    22: 'y',
    23: 'g',
    24: 'dg',
    25: 'dg',
    26: 'y',
    27: 'y',
    28: 'r',
    29: 'y',
    30: 'g',
    31: 'dg',
    32: 'y',
    33: 'dg',
    34: 'r',
    35: 'y'
}
puzzle54_moves_left = 7

puzzle54_step0 = kami2.PuzzleState(puzzle54_graph, puzzle54_node_colors, puzzle54_moves_left)
puzzle54 = kami2.Kami2Puzzle(puzzle54_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle54)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle54)

    # print("Solving using A* (# colors heuristic):")
    # informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle54)

    # num states explored: 952, actions:  [(4, 'y'), (16, 'r'), (24, 'r'), (30, 'r'), (30, 'y'), (30, 'dg'), (30, 'g')]
    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle54)

if __name__ == "__main__":
    main()
