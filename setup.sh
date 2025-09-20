#!/bin/bash

# Onction Dashboard Setup Script
# This script sets up a virtual environment, installs dependencies, and runs the app with PM2

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
}

# Check if Node.js is installed (required for PM2)
check_nodejs() {
    print_status "Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js is not installed. Please install Node.js first."
        print_status "You can install Node.js from: https://nodejs.org/"
        exit 1
    fi
}

# Check if PM2 is installed, install if not
check_and_install_pm2() {
    print_status "Checking PM2 installation..."
    if command -v pm2 &> /dev/null; then
        PM2_VERSION=$(pm2 --version)
        print_success "PM2 found: $PM2_VERSION"
    else
        print_warning "PM2 is not installed. Installing PM2 globally..."
        if npm install -g pm2; then
            print_success "PM2 installed successfully"
        else
            print_error "Failed to install PM2. Please install it manually: npm install -g pm2"
            exit 1
        fi
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_status "Activating virtual environment and installing dependencies..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Dependencies installed successfully"
}

# Create PM2 ecosystem file
create_pm2_config() {
    print_status "Creating PM2 ecosystem configuration..."
    
    cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'onction-dashboard',
    script: 'venv/bin/python',
    args: 'app/server.py',
    cwd: '$(pwd)',
    interpreter: 'none',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: '$(pwd)'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
EOF
    
    print_success "PM2 ecosystem configuration created"
}

# Create logs directory
create_logs_dir() {
    print_status "Creating logs directory..."
    mkdir -p logs
    print_success "Logs directory created"
}

# Start application with PM2
start_app() {
    print_status "Starting application with PM2..."
    
    # Stop existing PM2 processes if any
    pm2 stop onction-dashboard 2>/dev/null || true
    pm2 delete onction-dashboard 2>/dev/null || true
    
    # Start the application
    pm2 start ecosystem.config.js
    
    print_success "Application started with PM2"
    print_status "You can monitor the application with: pm2 monit"
    print_status "You can view logs with: pm2 logs onction-dashboard"
    print_status "You can stop the application with: pm2 stop onction-dashboard"
}

# Main execution
main() {
    print_status "Starting Onction Dashboard setup..."
    echo "=================================="
    
    # Check prerequisites
    check_python
    check_nodejs
    check_and_install_pm2
    
    # Setup environment
    create_venv
    install_dependencies
    create_logs_dir
    create_pm2_config
    
    # Start application
    start_app
    
    echo "=================================="
    print_success "Setup completed successfully!"
    print_status "Your Onction Dashboard is now running with PM2"
    print_status "Access the application at: http://localhost:8009"
}

# Run main function
main "$@"
