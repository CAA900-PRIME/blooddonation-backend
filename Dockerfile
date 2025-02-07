# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Python and necessary tools
RUN apt update && \
    apt install -y --no-install-recommends \
    python3 python3-pip python3-venv && \
    apt clean && rm -rf /var/lib/apt/lists/* \
	apt install -y pkg-config libmysqlclinet-dev \
	apt install -y build-essential

# Set the working directory
WORKDIR /app

# Expose port 5000 (default for Flask)
EXPOSE 5000
