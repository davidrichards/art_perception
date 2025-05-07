FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including OpenCV requirements
RUN apt-get update && apt-get install -y build-essential curl git libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-dev && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements_dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements_dev.txt

# Copy the project files
COPY . .

# Install the package in development mode with verbose output
RUN pip install -e . -v

# Create a shell script to keep the container running
RUN echo '#!/bin/bash\nwhile true; do sleep 1; done' >/keep-alive.sh && chmod +x /keep-alive.sh

# Set the entrypoint to our keep-alive script
ENTRYPOINT ["/keep-alive.sh"]
