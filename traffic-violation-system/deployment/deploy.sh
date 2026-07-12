#!/bin/bash

# Enterprise Traffic Violation System Deployment Script
echo "=========================================================="
echo "      ENTERPRISE TRAFFIC VIOLATION SYSTEM DEPLOYMENT      "
echo "=========================================================="

# Check if Docker is installed
if ! [ -x "$(command -v docker)" ]; then
  echo 'Error: docker is not installed. Please install Docker to continue.' >&2
  exit 1
fi

# Check if Docker Compose is installed
if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed. Please install Docker Compose to continue.' >&2
  exit 1
fi

echo "[1/3] Validating configuration files..."
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: Please run this script from the deployment/ directory."
  exit 1
fi

echo "[2/3] Building and starting all containers in daemon mode..."
docker-compose up -d --build

echo "[3/3] Checking running services..."
docker-compose ps

echo "=========================================================="
echo "Deployment successful! Services are exposed on port 80."
echo "=========================================================="
