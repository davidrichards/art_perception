import json
import requests
from typing import List
from rich.text import Text
from PIL import Image

from .domain import ColorSwatch, Strategy
from .extract import extract_palette

DEFAULT_NUM_COLORS = 6


def path_to_image(path: str) -> Image.Image:
    return Image.open(path)


def path_to_palette(
    path: str,
    num_colors: int = DEFAULT_NUM_COLORS,
    resize_to: int = 200,
    strategy: Strategy = Strategy.COLORFULLNESS,
) -> List[ColorSwatch]:
    image = path_to_image(path)
    return extract_palette(image, num_colors, resize_to, strategy=strategy)


def url_to_image(url: str) -> Image.Image:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes
    return Image.open(response.raw)


def url_to_palette(
    url: str,
    num_colors: int = DEFAULT_NUM_COLORS,
    resize_to: int = 200,
    strategy: Strategy = Strategy.COLORFULLNESS,
) -> List[ColorSwatch]:
    image = url_to_image(url)
    return extract_palette(image, num_colors, resize_to, strategy=strategy)


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
