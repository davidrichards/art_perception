from typing import List, Any
from PIL import Image
import numpy as np
import cv2

from .domain import ColorSwatch


def histogram_peaks_extractor(
    image: Image.Image,
    num_colors: int = 6,
    resize_to: int = 200,
    h_bins: int = 12,
    s_bins: int = 4,
    v_bins: int = 4,
) -> List[Any]:
    """
    Extracts vibrant, diverse colors using 3D HSV histogram binning.

    Args:
        image (PIL.Image.Image): Input image.
        num_colors (int): Number of color swatches to extract.
        resize_to (int): Resize for processing efficiency.
        h_bins (int): Number of hue bins (0–180 in OpenCV).
        s_bins (int): Number of saturation bins (0–255).
        v_bins (int): Number of value (brightness) bins (0–255).

    Returns:
        List[ColorSwatch]: Dominant vibrant color swatches.
    """
    # Prepare image
    image = image.convert("RGB")
    image.thumbnail((resize_to, resize_to))
    image_np = np.array(image)
    hsv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

    # Flatten to pixel array
    pixels = hsv_image.reshape(-1, 3)
    h, s, v = pixels[:, 0], pixels[:, 1], pixels[:, 2]

    # Vibrant color filter
    vibrant_mask = (s > 50) & (v > 50)
    vibrant_pixels = pixels[vibrant_mask]

    if len(vibrant_pixels) == 0:
        vibrant_pixels = pixels

    # Compute 3D histogram
    hist, edges = np.histogramdd(
        vibrant_pixels,
        bins=(h_bins, s_bins, v_bins),
        range=((0, 180), (0, 256), (0, 256)),
    )

    # Get bin indices sorted by count
    flat_hist = hist.flatten()
    top_indices = np.argsort(flat_hist)[-num_colors:][::-1]

    # Decode bin index to HSV bin ranges
    swatches = []
    bin_indices = np.array(np.unravel_index(top_indices, hist.shape)).T

    for h_idx, s_idx, v_idx in bin_indices:
        h_min, h_max = edges[0][h_idx], edges[0][h_idx + 1]
        s_min, s_max = edges[1][s_idx], edges[1][s_idx + 1]
        v_min, v_max = edges[2][v_idx], edges[2][v_idx + 1]

        # Mask pixels in that bin
        in_bin_mask = (
            (vibrant_pixels[:, 0] >= h_min)
            & (vibrant_pixels[:, 0] < h_max)
            & (vibrant_pixels[:, 1] >= s_min)
            & (vibrant_pixels[:, 1] < s_max)
            & (vibrant_pixels[:, 2] >= v_min)
            & (vibrant_pixels[:, 2] < v_max)
        )
        bin_pixels = vibrant_pixels[in_bin_mask]

        if len(bin_pixels) == 0:
            continue

        # Average HSV and convert to RGB
        avg_hsv = np.mean(bin_pixels, axis=0).astype(np.uint8)
        hsv_color = np.uint8([[avg_hsv]])
        rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)[0][0]

        proportion = len(bin_pixels) / len(vibrant_pixels)
        rgb = tuple(int(c) for c in rgb_color)
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)

        swatches.append(ColorSwatch(rgb=rgb, hex=hex_code, proportion=proportion))

    swatches.sort(key=lambda s: s.proportion, reverse=True)
    return swatches
