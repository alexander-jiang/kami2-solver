import unittest
from test_puzzle17 import puzzle17_graph, puzzle17_node_colors
from test_puzzle18 import puzzle18_graph, puzzle18_node_colors
from test_puzzle33 import puzzle33_graph, puzzle33_node_colors
from image_parser import parse_image_graph
import networkx as nx

class TestImageParser(unittest.TestCase):
    # methods not prefixed with "test" will not be run as unit tests
    # this helper
    def puzzle_parse_testing(self, puzzle_img, num_colors, manual_graph, manual_node_colors):
        # call the parser
        print(f"parsing puzzle image: {puzzle_img}")
        parsed_graph, node_colors = parse_image_graph(puzzle_img, num_colors)

        # convert to dict of lists for isomorphism check
        for node in manual_graph:
            manual_graph[node] = list(manual_graph[node])
        for node in parsed_graph:
            parsed_graph[node] = list(parsed_graph[node])

        # check that the number of nodes is correct
        self.assertEqual(len(manual_graph), len(parsed_graph), "incorrect number of nodes in parsed graph! {len(parsed_graph)} vs {len(manual_graph)} nodes in manual graph")

        # check that the edges in the graph are correct (i.e. graphs are isomorphic)
        manual_nxgraph = nx.from_dict_of_lists(manual_graph)
        parsed_nxgraph = nx.from_dict_of_lists(parsed_graph)

        graph_matcher = nx.algorithms.isomorphism.GraphMatcher(manual_nxgraph, parsed_nxgraph)
        self.assertTrue(graph_matcher.is_isomorphic())

        # check that node colors match (all nodes with same color in manual
        # input should have been parsed with the same label/color)
        manual_color_to_nodes = {}
        for node in manual_node_colors:
            node_color = manual_node_colors[node]
            if node_color not in manual_color_to_nodes:
                manual_color_to_nodes[node_color] = []
            manual_color_to_nodes[node_color].append(node)

        for color in manual_color_to_nodes:
            nodes = manual_color_to_nodes[color]
            # need to convert from the node numbering from manually generated graph
            # to the parsed graph node numbering
            parsed_nodes = [graph_matcher.mapping[node] for node in nodes]
            parsed_label = None
            for node in parsed_nodes:
                if parsed_label == None:
                    parsed_label = node_colors[node]
                elif parsed_label != node_colors[node]:
                    self.fail(f"label mismatch for node {node}: {parsed_label} vs {node_colors[node]}")

    def test_parse_puzzle17(self):
        puzzle_img = "kami2puzzle17.png"
        puzzle17_num_colors = 4
        self.puzzle_parse_testing(puzzle_img, puzzle17_num_colors, puzzle17_graph, puzzle17_node_colors)

    def test_parse_puzzle18(self):
        puzzle_img = "kami2puzzle18.png"
        puzzle18_num_colors = 4
        self.puzzle_parse_testing(puzzle_img, puzzle18_num_colors, puzzle18_graph, puzzle18_node_colors)

    def test_parse_puzzle33(self):
        puzzle_img = "kami2puzzle33.png"
        puzzle33_num_colors = 3
        self.puzzle_parse_testing(puzzle_img, puzzle33_num_colors, puzzle33_graph, puzzle33_node_colors)

    # TODO check that the image parser can handle a puzzle screenshot with blank space

if __name__ == '__main__':
    unittest.main()
