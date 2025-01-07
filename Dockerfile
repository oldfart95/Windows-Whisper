FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    devscripts \
    debhelper \
    dh-python \
    fakeroot \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt
RUN pip3 install stdeb

# Build the package
CMD ["./build_linux.sh"]
