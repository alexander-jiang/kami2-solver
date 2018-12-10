# kami2
Solver for the mobile puzzle game KAMI 2

### Notes:

#### 12/10/2018
Implemented DFS, UCS, and A* with two different heuristics.

It seems that DFS performs better than UCS and A*, but this is likely
because of how I defined the "terminal states".

For example, if you have 2 moves left but there are 4 or more colors on the
board, it is impossible to solve the puzzle (since each move can reduce the
number of colors on the board by at most 1). Thus these states are "terminal",
which forces the DFS to backtrack earlier, and it may get lucky (I've randomly
shuffled the list of possible subsequent states). If I didn't stop the DFS early
in these failing states, it would likely perform far worse than UCS or A*.

(Note that this fail-early system works best when the number of colors in the
puzzle is close to the number of moves you have to solve the puzzle e.g. in
puzzle #17, you have 4 moves to solve a puzzle with 4 colors, so any first move
that doesn't lead to a state where you can eliminate a color with one move is
backed out of immediately after visiting it. Similarly, the 3rd and 4th moves
must also each eliminate one color, so "poor" moves can be quickly discarded.)

On the other hand, the UCS and A* algorithms will enumerate all neighbors, and
since the distance function is very coarse (every action has step cost 1, and
even with the heuristics, there are often ties), these algorithms end up looking
like BFS since they often visit every neighbor.

I haven't yet tried the algorithms on a puzzle where there are significantly
more moves than colors (e.g. puzzle #89), though I anticipate that these puzzles
would get exponentially harder for DFS.

Next, I think I should implement a metric for determining which nodes to try
first in DFS. For example, a simple measure would be to try to color nodes with
the highest degree, as these are most likely to pull the graph closer together,
but more sophisticated measures of centrality could identify "key nodes" in the
graph that connect many different colors together, making it easier to contract
the colors in sequence.

For a concrete example, see nodes 9 & 12 in puzzle #17, which are both connected
to the only white nodes, and then the contracted group with 5 and 10 is
connected to all blue nodes, etc. Note that in this case, nodes 9 and 12 don't
have the highest degree, but nodes 5 and 10 both have very high degrees, and so
coloring 9 or 12 with white creates a contracted group with very high degree
(and more importantly, with minimal distance to the remaining colors).
