import unittest

from informed_search import num_colors_heuristic, color_distance_heuristic
from test_puzzle17 import puzzle17
from test_puzzle18 import puzzle18

class TestHeuristics(unittest.TestCase):
    def test_num_colors(self):
        start_state = puzzle17.start_state()
        start_heuristic = num_colors_heuristic(start_state)
        self.assertEqual(start_heuristic, start_state.num_colors(), msg="Heuristic is incorrect for initial state")

        contracting_moves = {
            3: ['b', 'w', 'o'], # only 2 cyan nodes, setting one to another color "contracts"
            6: ['c'], # join the 2 cyan nodes
            9: ['b', 'w', 'o'],
            5: ['b', 'c', 'o'], # only 2 white nodes
            12: ['w'], # 9 and 12 join the 2 white nodes
            10: ['b', 'c', 'o'],
        }
        for action, new_state, cost in puzzle17.actions_and_costs(start_state):
            with self.subTest(action=action):
                node, color = action
                if node in contracting_moves and color in contracting_moves[node]:
                    expected = start_heuristic - 1 # contracted 1 color but 4 colors total
                else:
                    expected = start_heuristic
                actual = num_colors_heuristic(new_state)
                self.assertEqual(actual, expected, msg="Heuristic is incorrect for action (%d, %s)" % (node, color))

    def test_color_distance17(self):
        start_state = puzzle17.start_state()
        start_heuristic = color_distance_heuristic(start_state)
        self.assertEqual(start_heuristic, start_state.num_colors(), msg="Heuristic is incorrect for initial state")

        contracting_moves = {
            3: ['b', 'w', 'o'], # only 2 cyan nodes, setting one to another color "contracts"
            6: ['c'], # join the 2 cyan nodes
            9: ['b', 'w', 'o'],
            5: ['b', 'c', 'o'], # only 2 white nodes
            12: ['w'], # 9 and 12 join the 2 white nodes
            10: ['b', 'c', 'o'],
        }
        for action, new_state, cost in puzzle17.actions_and_costs(start_state):
            with self.subTest(action=action):
                node, color = action
                if node in contracting_moves and color in contracting_moves[node]:
                    expected = start_heuristic - 1 # pulled the nodes of a color closer together
                else:
                    expected = start_heuristic
                # print(node, color)
                actual = color_distance_heuristic(new_state)
                self.assertEqual(actual, expected, msg="Heuristic is incorrect for action (%d, %s)" % (node, color))

    def test_color_distance18(self):
        start_state = puzzle18.start_state()
        start_heuristic = color_distance_heuristic(start_state)
        self.assertEqual(start_heuristic, start_state.num_colors() + 1, msg="Heuristic is incorrect for initial state")

        contracting_moves = {
            3: ['w', 'o', 'c'], # deletes a blue node, the remaining blue nodes are adjacent to 23
            4: ['b'], # merges 2 blue nodes and the resulting blue nodes are adjacent to 23
            5: ['b'], # merges 2 blue nodes and the resulting blue nodes are adjacent to 23

            13: ['b'], # now touching all cyan nodes
            23: ['b'], # now touching all cyan nodes
            24: ['b'], # merges two blue nodes and the remaining three blue nodes form a triangle with length-2 paths connecting (3-4-16-13or23-24-5-3)
            25: ['w', 'o', 'c'], # deletes a blue node and the remaining three blue nodes form a triangle
        }
        for action, new_state, cost in puzzle18.actions_and_costs(start_state):
            with self.subTest(action=action):
                node, color = action
                if node in contracting_moves and color in contracting_moves[node]:
                    expected = start_heuristic - 1 # pulled the nodes of a color closer together
                else:
                    expected = start_heuristic
                # print(node, color)
                actual = color_distance_heuristic(new_state)
                self.assertEqual(actual, expected, msg="Heuristic is incorrect for action (%d, %s)" % (node, color))

if __name__ == '__main__':
    unittest.main()
