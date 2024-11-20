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

# Check if required tools are installed
check_dependencies() {
    local missing_deps=0
    
    if ! command -v pytest &> /dev/null; then
        print_error "pytest is not installed"
        missing_deps=1
    fi
    
    if ! command -v flake8 &> /dev/null; then
        print_error "flake8 is not installed"
        missing_deps=1
    fi
    
    if ! command -v black &> /dev/null; then
        print_error "black is not installed"
        missing_deps=1
    fi
    
    if ! command -v isort &> /dev/null; then
        print_error "isort is not installed"
        missing_deps=1
    fi
    
    if [ $missing_deps -eq 1 ]; then
        print_status "Installing missing dependencies..."
        pip install -e ".[dev]"
    fi
}

# Run linting
run_linting() {
    print_status "Running linting checks..."
    
    # Change to the core package directory
    cd "$(dirname "$0")/../core" || exit 1
    
    echo "Running style checks..."
    black . --check
    isort . --check
    flake8 log2ml/ tests/ --max-line-length=100 --extend-ignore=E203 --statistics
    
    if [ $? -eq 0 ]; then
        print_success "Linting passed"
        return 0
    else
        print_error "Linting failed"
        return 1
    fi
}

# Run tests
run_tests() {
    print_status "Running tests with coverage..."
    
    # Change to the core package directory
    cd "$(dirname "$0")/../core" || exit 1
    
    echo "Running tests..."
    pytest tests/ -v --cov=log2ml --cov-report=xml --cov-report=term-missing
    
    if [ $? -eq 0 ]; then
        print_success "All tests passed"
        return 0
    else
        print_error "Tests failed"
        return 1
    fi
}

# Main execution
main() {
    local exit_code=0
    
    print_status "Starting test suite"
    check_dependencies
    
    # Run linting first
    if ! run_linting; then
        exit_code=1
    fi
    
    # Run tests even if linting failed
    if ! run_tests; then
        exit_code=1
    fi
    
    if [ $exit_code -eq 0 ]; then
        print_success "All checks passed successfully!"
    else
        print_error "Some checks failed. Please fix the issues above."
    fi
    
    exit $exit_code
}

# Run main function
main
