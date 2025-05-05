from typing import List, Any
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

from .domain import ColorSwatch


def kmeans_extractor(
    image: Image.Image, num_colors: int = 6, resize_to: int = 200, **kwargs
) -> List[Any]:
    """
    Extracts the most representative colors from an image using KMeans clustering.
    This strategy focuses on finding the main color groups in the image.

    Args:
        image (PIL.Image.Image): Input image.
        num_colors (int): Number of dominant color clusters to extract.
        resize_to (int): Size to resize the image to before processing.

    Returns:
        List[ColorSwatch]: List of ColorSwatch objects containing RGB values, hex codes, and proportions.
    """
    # Resize image and convert to RGB
    image = image.convert("RGB")
    image.thumbnail((resize_to, resize_to))
    image_np = np.array(image)
    h, w, _ = image_np.shape

    # Flatten the image to get RGB pixels
    pixels = image_np.reshape(-1, 3).astype(np.float32)

    # Cluster all pixels
    kmeans = KMeans(n_clusters=num_colors, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(pixels)
    counts = np.bincount(labels)
    total = counts.sum()

    # Build the swatches
    swatches = []
    for i in range(num_colors):
        rgb = tuple(kmeans.cluster_centers_[i].astype(int))
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        proportion = counts[i] / total
        swatches.append(ColorSwatch(rgb=rgb, hex=hex_code, proportion=proportion))

    swatches.sort(key=lambda s: s.proportion, reverse=True)
    return swatches
