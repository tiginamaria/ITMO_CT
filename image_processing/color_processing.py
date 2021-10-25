import binascii
import os
from collections import Counter

import imageio
import numpy as np
from PIL import ImageColor, Image
from sklearn.cluster import KMeans

from model.image_colors_info import ImageColorInfo, ImageColorsInfo
from utils.image_file_utils import get_parent_path


def _get_colors_clusters(img: np.array, colors_count: int = 10):
    """ Apply k-mean clustering to get main colors from image. """

    # Initialize k-mean classifier
    clt = KMeans(n_clusters=colors_count)

    # Fit classifier with image pixels
    clusters = clt.fit(img.reshape(-1, 3))

    # Get cluster centers
    cluster_centers = clusters.cluster_centers_
    cluster_labels = clusters.labels_

    # Calculate number of pixels for each cluster
    cluster_pixels_cnt = Counter(clusters.labels_)
    cluster_count = [cluster_pixels_cnt[i] for i in range(len(cluster_centers))]

    return cluster_centers, cluster_count, cluster_labels


def _build_clustered_image(img: np.array, centers: np.array, labels: np.array, output_dir: str) -> np.array:
    # Create copy of image
    c_img = img.reshape(-1, 3).copy()

    # Set each pixel color from its cluster
    for i, rgb_code in enumerate(centers):
        c_img[np.where(labels == i)] = rgb_code

    c_img = c_img.reshape(*img.shape)
    imageio.imwrite(os.path.join(output_dir, 'clusters.png'), c_img)

    return c_img


def _sort_colors_by_count(centers: np.array, count: np.array):
    # Sort cluster by their number of pixels
    return zip(*list(sorted(zip(count, centers), reverse=True, key=lambda p: p[0])))


def _build_colors_pallet(centers: np.array, output_dir: str) -> np.array:
    """ Build color pallet image for given set of colors. """

    # Create empty matrix for pallet image
    width = 300
    palette = np.zeros((100, 300, 3), np.uint8)
    steps = width / len(centers)

    # Set color for pallet boxes
    for i, rgb_code in enumerate(centers):
        palette[:, int(i * steps):(int((i + 1) * steps)), :] = rgb_code

    imageio.imwrite(os.path.join(output_dir, 'palette.png'), palette)

    return palette


def rgd_to_hex(rgb_code: np.array) -> str:
    """ Convert rgb to hex color format. """

    colour = binascii.hexlify(bytearray(int(c) for c in rgb_code)).decode('ascii')
    return colour


def hex_to_rgb(hex: str) -> np.array:
    """ Convert hex to rgb color format. """

    return ImageColor.getcolor(hex, "RGB")


def get_color_info(image_file: str) -> ImageColorsInfo:
    """ Get main colors from image using k-mean clustering method.
    :param image_file: path to file with image to get main colors from
    :return: image color information
    """

    image = Image.open(image_file)
    image_dir = get_parent_path(image_file)

    img = np.asarray(image)
    centers, counts, labels = _get_colors_clusters(img)

    # Build and visualize clustered image
    _build_clustered_image(img, centers, labels, image_dir)

    # centers, counts = _sort_colors_by_count(centers, counts)

    # Build and visualize colors pallet
    _build_colors_pallet(centers, image_dir)

    colors = []
    for center, count in zip(centers, counts):
        colors.append(ImageColorInfo(r=center[0], g=center[1], b=center[2], percent=int(100 * (count / img.size))))

    return ImageColorsInfo(colors=colors)
