import copy
import numpy as np
import cv2
import matplotlib
from matplotlib import pyplot as plt


img = cv2.imread("kami2puzzle18.png", cv2.IMREAD_COLOR)
puzzle_height_y = 1210
puzzle_width_x = img.shape[1]

puzzle = copy.deepcopy(img)
puzzle = puzzle[0:puzzle_height_y, 0:puzzle_width_x]
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("original image")
plt.show()

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
plt.show()

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
plt.show()
