import copy
import random
import itertools

class Kami2Puzzle:
    def __init__(self, initial_state):
        """
        Creates a puzzle based on the initial state of the puzzle.
        """
        self.initial_state = initial_state
        self.solution = None
        self.num_states_explored = None

    def start_state(self):
        """
        Returns the initial state of the puzzle.
        """
        return self.initial_state

    def actions_and_costs(self, state):
        """
        Returns a list of all possible actions from the given state
        (in arbitrary order), the resulting states from those actions,
        and the cost of the actions, represented as tuples of
        (action, next_state, cost), where action is a tuple (node, next_color).
        """
        nodes = state.nodes()
        # Note: in the game, you're allowed to set a node to one of the starting
        # colors even if that color has been removed from the graph, but doing
        # that is never part of an optimal solution
        colors = state.colors
        results = []
        for node in nodes:
            for new_color in colors:
                if new_color == state.get_color(node):
                    continue
                # print("setting node %d to color %s" % (node, new_color))
                new_state = state.set_color(node, new_color)
                cost = 1
                results.append(((node, new_color), new_state, cost))
        # random.shuffle(results)
        return results

    def is_terminal_state(self, state):
        """
        Returns 1 if the given state is a goal state (i.e. all nodes are the
        same color and number of moves remaining is >= 0), returns -1 if given
        state cannot lead to a solution (e.g. number of moves remaining < 0,
        other early termination conditions, etc.), and returns 0 otherwise.
        """
        if state.moves_left >= 0 and state.num_colors() == 1:
            return 1
        elif state.moves_left < 0 or state.num_colors() > state.moves_left + 1:
            return -1
        else:
            return 0

class PuzzleState:
    def __init__(self, graph, node_colors, moves_left):
        """
        Creates a new graph based on an undirected graph and a mapping from
        node IDs to colors (provided as a list of distinct strings).

        Properties:
        self.graph - dict from node to frozensets of nodes, the undirected graph
        self.colors - set of strings, the colors in the graph state
        self.node_colors - dict from node to string, the colors of each node
        self.moves_left - int, the number of moves left to solve the puzzle
        self.max_dist_for_color - dict, mapping color to the maximum distance
        between any two nodes of that color in the graph
        (see get_max_dist_for_color function below)
        """
        self._validate_init(graph, node_colors, moves_left)

        self.graph = graph
        self.colors = set(node_colors.values())
        self.node_colors = node_colors
        self.moves_left = moves_left

        self.heuristic_val = None
        self.max_dist_for_color = None

    def _validate_init(self, graph, node_colors, moves_left):
        """
        Validates the inputs to the constructor.
        """
        # Type validation
        for node in graph:
            assert isinstance(node, int), "Nodes are integers!"
            assert isinstance(graph[node], frozenset), "Neighbors of %d isn't a frozenset of nodes!" % (node,)
        assert isinstance(moves_left, int), "Moves left is an integer!"
        assert moves_left >= 0, "Moves left shouldn't be negative!"
        # Check that the graph and node_colors have the same keys
        assert set(graph.keys()) == set(node_colors.keys())
        # Graph edge validation: make sure for every edge A -> B there is B -> A
        for node in graph:
            for nbr in graph[node]:
                assert nbr != node, "Graph validation failed: self-loop exists on node %d" % (node,)
                assert node in graph[nbr], "Graph validation failed: missing %d -> %d" % (nbr, node)
                assert node_colors[node] != node_colors[nbr], "%d and %d have the same color %s" % (node, nbr, node_colors[node])

    def __hash__(self):
        return hash((
            self.moves_left,
            frozenset(self.node_colors.items()),
            frozenset(self.graph.items()),
        ))

    def __eq__(self, other):
        """
        Compares states for equality.
        """
        return (self.moves_left == other.moves_left and
            self.node_colors == other.node_colors and
            self.graph.keys() == other.graph.keys() and
            self.graph == other.graph)

    def __neq__(self, other):
        return not self.__eq__(other)

    def nodes(self):
        """
        Returns a list of all nodes in the graph, in no particular order.
        """
        return self.graph.keys()

    def num_colors(self):
        """
        Returns the number of colors in the graph.
        """
        return len(self.colors)

    def get_color(self, node):
        """
        Gets the color of a node.
        """
        return self.node_colors[node]

    def set_color(self, node, new_color):
        """
        Returns a new state with the node set to the new color, and with the
        graph contracted (if necessary).
        """
        if self.get_color(node) == new_color:
            return self

        new_graph = copy.deepcopy(self.graph)
        new_node_colors = copy.deepcopy(self.node_colors)

        # Combine node with same-colored neighbors
        new_neighbors = set([])
        for neighbor in self.graph[node]:
            if self.get_color(neighbor) == new_color:
                new_neighbors |= (self.graph[neighbor] - set([node,]))
                # replace the reference to neighbor with reference to new node
                for next_nbr in self.graph[neighbor]:
                    if next_nbr == node: continue
                    new_next_nbrs = set(new_graph[next_nbr])
                    new_next_nbrs.remove(neighbor)
                    new_next_nbrs.add(node)
                    new_graph[next_nbr] = frozenset(new_next_nbrs)
                    # new_graph[next_nbr] ^= set([neighbor, node])
                del new_graph[neighbor]
                del new_node_colors[neighbor]
            else:
                new_neighbors.add(neighbor)

        new_graph[node] = frozenset(new_neighbors)
        new_node_colors[node] = new_color

        return PuzzleState(new_graph, new_node_colors, self.moves_left - 1)

    ## TODO this assumes the heuristic function doesn't change across calls to update_heuristic_value()
    def update_heuristic_value(self, heuristic_func):
        if self.heuristic_val is None:
            self.heuristic_val = heuristic_func(self)
            # print(f"saving heuristic value: {self.heuristic_val} for state {hash(self)}")
        # else:
        #     print(f"using memoized heuristic value: {self.heuristic_val} for state {hash(self)}")
        return self.heuristic_val

    def get_max_dist_for_color(self):
        """
        Returns a mapping from node color to the maximum distance between any
        two nodes of that color in the graph (memoized).
        """
        def brandes(graph):
            """
            Since graph is unweighted and undirected, use BFS to compute
            pairwise distances (Brandes' algorithm computes more centrality
            measures, which we may not need).
            """
            dist = {}
            for node_s in graph:
                # stack = []
                # pred = {}
                # num_shortest_paths = {}
                dist[node_s] = {}
                for node in graph:
                    # pred[node] = []
                    dist[node_s][node] = -1
                    # num_shortest_paths[node] = 0
                # num_shortest_paths[node_s] = 1
                dist[node_s][node_s] = 0

                queue = []
                queue.append(node_s)
                while len(queue) > 0:
                    node_v = queue.pop(0)
                    # stack.append(node_v)
                    for nbr in graph[node_v]:
                        # was this neighbor found before?
                        if dist[node_s][nbr] < 0:
                            queue.append(nbr)
                            dist[node_s][nbr] = dist[node_s][node_v] + 1
                        # is shortest path to nbr via node_v?
                        # if dist[node_s][nbr] == dist[node_s][node_v] + 1:
                        #     num_shortest_paths[nbr] += num_shortest_paths[node_v]
                        #     pred[nbr].append(node_v)
            return dist

        if self.max_dist_for_color is None:
            self.max_dist_for_color = {}
            pairwise_distances = brandes(self.graph)
            for color in self.colors:
                max_dist_for_color = -float('inf')
                color_nodes = []
                for node in self.graph:
                    if self.get_color(node) == color:
                        color_nodes.append(node)

                for (node1, node2) in itertools.combinations(color_nodes, 2):
                    distance = pairwise_distances[node1][node2]
                    if distance > max_dist_for_color:
                        max_dist_for_color = distance
                self.max_dist_for_color[color] = max_dist_for_color

        return self.max_dist_for_color
