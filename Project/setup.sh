#!/bin/bash

# Setup script for Sistem Prediksi Penjualan UMKM project
# This script sets up the virtual environment and installs dependencies

echo "======================================"
echo "Setup Sistem Prediksi Penjualan UMKM"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ All dependencies installed successfully"
echo ""

# Create necessary folders
echo "📁 Creating necessary folders..."

folders=(
    "data/raw"
    "data/processed"
    "model"
    "notebooks"
    "docs"
)

for folder in "${folders[@]}"; do
    mkdir -p "$folder"
    echo "✅ Created folder: $folder"
done
echo ""

# Create .gitkeep files
echo "🏷️  Creating .gitkeep files..."

for folder in "${folders[@]}"; do
    touch "$folder/.gitkeep"
    echo "✅ Created .gitkeep in: $folder"
done
echo ""

echo "======================================"
echo "✅ Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the Streamlit app: streamlit run app/main.py"
echo ""
