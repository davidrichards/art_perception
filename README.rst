==============
Art Perception
==============


.. image:: https://img.shields.io/pypi/v/art_perception.svg
        :target: https://pypi.python.org/pypi/art_perception

.. image:: https://img.shields.io/travis/davidrichards/art_perception.svg
        :target: https://travis-ci.com/davidrichards/art_perception

.. image:: https://readthedocs.org/projects/art-perception/badge/?version=latest
        :target: https://art-perception.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/davidrichards/art_perception/shield.svg
     :target: https://pyup.io/repos/github/davidrichards/art_perception/
     :alt: Updates



Art Perception contains all the tools you need to obegin observing attributes found in art and sharing this information to a digital audience.


* Free software: MIT license
* Documentation: https://art-perception.readthedocs.io.


Features
--------

Extract Palette
~~~~~~~~~~~~~

The extract-palette utility allows you to extract color palettes from images using various strategies. You can process both local images and images from URLs.

Basic Usage
^^^^^^^^^^

Process an image from a URL:

.. code-block:: bash

   ./bin/extract-palette https://example.com/image.jpg

Process a local image:

.. code-block:: bash

   ./bin/extract-palette path/to/local/image.jpg

Available Strategies
^^^^^^^^^^^^^^^^^

The tool offers three different strategies for color extraction:

1. **Colorfulness** (default): Extracts vibrant colors by ranking pixels by colorfulness and clustering in LAB space. Best for finding the most visually striking colors.

2. **KMeans**: Uses K-means clustering to find the most representative colors in the image. Good for finding dominant color groups.

3. **Histogram Peaks**: Extracts vibrant, diverse colors using 3D HSV histogram binning. Effective for finding distinct color regions.

To specify a strategy, use the --strategy option:

.. code-block:: bash

   ./bin/extract-palette image.jpg --strategy kmeans
   ./bin/extract-palette image.jpg --strategy histogram_peaks
   ./bin/extract-palette image.jpg --strategy colorfulness

Additional Options
^^^^^^^^^^^^^^^

* ``--num-colors`` or ``-n``: Number of colors to extract (default: 6)
* ``--resize`` or ``-r``: Size to resize the image to before processing (default: 200 pixels)
* ``--width`` or ``-w``: Width of the visual representation in characters (default: 80)
* ``--json`` or ``-j``: Show the JSON output instead of the visual representation
* ``--details`` or ``-d``: Show detailed information about each color
* ``--no-palette`` or ``-np``: Hide the color palette visualization
* ``--output`` or ``-o``: Save the output to a JSON file

Example with Options
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   ./bin/extract-palette image.jpg --strategy kmeans --num-colors 8 --resize 300 --width 100 --details --output palette.json

Output Format
^^^^^^^^^^^

The tool provides both visual and JSON output formats. The JSON output includes:

* RGB values for each color
* Hex color codes
* Proportion of each color in the image

Docker Usage
~~~~~~~~~~~

The project includes Docker configuration for consistent development and usage across different environments.

Building and Running
^^^^^^^^^^^^^^^^^

Build the container:

.. code-block:: bash

   docker-compose build

Start the container:

.. code-block:: bash

   docker-compose up -d

Enter the container:

.. code-block:: bash

   docker-compose exec cli bash

Now you can use the CLI tools inside the container. For example:

.. code-block:: bash

   extract-palette image.jpg --strategy kmeans

VS Code Development
^^^^^^^^^^^^^^^^

For VS Code users, the project includes a devcontainer configuration:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. VS Code will build the container and set up the development environment with:
   - Python extensions
   - Code formatting (Black)
   - Linting (Flake8)
   - Git integration

The container includes all necessary dependencies and tools for development.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
