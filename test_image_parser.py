import unittest
from test_puzzle18 import puzzle18_graph, puzzle18_node_colors
from image_parser import parse_image_graph
import networkx as nx

class TestImageParser(unittest.TestCase):
    def test_parse_puzzle18(self):
        # call the parser
        puzzle_img = "kami2puzzle18.png"
        print(f"parsing puzzle image: {puzzle_img}")
        parsed_graph, node_colors = parse_image_graph(puzzle_img)

        # convert to dict of lists for isomorphism check
        for node in puzzle18_graph:
            puzzle18_graph[node] = list(puzzle18_graph[node])
        for node in parsed_graph:
            parsed_graph[node] = list(parsed_graph[node])

        # check that the number of nodes is correct
        self.assertEqual(len(puzzle18_graph), len(parsed_graph))

        # check that the edges in the graph are correct (i.e. graphs are isomorphic)
        puzzle18_nxgraph = nx.from_dict_of_lists(puzzle18_graph)
        parsed_nxgraph = nx.from_dict_of_lists(parsed_graph)

        graph_matcher = nx.algorithms.isomorphism.GraphMatcher(puzzle18_nxgraph, parsed_nxgraph)
        self.assertTrue(graph_matcher.is_isomorphic())

        # check that node colors match (all nodes with same color in manual
        # input should have been parsed with the same label/color)
        puzzle18_color_to_nodes = {}
        for node in puzzle18_node_colors:
            node_color = puzzle18_node_colors[node]
            if node_color not in puzzle18_color_to_nodes:
                puzzle18_color_to_nodes[node_color] = []
            puzzle18_color_to_nodes[node_color].append(node)

        for color in puzzle18_color_to_nodes:
            nodes = puzzle18_color_to_nodes[color]
            # need to convert from the node numbering from manually generated graph
            # to the parsed graph node numbering
            parsed_nodes = [graph_matcher.mapping[node] for node in nodes]
            parsed_label = None
            for node in parsed_nodes:
                if parsed_label == None:
                    parsed_label = node_colors[node]
                elif parsed_label != node_colors[node]:
                    self.fail(f"label mismatch for node {node}: {parsed_label} vs {node_colors[node]}")

    # TODO check that the image parser can handle a puzzle screenshot with blank space

if __name__ == '__main__':
    unittest.main()
