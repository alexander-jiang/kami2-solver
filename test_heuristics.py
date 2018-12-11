import unittest

from informed_search import num_colors_heuristic
from test_puzzle17 import puzzle17

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
                self.assertEqual(num_colors_heuristic(new_state), expected, msg="Heuristic is incorrect for action (%d, %s)" % (node, color))

if __name__ == '__main__':
    unittest.main()
