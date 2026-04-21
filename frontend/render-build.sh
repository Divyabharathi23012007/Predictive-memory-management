#!/bin/bash
# Build script for frontend deployment
echo "Building frontend for Render deployment..."

# Create a simple build script
mkdir -p build
cp index.html build/index.html
cp nginx.conf build/

echo "Frontend build complete!"
