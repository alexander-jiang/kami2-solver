# kami2
Solver for the mobile puzzle game KAMI 2

## To-do:
- WIP: build an image parser that constructs the graph of the puzzle state (i.e.
the different contiguous regions and the adjacencies between those regions) from
a screenshot of the puzzle
- TODO: switch to using a graph module like networkx or graph-tools (the latter
is better-performing but trickier to install on my Windows machine)
- TODO: read up on centrality measures in graph theory (e.g. betweenness
centrality) and algorithms for computing those measures (e.g. Brandes' algorithm
for betweenness centrality)


## Notes:

### 12/08/2019
Some improvements to the solver algorithm:
- update the priority queue tiebreaking to choose states with fewer moves left first,
and then break ties by LIFO (instead of FIFO, which was how it was originally implemented).
This keeps expanding the frontier at states that are close to the goal and instead of
backtracking to an earlier state.
- Include heuristic function when checking if the state is a terminal state

The image parser seems to work consistently well on puzzles without whitespace (i.e.
where all tiles are one of the colors in the palette). The whitespace/background in
puzzles is difficult to parse because it has a pretty significant gradient, making
preprocessing less effective, and causing the whitespace/background to sometimes
be parsed as one or two colors, depending on which parts of the background are visible.

The image parser uses K-means to distinguish the colors in the puzzle from each other
(for now, the number of colors must be manually fed into the parser, but it could be
possible to do edge detection on the color palette at the bottom of the screen), with
some pre-processing (bilateral filter to smooth out the paper-like texture within each
contiguous region while preserving edges) and post-processing (morphological operations
to avoid marking two same-colored regions that touch at a vertex as contiguous and to
remove noise from the k-means step).

### 10/19/2019
Using bilateral filter as preprocessing (to smooth out small differences in color
from the paper-like texture of the game but leave edges between contiguous regions
of the same color in the puzzle intact) and then K-means (where K is set to the
number of colors in the puzzle) seems to work pretty well.

I think it's okay if I have to manually input the number of colors that the puzzle
has and the number of moves remaining in addition to providing the screenshot: it
is possible to automatically parse these given the image, but it probably won't
save that much time (most of the time I spent when turning a puzzle into a puzzle
state that my solver could operate on was spent on carefully labeling contiguous
regions and which were adjacent).

### 10/16/2019
Cleaned up the style of the repo (e.g. more consistency between snake_case and
camelCase), from the initial commit onwards.

### 12/11/2018
Fixed a bug with the color distance function and improved its performance:
- Floyd-Warshall algorithm is overkill: since the graph is unweighted and
undirected, a simple BFS will produce the pairwise distances.
- I forgot to account for the case when a color has already been contracted down
to one node (in which case, it takes no moves to contract a color to a single
node)

The color distance heuristic function tries to compute a tighter lower bound on
how many moves it would take to contract any color down to one node. (The num
colors heuristic assumed that any color could be contracted down to one node in
one move.) The color distance heuristic first computes the pairwise distance
between all nodes of one color and then takes the maximum of these distances,
divides that distance by two and rounds up (since the optimistic estimate is
that those two same-color nodes can be joined along the shortest path by merging
from the middle). This is the estimate of how many moves it would take to
contract that color into one node. It repeats this for all colors and takes the
minimum of these estimates and adds this number to (# colors) - 1, as in the
num colors heuristic (as it optimistically assumes that the other colors can
be contracted into a single node in one move per color after the first color
is contracted into a single node).

The color distance heuristic function matches the performance of the
num_color_heuristic function on puzzle 17 (both explore 36 states), and
explores about half as many states as the num color heuristic function in
puzzle 18 (64 vs. 131).

The new heuristic function now makes puzzle 54 tractable (solved and explored
952 states) and shows a huge improvement in solving puzzle 71 (explored only 281
states vs. 6242 states explored by num colors heuristic). Puzzle 72 is similar
to puzzle 71 (slightly harder), and the color distance heuristic solved it and
explored only 26 states!

### 12/10/2018
I've implemented DFS, UCS, and A* with the num_color_heuristic heuristic
function (see deterministic_search.py and informed_search.py for the search
algorithms and heuristic functions).

I fixed a bug in the num_colors_heuristic function which wasn't counting
colors that were already contracted to a single node towards reducing the
heuristic estimate (which would explain why the A* was exploring almost the
exact same number of states as UCS did: they were almost the same algorithm).

The A* with num_colors_heuristic function now performs better than DFS on puzzle
18 (see the bugfix below), but worse than DFS on puzzle 17. This is likely
because puzzle 17 is a 4 move, 4 color puzzle, so DFS will only need to
enumerate all of the first move options before being forced to either eliminate
a color or backtrack due to the "failing" terminal states in the state space
(where there aren't enough moves to possibly solve the puzzle). However, puzzle
18 is a 5 move, 4 color puzzle, so DFS will have to try the possible
combinations of the first two moves before getting feedback on whether it has
reached an "impossible to solve" state.

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
