#!/bin/bash

# ANSI color codes
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored status messages
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

# Check if flake8 is installed
if ! command -v flake8 &> /dev/null; then
    print_error "flake8 is not installed. Installing now..."
    pip install flake8
fi

print_status "Running flake8 linter..."

# Run flake8 with specified configuration
flake8 tools/ tests/ \
    --max-line-length=100 \
    --extend-ignore=E203 \
    --statistics \
    --show-source \
    --count

# Check the exit code
if [ $? -eq 0 ]; then
    print_success "Linting passed successfully!"
    exit 0
else
    print_error "Linting failed. Please fix the issues above."
    exit 1
fi
