#!/usr/bin/env python3

"""Console script for art_perception."""

import art_perception
from pathlib import Path
from typing import Optional
import sys

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()


@app.command()
def main(
    image_source: str = typer.Argument(..., help="Path to image file or URL"),
    output_path: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to save JSON output. If not provided, output will be printed to console",
    ),
    num_colors: int = typer.Option(
        art_perception.DEFAULT_NUM_COLORS,
        "--num-colors",
        "-n",
        help="Number of colors to extract from the image",
    ),
    resize_to: int = typer.Option(
        200,
        "--resize",
        "-r",
        help="Size to resize the image to before processing (in pixels)",
    ),
    visual_width: int = typer.Option(
        80,
        "--width",
        "-w",
        help="Width of the visual representation in characters",
    ),
):
    """Extract color palette from an image file or URL.

    The image can be provided either as a local file path or a URL.
    The output will be a list of color swatches with their RGB values,
    hex codes, and proportions. The output can be saved to a JSON file
    or printed to the console.
    """
    try:
        # Determine if the source is a URL or file path
        if image_source.startswith(("http://", "https://")):
            console.print(f"Processing image from URL: {image_source}")
            try:
                swatches = art_perception.url_to_palette(
                    image_source, num_colors=num_colors, resize_to=resize_to
                )
            except Exception as e:
                console.print(f"[red]Error processing URL: {str(e)}[/red]")
                console.print(
                    "[yellow]Note: Make sure to use a direct image URL, not a webpage URL.[/yellow]"
                )
                raise typer.Exit(1)
        else:
            console.print(f"Processing image from path: {image_source}")
            try:
                swatches = art_perception.path_to_palette(
                    image_source, num_colors=num_colors, resize_to=resize_to
                )
            except Exception as e:
                console.print(f"[red]Error processing file: {str(e)}[/red]")
                raise typer.Exit(1)

        # Display visual representation
        visual = art_perception.swatches_to_visual(swatches, width=visual_width)
        console.print("\nColor Palette Visualization:")
        console.print(Panel(visual, title="Color Proportions", border_style="dim"))

        # Display color details
        console.print("\nColor Details:")
        for swatch in swatches:
            console.print(
                f"RGB: {swatch.rgb}  Hex: {swatch.hex}  Proportion: {swatch.proportion:.2%}"
            )

        # Handle output
        if output_path:
            try:
                art_perception.swatches_to_json_file(swatches, str(output_path))
                console.print(f"\n[green]Color palette saved to {output_path}[/green]")
            except Exception as e:
                console.print(f"[red]Error saving to file: {str(e)}[/red]")
                raise typer.Exit(1)
        else:
            try:
                json_output = art_perception.swatches_to_json(swatches)
                console.print("\nJSON Output:")
                console.print(json_output)
            except Exception as e:
                console.print(f"[red]Error generating JSON: {str(e)}[/red]")
                raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
