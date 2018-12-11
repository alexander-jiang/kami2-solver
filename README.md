# kami2
Solver for the mobile puzzle game KAMI 2

### Notes:

#### 12/10/2018
I've implemented DFS, UCS, and A* with two different heuristics.

The A* with num_colors_heuristic function now performs better than DFS on puzzle
18 (see the bugfix below), but worse than DFS on puzzle 17. This is likely
because puzzle 17 is a 4 move, 4 color puzzle, so DFS will only need to
enumerate all of the first move options before being forced to either eliminate
a color or backtrack due to the "failing" terminal states in the state space
(where there aren't enough moves to possibly solve the puzzle). However, puzzle
18 is a 5 move, 4 color puzzle, so DFS will have to try the possible
combinations of the first two moves before getting feedback on whether it has
reached an "impossible to solve" state.

I fixed a bug in the num_colors_heuristic function which wasn't counting
colors that were already contracted to a single node towards reducing the
heuristic estimate (which would explain why the A* was exploring almost the
exact same number of states as UCS did: they were almost the same algorithm).

Next, I think I should implement a heuristic that captures the "centrality" of
certain nodes. For example, a simple measure would be to try to color nodes with
the highest degree, as these are most likely to pull the graph closer together,
but more sophisticated measures of centrality could identify "key nodes" in the
graph that connect many different colors together, making it easier to contract
the colors in sequence.

For a concrete example, see nodes 9 & 12 in puzzle 17, which are both connected
to the only white nodes, and then the contracted group with 5 and 10 is
connected to all blue nodes, etc. Note that in this case, nodes 9 and 12 don't
have the highest degree, but nodes 5 and 10 both have very high degrees, and so
coloring 9 or 12 with white creates a contracted group with very high degree
(and more importantly, with minimal distance to the remaining colors).
