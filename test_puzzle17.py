import statespace as kami2
import deterministic_search as search
import informed_search

puzzle17_graph = {
    1: frozenset([2, 3, 4, 5]),
    2: frozenset([1, 3, 6, 10]),
    3: frozenset([1, 2, 4, 6]),
    4: frozenset([1, 3, 5, 6, 7]),
    5: frozenset([1, 4, 7, 8, 9, 12]),
    6: frozenset([2, 3, 4, 8, 9, 10]),
    7: frozenset([4, 5, 8]),
    8: frozenset([5, 6, 7, 9]),
    9: frozenset([5, 6, 8, 10, 12]),
    10: frozenset([2, 6, 9, 11, 12, 13, 14, 16]),
    11: frozenset([10]),
    12: frozenset([5, 9, 10]),
    13: frozenset([10, 14, 16]),
    14: frozenset([10, 13, 15]),
    15: frozenset([14, 16]),
    16: frozenset([10, 13, 15])
}
puzzle17_node_colors = {
    1: 'o',
    2: 'b',
    3: 'c',
    4: 'b',
    5: 'w',
    6: 'o',
    7: 'o',
    8: 'b',
    9: 'c',
    10: 'w',
    11: 'o',
    12: 'b',
    13: 'o',
    14: 'b',
    15: 'o',
    16: 'b'
}
puzzle17_moves_left = 4

puzzle17_step0 = kami2.PuzzleState(puzzle17_graph, puzzle17_node_colors, puzzle17_moves_left)
puzzle17 = kami2.Kami2Puzzle(puzzle17_step0)

def main():
    print("Solving using DFS:")
    search.DepthFirstSearch().solve(puzzle17)

    # print("Solving using UCS:")
    # search.UniformCostSearch().solve(puzzle17)

    print("Solving using A* (# colors heuristic):")
    informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle17)

    # color distance heuristic is significantly slower but this problem is small enough
    # print("Solving using A* (color distance heuristic):")
    # informed_search.AStarSearch(informed_search.color_distance_heuristic).solve(puzzle17)

if __name__ == "__main__":
    main()
