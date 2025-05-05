from PIL import Image
from typing import List, Any

from .domain import Strategy
from .extract_colorfullness import extract_colorfulness
from .kmeans_extractor import kmeans_extractor
from .histogram_peaks_extractor import histogram_peaks_extractor


def extract_palette(
    image: Image.Image,
    num_colors=6,
    resize_to=200,
    bins=64,
    strategy=Strategy.KMEANS,
    **kwargs,
) -> List[Any]:
    """
    Extracts a palette of colors from an image using a specified strategy.

    Args:
        image (PIL.Image.Image): Input image.
        num_colors (int): Number of colors to extract.
        resize_to (int): Resize the image to this size.
        bins (int): Number of bins for the histogram.
        strategy (Strategy): The strategy to use for extracting the palette.

    Returns:
        List[ColorSwatch]: List of ColorSwatch objects containing RGB values, hex codes, and proportions.
    """

    if strategy == Strategy.KMEANS:
        return kmeans_extractor(
            image, num_colors=num_colors, resize_to=resize_to, **kwargs
        )
    elif strategy == Strategy.HISTOGRAM_PEAKS:
        h_bins = 12
        s_bins = 4
        v_bins = 4
        kwargs.setdefault("h_bins", h_bins)
        kwargs.setdefault("s_bins", s_bins)
        kwargs.setdefault("v_bins", v_bins)

        return histogram_peaks_extractor(image, **kwargs)
    elif strategy == Strategy.COLORFULLNESS:
        return extract_colorfulness(
            image, num_colors=num_colors, resize_to=resize_to, **kwargs
        )
    else:
        raise ValueError(f"Invalid strategy: {strategy}")
