FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Python and necessary tools
RUN apt update && \
    apt install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    pkg-config \
    libmysqlclient-dev \
    build-essential && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

EXPOSE 8080

# Set the default command to run the app
CMD ["python3", "app.py"]
