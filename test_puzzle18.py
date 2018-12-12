import statespace as kami2
import deterministic_search as search
import informed_search

puzzle18_graph = {
    1: frozenset([2, 3, 5]),
    2: frozenset([1, 3]),
    3: frozenset([1, 2, 4, 5]),
    4: frozenset([3, 5, 16, 17]),
    5: frozenset([1, 3, 4, 6, 7, 10, 13, 14]),
    6: frozenset([5, 7, 8]),
    7: frozenset([5, 6, 8, 10]),
    8: frozenset([6, 7, 9, 10]),
    9: frozenset([8, 10, 11]),
    10: frozenset([5, 7, 8, 9, 11, 12, 13, 23, 24]),
    11: frozenset([9, 10]),
    12: frozenset([10, 24]),
    13: frozenset([5, 10, 14, 16, 21, 23]),
    14: frozenset([5, 13, 16]),
    15: frozenset([16, 18]),
    16: frozenset([4, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23]),
    17: frozenset([4, 16]),
    18: frozenset([15, 16, 19]),
    19: frozenset([16, 18, 20]),
    20: frozenset([16, 19, 22]),
    21: frozenset([13, 16, 23]),
    22: frozenset([16, 20, 23]),
    23: frozenset([10, 13, 16, 21, 22, 24, 25, 26]),
    24: frozenset([10, 12, 23, 25]),
    25: frozenset([23, 24, 26]),
    26: frozenset([23, 25])
}
puzzle18_node_colors = {
    1: 'w',
    2: 'o',
    3: 'b',
    4: 'w',
    5: 'c',
    6: 'w',
    7: 'o',
    8: 'c',
    9: 'o',
    10: 'b',
    11: 'w',
    12: 'o',
    13: 'w',
    14: 'o',
    15: 'o',
    16: 'b',
    17: 'o',
    18: 'w',
    19: 'c',
    20: 'w',
    21: 'c',
    22: 'c',
    23: 'o',
    24: 'w',
    25: 'b',
    26: 'w'
}
puzzle18_moves_left = 5

puzzle18_step0 = kami2.PuzzleState(puzzle18_graph, puzzle18_node_colors, puzzle18_moves_left)
puzzle18 = kami2.Kami2Puzzle(puzzle18_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle18)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle18)

    print("Solving using A* (# colors heuristic):")
    informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle18)
    
    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle18)

if __name__ == "__main__":
    main()
