import statespace as kami2
import deterministic_search as search
import informed_search

puzzle33_graph = {
    1: frozenset([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
    2: frozenset([1]),
    3: frozenset([1]),
    4: frozenset([1, 12]),
    5: frozenset([1, 12]),
    6: frozenset([1, 12]),
    7: frozenset([1, 12]),
    8: frozenset([1, 12]),
    9: frozenset([1, 12]),
    10: frozenset([1]),
    11: frozenset([1]),
    12: frozenset([4, 5, 6, 7, 8, 9, 13, 14, 15]),
    13: frozenset([12, 16, 17]),
    14: frozenset([12, 17, 18]),
    15: frozenset([12, 16, 18]),
    16: frozenset([13, 15, 19]),
    17: frozenset([13, 14, 19]),
    18: frozenset([14, 15, 19]),
    19: frozenset([16, 17, 18])
}
puzzle33_node_colors = {
    1: 'g',
    2: 'b',
    3: 'o',
    4: 'b',
    5: 'b',
    6: 'b',
    7: 'b',
    8: 'b',
    9: 'b',
    10: 'b',
    11: 'o',
    12: 'g',
    13: 'o',
    14: 'o',
    15: 'o',
    16: 'b',
    17: 'b',
    18: 'b',
    19: 'g'
}
puzzle33_moves_left = 4

puzzle33_step0 = kami2.PuzzleState(puzzle33_graph, puzzle33_node_colors, puzzle33_moves_left)
puzzle33 = kami2.Kami2Puzzle(puzzle33_step0)

def main():
    # print("Solving using DFS:")
    # search.DepthFirstSearch().solve(puzzle33)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle33)

    print("Solving using A* (# colors heuristic):")
    informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle33)

    print("Solving using A* (color distance heuristic):")
    informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle33)

if __name__ == "__main__":
    main()
