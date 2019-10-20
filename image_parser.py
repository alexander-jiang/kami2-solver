import copy
import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt


img = cv2.imread("kami2puzzle18.png", cv2.IMREAD_COLOR)
puzzle_height_y = 1210
puzzle_width_x = img.shape[1]

bilateral_d = 5
bilateral_sigma = 100
bilateral_filtered_img = cv2.bilateralFilter(img, bilateral_d, bilateral_sigma, bilateral_sigma)

fig, (ax1, ax2) = plt.subplots(1, 2)
puzzle = copy.deepcopy(bilateral_filtered_img)
puzzle = puzzle[0:puzzle_height_y, 0:puzzle_width_x]
ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax1.set_title("original image")

ax2.imshow(cv2.cvtColor(bilateral_filtered_img, cv2.COLOR_BGR2RGB))
ax2.set_title(f"bilateral filter (d={bilateral_d}, sigma={bilateral_sigma})")
# plt.show()

print(puzzle.shape) # y by x by color
print(puzzle[0,0:5,:])

# Use K-means to reduce number of colors
pixel_colors = copy.deepcopy(puzzle)
pixel_colors = np.reshape(pixel_colors, (puzzle.shape[0] * puzzle.shape[1], puzzle.shape[2]))
pixel_colors = np.asarray(pixel_colors, dtype=np.float32)
print(pixel_colors.shape)
print(pixel_colors[0:5])

# configure kmeans
K = 4
max_iters = 100
epsilon = 1.0
termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iters, epsilon)
flags = cv2.KMEANS_RANDOM_CENTERS
random_restarts = 10

print(f"starting K means: max {max_iters} iterations, {random_restarts} random restarts")
compactness, labels, centers = cv2.kmeans(pixel_colors, K, None, termination_criteria, random_restarts, flags)
print("K means complete!")
print("compactness =", compactness)
print("centers =", centers)

# extract the color palette
img_copy = copy.deepcopy(img)
# top left corner of the color palette in the image (i.e. the node colors)
start_y = puzzle_height_y
start_x = 300
height_y = 124
width_x = 450
palette = img_copy[start_y:start_y+height_y, start_x:start_x+width_x]

# compare the k-means colors to the color palette
fig, (ax1, ax2) = plt.subplots(1, 2)
centers_rgb = [(center[2] / 255.0, center[1] / 255.0, center[0] / 255.0) for center in centers]
bounds = np.arange(K+1)
cmap = matplotlib.colors.ListedColormap(centers_rgb)
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
cb2 = matplotlib.colorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='horizontal')
ax1.set_title(f"k means colors (k = {K})")

ax2.imshow(cv2.cvtColor(palette, cv2.COLOR_BGR2RGB))
ax2.axis('off')
ax2.set_title("color palette from original image")
# plt.show()

flatten_labels = np.ravel(labels)
print("flattened labels:")
print(flatten_labels[0:5])
# convert colors in puzzle to the k-means colors
converted_pixels = [[round(centers[i,0]), round(centers[i,1]), round(centers[i,2])] for i in flatten_labels]
converted_puzzle = np.reshape(converted_pixels, (puzzle.shape[0], puzzle.shape[1], puzzle.shape[2]))
converted_puzzle = np.asarray(converted_puzzle, dtype=np.uint16)
print(converted_puzzle.shape)
print(converted_puzzle[0,0:5,:])

# compare the original puzzle to the k-means compressed version
fig2, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB))
ax1.set_title("original image")
ax1.axis('off')

ax2.imshow(cv2.cvtColor(converted_puzzle, cv2.COLOR_BGR2RGB))
ax2.set_title(f"converted image ({K} colors)")
ax2.axis('off')
# plt.show()

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

# parse contiguous regions (i.e. nodes) from converted colors
pixel_labels = np.reshape(flatten_labels, (puzzle_height_y, puzzle_width_x))
pixel_nodes = np.zeros((puzzle_height_y, puzzle_width_x))
next_node_number = 1
for pixel_y in range(puzzle_height_y):
    for pixel_x in range(puzzle_width_x):
        # if pixel was already marked with a node number, then don't change it
        if pixel_nodes[pixel_y, pixel_x] > 0:
            continue

        print(f"new node {next_node_number}: starting with pixel (y={pixel_y}, x={pixel_x})")
        pixel_nodes[pixel_y, pixel_x] = next_node_number
        next_node_number += 1

        neighbor_coords = get_neighbor_coords(pixel_y, pixel_x)

        # recursively assign the same node number to all contiguous pixels that are the same color
        while len(neighbor_coords) > 0:
            nbr_y, nbr_x = neighbor_coords.pop(0)
            if pixel_labels[nbr_y, nbr_x] == pixel_labels[pixel_y, pixel_x] and pixel_nodes[nbr_y, nbr_x] == 0:
                pixel_nodes[nbr_y, nbr_x] = pixel_nodes[pixel_y, pixel_x]
                neighbor_coords.extend(get_neighbor_coords(nbr_y, nbr_x))


fig, (ax1, ax2) = plt.subplots(1, 2)
c = ax1.pcolor(pixel_nodes)
ax1.invert_yaxis()
ax1.set_title("node groupings")
fig.colorbar(c, ax=ax1)

ax2.imshow(cv2.cvtColor(puzzle, cv2.COLOR_BGR2RGB))
ax2.set_title("original image")
plt.show()

# there are like 2 pixels labeled incorrectly: (y=954, x=371)
