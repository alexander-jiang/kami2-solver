import unittest
import itertools
from test_puzzle17 import puzzle17_graph, puzzle17_node_colors
from test_puzzle18 import puzzle18_graph, puzzle18_node_colors
from test_puzzle33 import puzzle33_graph, puzzle33_node_colors
from test_puzzle98 import puzzle98_graph, puzzle98_node_colors
from test_puzzle103 import puzzle103_graph, puzzle103_node_colors
from image_parser import parse_image_graph
import networkx as nx

class TestImageParser(unittest.TestCase):
    # methods not prefixed with "test" will not be run as unit tests
    # this helper
    def puzzle_parse_testing(self, puzzle_img, num_colors, manual_graph, manual_node_colors):
        # call the parser
        print(f"parsing puzzle image: {puzzle_img}")
        parsed_graph, parsed_node_colors = parse_image_graph(puzzle_img, num_colors)
        num_nodes = len(manual_graph.keys())

        # convert to dict of lists for isomorphism check
        for node in manual_graph:
            manual_graph[node] = list(manual_graph[node])
        for node in parsed_graph:
            parsed_graph[node] = list(parsed_graph[node])

        # check that the number of nodes is correct
        self.assertEqual(len(manual_graph), len(parsed_graph),
            "incorrect number of nodes in parsed graph! {len(parsed_graph)} vs {len(manual_graph)} nodes in manual graph")

        # check that the edges in the graph are correct (i.e. graphs are isomorphic)
        manual_nxgraph = nx.from_dict_of_lists(manual_graph)
        parsed_nxgraph = nx.from_dict_of_lists(parsed_graph)

        graph_matcher = nx.algorithms.isomorphism.GraphMatcher(parsed_nxgraph, manual_nxgraph)
        self.assertTrue(graph_matcher.is_isomorphic())

        ## some graphs have non-unique isomorphisms but the pairs of nodes
        ## that are interchangeable in isomorphism may actually be different colors

        # check that node colors match (all nodes with same color in manual
        # input should have been parsed with the same label/color)
        manual_color_to_nodes = {}
        for node in manual_node_colors:
            node_color = manual_node_colors[node]
            if node_color not in manual_color_to_nodes:
                manual_color_to_nodes[node_color] = []
            manual_color_to_nodes[node_color].append(node)

        ## instead of listing manual nodes and then converting to parsed nodes,
        ## use the parsed_node_colors mapping and then see if there is a way to map
        ## the parsed nodes back to the manual nodes
        parsed_color_to_nodes = {}
        for parsed_node in parsed_node_colors:
            this_color = parsed_node_colors[parsed_node]
            if this_color not in parsed_color_to_nodes:
                parsed_color_to_nodes[this_color] = []
            parsed_color_to_nodes[this_color].append(parsed_node)

        # num of nodes for each color
        parsed_color_lengths = [len(parsed_color_to_nodes[color]) for color in parsed_color_to_nodes]
        parsed_color_lengths.sort()

        manual_color_lengths = [len(manual_color_to_nodes[color]) for color in manual_color_to_nodes]
        manual_color_lengths.sort()

        # print(f"number of parsed nodes of each color (sorted) = {parsed_color_lengths}")
        # print(f"number of manual nodes of each color (sorted) = {manual_color_lengths}")
        self.assertEqual(parsed_color_lengths, manual_color_lengths,
            "list of number of nodes for each color doesn't match between manual {manual_color_lengths} and parsed {parsed_color_lengths}")

        # construct all possible mappings from parsed color to manual color given the color lengths (i.e. how many nodes of each color)
        parsed_to_manual_color_mappings = []

        color_len_permutations = {} # each entry here is a list of possible mappings for each color length
        for color_len in manual_color_lengths:
            candidate_parsed_colors = []
            for color in parsed_color_to_nodes:
                if len(parsed_color_to_nodes[color]) == color_len:
                    candidate_parsed_colors.append(color)

            candidate_manual_colors = []
            for color in manual_color_to_nodes:
                if len(manual_color_to_nodes[color]) == color_len:
                    candidate_manual_colors.append(color)

            self.assertEqual(len(candidate_manual_colors), len(candidate_parsed_colors),
                f"should be an equal number of colors that have {color_len} nodes in manual graph vs. parsed graph!")

            # hold the candidate_parsed_colors constant, but try all permutations
            # of the candidate_manual_colors
            color_len_permutations[color_len] = []
            for manual_color_permutations in itertools.permutations(candidate_manual_colors):
                partial_color_mapping = {}
                for color_idx in range(len(candidate_manual_colors)):
                    parsed_color = candidate_parsed_colors[color_idx]
                    manual_color = manual_color_permutations[color_idx]
                    partial_color_mapping[parsed_color] = manual_color
                color_len_permutations[color_len].append(partial_color_mapping)

        for color_len in color_len_permutations:
            parsed_to_manual_mapping_copy = []
            if len(parsed_to_manual_color_mappings) == 0:
                for partial_map in color_len_permutations[color_len]:
                    parsed_to_manual_mapping_copy.append(partial_map)
            else:
                for previous_mapping in parsed_to_manual_color_mappings:
                    for partial_map in color_len_permutations[color_len]:
                        merged_mapping = {}
                        merged_mapping.update(previous_mapping)
                        merged_mapping.update(partial_map)
                        parsed_to_manual_mapping_copy.append(merged_mapping)
            parsed_to_manual_color_mappings = parsed_to_manual_mapping_copy

        # validate every mapping
        # print(f"color_len_permutations = {color_len_permutations}")
        for mapping in parsed_to_manual_color_mappings:
            self.assertEqual(num_colors, len(mapping.keys()),
                f"parsed->manual color mapping {mapping} has incorrect number of parsed colors!")
            self.assertEqual(num_colors, len(set(mapping.values())),
                f"parsed->manual color mapping {mapping} has incorrect number of manual colors!")
            # print(f"parsed->manual color mapping {mapping}")

        expected_num_mappings = 1
        for color_len in color_len_permutations:
            expected_num_mappings *= len(color_len_permutations[color_len])
        self.assertEqual(expected_num_mappings, len(parsed_to_manual_color_mappings),
            f"expected {expected_num_mappings} color mappings but instead found {len(parsed_to_manual_color_mappings)} color mappings")

        # for every color mapping, check if the isomorphism mapping maps a parsed node
        # to a "wrong-colored" manual node: they might be interchangeable in the isomorphism mapping
        good_mapping_found = False
        for mapping in parsed_to_manual_color_mappings:
            # note which parsed nodes map to a "wrong-olored" manual node
            # and which manual node swaps are feasible in isomorphism mapping
            parsed_needing_swap = []
            manual_swaps = []
            # print(f"checking parsed->manual color mapping {mapping}")

            for parsed_color in mapping:
                manual_color = mapping[parsed_color]
                # print(f"checking parsed color {parsed_color} -> manual color {manual_color}")

                for parsed_node in parsed_color_to_nodes[parsed_color]:
                    matched_manual = graph_matcher.mapping[parsed_node]
                    if matched_manual in manual_color_to_nodes[manual_color]:
                        continue # maps to a node of the "right" color (given this permutation)

                    parsed_needing_swap.append(parsed_node)
                    manual_nbrs = manual_graph[matched_manual]
                    swap_candidates = []
                    for node in manual_graph:
                        if (manual_graph[node] == manual_nbrs and
                            manual_node_colors[node] == manual_color and
                            node != matched_manual):
                                swap_candidates.append(node)
                    # print(f"parsed node {parsed_node} mapped to wrong-color ({manual_node_colors[matched_manual]}) manual node {matched_manual}")
                    # print(f"isomorphism swap candidates => {swap_candidates}")

                    for candidate in swap_candidates:
                        # try changing the isomorphism mapping to satisfy this swap
                        feasible_swap = graph_matcher.semantic_feasibility(parsed_node, candidate)
                        if feasible_swap:
                            # print(f"can swap parsed {parsed_node} to map to manual {candidate}")
                            manual_swaps.append((matched_manual, candidate))
            # print(f"manual_swaps = {manual_swaps}")

            ## look for a cycle in the graph from manual_swaps
            if len(parsed_needing_swap) > 0:
                manual_nodes_to_be_swapped = [graph_matcher.mapping[parsed_node] for parsed_node in parsed_needing_swap]
                swap_digraph = nx.DiGraph()
                for edge in manual_swaps:
                    swap_digraph.add_edge(edge[0], edge[1])
                # print(f"swap_digraph edges = {swap_digraph.edges}")

                cycle_generator = nx.simple_cycles(swap_digraph)
                ## check if a cycle covers all parsed nodes that need to be swapped.
                ## if so, the isomorphism mapping can be resolved. if not, the parsed graph was incorrect
                found_good_cycle = False
                for cycle in cycle_generator:
                    # print(f"checking manual nodes cycle {cycle}")
                    if len(cycle) < len(parsed_needing_swap):
                        continue # cycle is too short
                    if len(set(manual_nodes_to_be_swapped) | set(cycle)) == len(parsed_needing_swap):
                        # print(f"found manual swap cycle: {cycle}")
                        graph_matcher_mapping_copy = graph_matcher.mapping.copy()
                        for parsed_node in parsed_needing_swap:
                            current_manual = graph_matcher.mapping[parsed_node]
                            cycle_idx = cycle.index(current_manual)
                            new_idx = (cycle_idx + 1) % len(cycle)
                            # print(f"parsed node {parsed_node} should map to manual node {cycle[new_idx]}")
                            graph_matcher_mapping_copy[parsed_node] = cycle[new_idx]
                        print(f"new parsed->manual node mapping = {graph_matcher_mapping_copy})")
                        self.assertEqual(num_nodes, len(graph_matcher_mapping_copy.keys()),
                            f"new mapping should have {num_nodes} parsed nodes")
                        self.assertEqual(num_nodes, len(set(graph_matcher_mapping_copy.values())),
                            f"new mapping should have {num_nodes} manual nodes")
                        found_good_cycle = True
                        break
                if not found_good_cycle:
                    # print(f"failed to find a good cycle")
                    continue
                else:
                    good_mapping_found = True
                    break
            else:
                ## if no swaps were needed, then this mapping is correct
                ## no need to check other possible mappings
                good_mapping_found = True
                break

        self.assertTrue(good_mapping_found,
            "Failed to find a parsed->manual color mapping that would satisfy isomorphism and node coloring!")


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

    def test_parse_puzzle98(self):
        puzzle_img = "kami2puzzle98.png"
        puzzle98_num_colors = 5
        self.puzzle_parse_testing(puzzle_img, puzzle98_num_colors, puzzle98_graph, puzzle98_node_colors)

    def test_parse_puzzle103(self):
        puzzle_img = "kami2puzzle103.png"
        puzzle103_num_colors = 3
        self.puzzle_parse_testing(puzzle_img, puzzle103_num_colors, puzzle103_graph, puzzle103_node_colors)

    # TODO check that the image parser can handle a puzzle screenshot with blank space

if __name__ == '__main__':
    unittest.main()
