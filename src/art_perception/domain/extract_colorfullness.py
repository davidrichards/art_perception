from typing import List, Any
from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans

from .domain import ColorSwatch


def extract_colorfulness(
    image: Image.Image, num_colors: int = 6, resize_to: int = 200
) -> List[Any]:
    """
    Extracts vibrant colors by ranking pixels by colorfulness and clustering in LAB space.

    Args:
        image (PIL.Image.Image): Input image.
        num_colors (int): Number of vibrant color swatches to return.
        resize_to (int): Resize image to speed up computation.

    Returns:
        List[ColorSwatch]: List of ColorSwatch objects with RGB, hex, and proportion.
    """
    # Resize and convert to RGB
    image = image.convert("RGB")
    image.thumbnail((resize_to, resize_to))
    image_np = np.array(image)
    h, w, _ = image_np.shape

    # Convert to HSV for filtering
    hsv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    h_channel, s_channel, v_channel = cv2.split(hsv_image)

    # Filter for vibrant pixels
    mask = (s_channel > 50) & (v_channel > 50)
    pixels_rgb = image_np.reshape(-1, 3)
    vibrant_pixels = (
        pixels_rgb[mask.reshape(-1)] if np.count_nonzero(mask) > 0 else pixels_rgb
    )

    # Compute Hasler–Süsstrunk colorfulness metric
    R, G, B = vibrant_pixels[:, 0], vibrant_pixels[:, 1], vibrant_pixels[:, 2]
    rg = np.abs(R - G)
    yb = np.abs(0.5 * (R + G) - B)
    colorfulness = np.sqrt(rg**2 + yb**2)

    # Get top 20% most colorful pixels
    top_pct = 0.2
    num_top = max(1, int(len(vibrant_pixels) * top_pct))
    top_indices = np.argsort(colorfulness)[-num_top:]
    top_pixels = vibrant_pixels[top_indices]

    # Convert to LAB
    lab_pixels = cv2.cvtColor(top_pixels[np.newaxis, :, :], cv2.COLOR_RGB2LAB)[0]

    # Run KMeans
    kmeans = KMeans(n_clusters=num_colors, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(lab_pixels)
    counts = np.bincount(labels)
    total = counts.sum()

    # Convert centroids back to RGB
    lab_centroids = kmeans.cluster_centers_.astype(np.uint8)
    lab_centroids = lab_centroids.reshape(-1, 1, 3)
    rgb_centroids = cv2.cvtColor(lab_centroids, cv2.COLOR_LAB2RGB).reshape(-1, 3)

    # Build swatches
    swatches = []
    for i in range(num_colors):
        rgb = tuple(int(c) for c in rgb_centroids[i])
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        proportion = counts[i] / total
        swatches.append(ColorSwatch(rgb=rgb, hex=hex_code, proportion=proportion))

    swatches.sort(key=lambda s: s.proportion, reverse=True)
    return swatches
