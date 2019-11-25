import argparse
import collections
import copy
import itertools
import json
import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt

# TODO I know this is hardcoded, but the screenshots should always be the same resolution (750x1334), right?
puzzle_height_y = 1210
puzzle_width_x = 750

def get_original_image(filename):
    return cv2.imread(filename, cv2.IMREAD_COLOR)

def image_preprocessing(img):
    bilateral_d = 5
    bilateral_sigma = 100
    bilateral_filtered_img = cv2.bilateralFilter(img, bilateral_d, bilateral_sigma, bilateral_sigma)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax1.set_title("original image")

    ax2.imshow(cv2.cvtColor(bilateral_filtered_img, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"bilateral filter (d={bilateral_d}, sigma={bilateral_sigma})")
    # plt.show()
    return bilateral_filtered_img

def crop_to_puzzle(full_screenshot_img):
    puzzle = copy.deepcopy(full_screenshot_img)
    return puzzle[0:puzzle_height_y, 0:puzzle_width_x]

def crop_to_color_palette(full_screenshot_img):
    img_copy = copy.deepcopy(full_screenshot_img)

    # top left corner of the color palette in the image (i.e. the node colors)
    start_y = puzzle_height_y
    start_x = 300
    height_y = 124
    width_x = 450
    return img_copy[0:puzzle_height_y, 0:puzzle_width_x]

def convert_to_kmeans_colors(labels, centers):
    flatten_labels = np.ravel(labels)
    # print("flattened labels:")
    # print(flatten_labels[0:5])

    # convert colors in puzzle to the k-means colors
    converted_pixels = [[round(centers[i,0]), round(centers[i,1]), round(centers[i,2])] for i in flatten_labels]
    converted_puzzle = np.reshape(converted_pixels, (puzzle_height_y, puzzle_width_x, 3))
    return np.asarray(converted_puzzle, dtype=np.uint16)

def assign_pixels_to_nodes(pixel_labels, num_labels):
    # parse contiguous regions (i.e. nodes) from converted colors
    pixel_nodes = np.zeros((puzzle_height_y, puzzle_width_x))
    next_node_number = 1

    masks_by_label = np.zeros((num_labels, pixel_labels.shape[0], pixel_labels.shape[1]))

    erosion_kernel = np.ones((3, 3), dtype=np.uint8)
    dilation_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    pixel_labels_ndarray = np.array(pixel_labels)

    for label_num in range(num_labels):
        # construct binary bitmask of the pixel_labels (1 for each pixel of that label, 0 otherwise)
        masks_by_label[label_num] = np.where(pixel_labels_ndarray == label_num, 1, 0)

        # erode by 3x3 square kernel, and then dilate by a 3x3 cross kernel to leave
        # a thin strip of pixels between neighboring regions
        erosion = cv2.erode(masks_by_label[label_num], erosion_kernel, iterations=1)
        dilation = cv2.dilate(erosion, dilation_kernel, iterations=1)

        # fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        # ax1.imshow(masks_by_label[label_num], cmap='gray')
        # ax1.set_title(f"initial mask for label {label_num}")
        #
        # ax2.imshow(erosion, cmap='gray')
        # ax2.set_title(f"label {label_num} mask after erosion")
        #
        # ax3.imshow(dilation, cmap='gray')
        # ax3.set_title(f"label {label_num} mask after erosion & dilation")
        # plt.show()

        # label each contiguous region in the resulting mask as a separate node
        for pixel_y in range(puzzle_height_y):
            for pixel_x in range(puzzle_width_x):
                # if pixel is not in the dilated mask or is already labeled, skip it
                if dilation[pixel_y, pixel_x] == 0 or pixel_nodes[pixel_y, pixel_x] > 0:
                    continue

                print(f"new node {next_node_number}: starting with pixel (y={pixel_y}, x={pixel_x})")
                pixel_nodes[pixel_y, pixel_x] = next_node_number
                next_node_number += 1

                neighbor_coords = get_neighbor_coords(pixel_y, pixel_x)
                # recursively assign the same node number to all contiguous pixels that are also in the dilation mask
                while len(neighbor_coords) > 0:
                    nbr_y, nbr_x = neighbor_coords.pop(0)
                    if pixel_nodes[nbr_y, nbr_x] == 0 and dilation[nbr_y, nbr_x] == 1:
                        pixel_nodes[nbr_y, nbr_x] = pixel_nodes[pixel_y, pixel_x]
                        neighbor_coords.extend(get_neighbor_coords(nbr_y, nbr_x))

    before_fill_in = pixel_nodes.copy()

    # fill in pixels that weren't part of any mask (the pixels along the borders)
    any_updates = True
    while any_updates:
        tmp_pixel_nodes = pixel_nodes.copy()
        any_updates = False
        for pixel_y in range(puzzle_height_y):
            for pixel_x in range(puzzle_width_x):
                # if pixel is already labeled, skip it
                if tmp_pixel_nodes[pixel_y, pixel_x] > 0:
                    continue

                neighbor_coords = get_neighbor_coords(pixel_y, pixel_x)
                # if the labels on neighbors are all the same, use that label
                nbr_labels = []
                should_update = False # update only if all labeled neighbors share the same label
                for nbr_y, nbr_x in neighbor_coords:
                    if pixel_nodes[nbr_y, nbr_x] != 0:
                        nbr_labels.append(pixel_nodes[nbr_y, nbr_x])

                should_update = True if len(nbr_labels) > 0 else False
                for nbr_label in nbr_labels:
                    if nbr_label != nbr_labels[0]:
                        should_update = False
                if should_update:
                    tmp_pixel_nodes[pixel_y, pixel_x] = nbr_labels[0]
                    # print(f"updated {(pixel_y, pixel_x)} to label {nbr_labels[0]}")
                    any_updates = True
        pixel_nodes = tmp_pixel_nodes.copy()

    fig, (ax1, ax2) = plt.subplots(1, 2)
    c1 = ax1.pcolormesh(before_fill_in, cmap='jet')
    ax1.invert_yaxis()
    ax1.set_title("node groupings")
    fig.colorbar(c1, ax=ax1)

    c2 = ax2.pcolormesh(pixel_nodes, cmap='jet')
    ax2.invert_yaxis()
    ax2.set_title("grouping after fill-in")
    fig.colorbar(c2, ax=ax2)

    return (pixel_nodes, next_node_number - 1)

def label_pixels_by_node(preprocessed_img, num_colors, debug_print=False):
    puzzle = crop_to_puzzle(preprocessed_img)
    # print(puzzle.shape) # y by x by color
    # print(puzzle[0,0:5,:])

    # Use K-means to reduce number of colors
    pixel_colors = copy.deepcopy(puzzle)
    pixel_colors = np.reshape(pixel_colors, (puzzle.shape[0] * puzzle.shape[1], puzzle.shape[2]))
    pixel_colors = np.asarray(pixel_colors, dtype=np.float32)
    # print(pixel_colors.shape)
    # print(pixel_colors[0:5])

    # configure kmeans
    K = num_colors # if you set K to equal the number of colors that are actually used in the puzzle, this should be very effective
    max_iters = 100
    epsilon = 1.0
    termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iters, epsilon)
    flags = cv2.KMEANS_RANDOM_CENTERS
    random_restarts = 10

    if debug_print:
        print(f"starting K means: max {max_iters} iterations, {random_restarts} random restarts")
    compactness, labels, centers = cv2.kmeans(pixel_colors, K, None, termination_criteria, random_restarts, flags)
    if debug_print:
        print("K means complete!")
        # print("compactness =", compactness)
        print("centers =", centers)

    # extract the color palette
    palette = crop_to_color_palette(preprocessed_img)

    # compare the k-means colors to the color palette
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # centers_rgb = [(center[2] / 255.0, center[1] / 255.0, center[0] / 255.0) for center in centers]
    # bounds = np.arange(K+1)
    # cmap = matplotlib.colors.ListedColormap(centers_rgb)
    # norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    # cb2 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')
    # ax1.set_title(f"k means colors (k = {K})")
    #
    # ax2.imshow(cv2.cvtColor(palette, cv2.COLOR_BGR2RGB))
    # ax2.axis('off')
    # ax2.set_title("color palette from original image")
    # plt.show()

    converted_puzzle = convert_to_kmeans_colors(labels, centers)
    # print(converted_puzzle.shape)
    # print(converted_puzzle[0,0:5,:])

    # compare the original puzzle to the k-means compressed version
    fig2, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB))
    ax1.set_title("original image")
    ax1.axis('off')

    ax2.imshow(cv2.cvtColor(converted_puzzle, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"converted image ({K} colors)")
    ax2.axis('off')
    # plt.show()

    # parse contiguous regions (i.e. nodes) from converted colors
    num_labels = len(centers)
    flatten_labels = np.ravel(labels)
    pixel_labels = np.reshape(flatten_labels, (puzzle_height_y, puzzle_width_x))
    pixel_nodes, num_nodes = assign_pixels_to_nodes(pixel_labels, num_labels)

    # assign colors to each node
    node_colors = {}
    for i in range(pixel_nodes.shape[0]):
        for j in range(pixel_nodes.shape[1]):
            if pixel_nodes[i,j] not in node_colors:
                node_colors[pixel_nodes[i,j]] = pixel_labels[i,j]
            # elif node_colors[pixel_nodes[i,j]] != pixel_labels[i,j]:
            #     print(f"node {pixel_nodes[i,j]} has different K-means labels! {node_colors[pixel_nodes[i,j]]} vs {pixel_labels[i,j]}")
    return (pixel_nodes, node_colors, num_nodes)

# gets a list of neighboring pixel coordinates (y, x)
def get_neighbor_coords(pixel_y, pixel_x):
    neighbor_coords = []
    if pixel_y > 0:
        neighbor_coords.append((pixel_y - 1, pixel_x))
    if pixel_y < puzzle_height_y - 1:
        neighbor_coords.append((pixel_y + 1, pixel_x))
    if pixel_x > 0:
        neighbor_coords.append((pixel_y, pixel_x - 1))
    if pixel_x < puzzle_width_x - 1:
        neighbor_coords.append((pixel_y, pixel_x + 1))
    return neighbor_coords

def identify_adjacent_nodes(pixel_nodes, num_nodes, debug_print=False):
    puzzle_graph = {}
    counts = {}
    for i in range(1, num_nodes + 1):
        puzzle_graph[i] = set([])
        counts[i] = collections.Counter()

    ## TODO also have to consider that there are some pixels labeled with 0
    ## i.e. not assigned to a node yet because they are neighboring to more than
    ## one region. These nodes can still be used to mark dependencies

    for i in range(pixel_nodes.shape[0]):
        for j in range(pixel_nodes.shape[1]):
            this_node = pixel_nodes[i, j]

            if i > 0 and pixel_nodes[i-1, j] != this_node:
                counts[this_node][pixel_nodes[i-1, j]] += 1
            if i < pixel_nodes.shape[0] - 1 and pixel_nodes[i+1, j] != this_node:
                counts[this_node][pixel_nodes[i+1, j]] += 1
            if j > 0 and pixel_nodes[i, j-1] != this_node:
                counts[this_node][pixel_nodes[i, j-1]] += 1
            if j < pixel_nodes.shape[1] - 1 and pixel_nodes[i, j+1] != this_node:
                counts[this_node][pixel_nodes[i, j+1]] += 1


    for this_node in range(1, num_nodes + 1):
        for potential_nbr in counts[this_node]:
            # set a reasonable threshold to avoid two opposit "corners" being marked as adjacent (corner cases, literally!)
            if counts[this_node][potential_nbr] > 5:
                puzzle_graph[this_node].add(potential_nbr)
                puzzle_graph[potential_nbr].add(this_node)
            if debug_print:
                print(f"neighbors of node {this_node} = {puzzle_graph[this_node]}")

    for this_node in range(1, num_nodes + 1):
        puzzle_graph[this_node] = frozenset(puzzle_graph[this_node])
    return puzzle_graph

def parse_image_graph(img_filename, num_colors, debug_print=False, debug_plots=False):
    img = get_original_image(img_filename)

    preprocessed_img = image_preprocessing(img)

    pixel_nodes, node_colors, num_nodes = label_pixels_by_node(preprocessed_img, num_colors, debug_print=debug_print)
    if debug_print:
        print(f"assigned pixels to contiguous nodes! there are {num_nodes} nodes")

    fig, (ax1, ax2) = plt.subplots(1, 2)
    c = ax1.pcolormesh(pixel_nodes, cmap='jet')
    ax1.invert_yaxis()
    ax1.set_title("node groupings")
    fig.colorbar(c, ax=ax1)

    puzzle = crop_to_puzzle(preprocessed_img)
    ax2.imshow(cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB))
    ax2.set_title("original image")
    if debug_plots:
        plt.show()

    # detect which nodes are adjacent to build the graph
    puzzle_graph = identify_adjacent_nodes(pixel_nodes, num_nodes, debug_print=debug_print)

    # dump to json for debugging
    # puzzle_graph_copy = {}
    # for i in range(1, num_nodes + 1):
    #     puzzle_graph_copy[i] = list(puzzle_graph[i])
    # with open("output_graph.json", 'w') as f:
    #     json.dump(puzzle_graph_copy, f)

    # print(node_colors)

    return puzzle_graph, node_colors

def main():
    parser = argparse.ArgumentParser(description='Given a screenshot of a Kami 2 puzzle, construct the graph representation of the puzzle state.')
    parser.add_argument('img_filename', type=str,
                        help='path to the screenshot')
    parser.add_argument('num_colors', type=int,
                        help='number of colors in the puzzle (used to help label colors)')

    args = parser.parse_args()
    print(args.img_filename)

    parse_image_graph(args.img_filename, args.num_colors, debug_print=True, debug_plots=True)

if __name__ == "__main__": main()
