# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables - Disable interaction, Enable Debug
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Python and necessary tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy only the requirements file first (for caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5000 (default for Flask)
EXPOSE 5000

# Run the Flask app (server-side rendering)
CMD ["python3", "app.py"]
