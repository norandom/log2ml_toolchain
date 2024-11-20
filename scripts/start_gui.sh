#!/bin/bash

# Change to the GUI directory
cd "$(dirname "$0")/../gui/vector-analyzer"

# Check if yarn is installed
if ! command -v yarn &> /dev/null; then
    echo "yarn is not installed. Installing yarn..."
    npm install -g yarn
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    yarn install
fi

# Start the Tauri development server
echo "Starting Vector Analyzer..."
yarn run tauri:dev
