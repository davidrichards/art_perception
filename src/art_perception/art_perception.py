import json
import numpy as np
from PIL import Image
from pydantic import BaseModel, Field
import requests
from sklearn.cluster import KMeans
from typing import List, Tuple, Optional
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

DEFAULT_NUM_COLORS = 6


class ColorSwatch(BaseModel):
    rgb: Tuple[int, int, int]
    hex: str
    proportion: float = Field(ge=0.0, le=1.0, default=1.0 / DEFAULT_NUM_COLORS)
    label: Optional[str] = None


def extract_palette(
    image: Image.Image, num_colors=DEFAULT_NUM_COLORS, resize_to=200
) -> List[ColorSwatch]:
    image = image.convert("RGB")
    image.thumbnail((resize_to, resize_to))

    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(pixels)
    counts = np.bincount(labels)

    total = counts.sum()
    centroids = kmeans.cluster_centers_.astype(int)

    swatches = []
    for i, count in enumerate(counts):
        rgb = tuple(centroids[i])
        hex_code = "#{:02x}{:02x}{:02x}".format(*rgb)
        proportion = count / total
        swatches.append(ColorSwatch(rgb=rgb, hex=hex_code, proportion=proportion))

    swatches.sort(key=lambda s: s.proportion, reverse=True)
    return swatches


def path_to_image(path: str) -> Image.Image:
    return Image.open(path)


def path_to_palette(
    path: str, num_colors: int = DEFAULT_NUM_COLORS, resize_to: int = 200
) -> List[ColorSwatch]:
    image = path_to_image(path)
    return extract_palette(image, num_colors, resize_to)


def url_to_image(url: str) -> Image.Image:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes
    return Image.open(response.raw)


def url_to_palette(
    url: str, num_colors: int = DEFAULT_NUM_COLORS, resize_to: int = 200
) -> List[ColorSwatch]:
    image = url_to_image(url)
    return extract_palette(image, num_colors, resize_to)


def swatches_to_json(swatches: List[ColorSwatch]) -> str:
    return json.dumps([swatch.model_dump() for swatch in swatches])


def swatches_to_json_file(swatches: List[ColorSwatch], path: str):
    with open(path, "w") as f:
        json.dump([swatch.model_dump() for swatch in swatches], f)


def swatches_to_visual(swatches: List[ColorSwatch], width: int = 80) -> Text:
    """Create a visual representation of the swatches using colored blocks.

    Args:
        swatches: List of ColorSwatch objects
        width: Width of the visual representation in characters

    Returns:
        A Text object containing the visual representation
    """
    visual = Text()

    # Calculate the width for each swatch based on its proportion
    total_width = 0
    for swatch in swatches:
        swatch_width = int(width * swatch.proportion)
        if swatch_width == 0 and swatch.proportion > 0:
            swatch_width = 1  # Ensure at least one character for non-zero proportions
        total_width += swatch_width

    # Adjust the last swatch's width to match the total width
    if total_width != width and swatches:
        swatches[-1].proportion += (width - total_width) / width

    # Create the visual representation
    for swatch in swatches:
        swatch_width = int(width * swatch.proportion)
        if swatch_width > 0:
            block = "█" * swatch_width
            visual.append(
                block, style=f"rgb({swatch.rgb[0]},{swatch.rgb[1]},{swatch.rgb[2]})"
            )

    return visual
