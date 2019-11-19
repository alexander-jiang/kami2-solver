import unittest
from test_puzzle18 import puzzle18_graph, puzzle18_node_colors
from image_parser import parse_image_graph
import networkx as nx

class TestImageParser(unittest.TestCase):
    def test_parse_puzzle18(self):
        # call the parser
        puzzle_img = "kami2puzzle18.png"
        print(f"parsing puzzle image: {puzzle_img}")
        parsed_graph = parse_image_graph(puzzle_img)

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

        self.assertTrue(nx.is_isomorphic(puzzle18_nxgraph, parsed_nxgraph))

    # TODO check that the image parser can handle a puzzle screenshot with blank space

if __name__ == '__main__':
    unittest.main()
