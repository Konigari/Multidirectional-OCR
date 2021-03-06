import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, disk
from skimage.measure import regionprops
from skimage.color import label2rgb
import skimage.io._io as io


image = io.imread('test.jpg', as_grey=True)

# apply threshold
thresh = threshold_otsu(image)
bw = closing(image > thresh, disk(15))

# remove artifacts connected to image border
cleared = bw.copy()
clear_border(cleared)

# label image regions
label_image = label(cleared)
borders = np.logical_xor(bw, cleared)
label_image[borders] = -1
image_label_overlay = label2rgb(label_image, image=image)

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
ax.imshow(image_label_overlay)

for region in regionprops(label_image):

    # skip small images
    if region.area < 100:
        continue

    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    if abs(region.orientation) > 0.01:
    	fig, bx = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    	bx.imshow(image[minr:maxr, minc:maxc])

    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)


# for region in regionprops(label_image)
# 	if abs(region.orientation)
plt.show()
