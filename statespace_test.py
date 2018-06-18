import statespace as kami2
import deterministic_search as search
import informed_search
import copy

puzzle6_graph = {
    1: frozenset([2]),
    2: frozenset([1, 3, 4, 5]),
    3: frozenset([2, 4, 6]),
    4: frozenset([2, 3, 5, 6]),
    5: frozenset([2, 4, 6]),
    6: frozenset([3, 4, 5, 7]),
    7: frozenset([6]),
}
puzzle6_node_colors = {
    1: 'b',
    2: 'r',
    3: 'y',
    4: 'b',
    5: 'y',
    6: 'r',
    7: 'b',
}
puzzle6_moves_left = 3
print "### Puzzle 6 initial state:"
print puzzle6_graph
print puzzle6_node_colors

puzzle6_step0 = kami2.PuzzleState(puzzle6_graph, puzzle6_node_colors, puzzle6_moves_left)
puzzle6 = kami2.Kami2Puzzle(puzzle6_step0)

assert puzzle6_step0.num_colors() == 3, "Puzzle should have 3 colors, actually has: %d" % puzzle6_step0.num_colors()
assert puzzle6_step0.moves_left == 3, "Puzzle should have 3 moves left, actually has: %d" % puzzle6_step0.moves_left
assert not puzzle6.is_terminal_state(puzzle6_step0), "Puzzle should not be in a terminal state!"

def testSetColor(step_num, node_to_update, new_color, prev_state,
                 num_colors, new_neighbors, moves_left, is_terminal):
    print "### %d. Setting color of node %d to '%s'" % (step_num, node_to_update, new_color)
    save_prev_node_colors = copy.deepcopy(prev_state.node_colors)
    save_prev_graph = copy.deepcopy(prev_state.graph)
    new_state = prev_state.set_color(node_to_update, new_color)

    assert puzzle6.start_state() == puzzle6_step0, "Puzzle's start state should not have changed!"
    assert new_state.moves_left == moves_left, "Puzzle should have %d moves left, actually has: %d" % (moves_left, new_state.moves_left)
    assert prev_state.node_colors == save_prev_node_colors, "Previous state's node_colors should be unchanged!"
    assert prev_state.graph == save_prev_graph, "Previous state's graph should be unchanged!"

    assert new_state.num_colors() == num_colors, "Puzzle should have %d colors, actually has: %d" % (num_colors, new_state.num_colors())
    assert new_state.node_colors[node_to_update] == new_color, "Contracted node has wrong color!"
    assert new_state.graph[node_to_update] == new_neighbors, "Contracted node has wrong neighbors!"

    print new_state.graph
    print new_state.node_colors
    if is_terminal:
        assert puzzle6.is_terminal_state(new_state), "Puzzle should be in a terminal state!"
        if len(new_state.colors) == 1:
            print "### Solved!"
    else:
        assert not puzzle6.is_terminal_state(new_state), "Puzzle should not be in a terminal state!"

    return new_state

step_num = 1
node_to_update = 4
new_color = 'y'
puzzle6_step1 = testSetColor(step_num, node_to_update, new_color, puzzle6_step0,
                             3, set([2, 6]), 2, False)

step_num += 1
node_to_update = 4
new_color = 'r'
puzzle6_step2 = testSetColor(step_num, node_to_update, new_color, puzzle6_step1,
                             2, set([1, 7]), 1, False)

step_num += 1
node_to_update = 4
new_color = 'b'
puzzle6_step3 = testSetColor(step_num, node_to_update, new_color, puzzle6_step2,
                             1, set([]), 0, True)

print "Solving using DFS:"
search.DepthFirstSearch().solve(puzzle6)

print "Solving using UCS:"
search.UniformCostSearch().solve(puzzle6)

print "Solving using A*:"
informed_search.AStarSearch(informed_search.num_colors_heuristic).solve(puzzle6)
