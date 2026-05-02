# Setup script for Sistem Prediksi Penjualan UMKM project (Windows)
# This script sets up the virtual environment and installs dependencies

Write-Host "======================================"
Write-Host "Setup Sistem Prediksi Penjualan UMKM"
Write-Host "======================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion"
} catch {
    Write-Host "Python is not installed. Please install Python first."
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to create virtual environment"
    exit 1
}
Write-Host "Virtual environment created"
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..."
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment"
    exit 1
}
Write-Host "Virtual environment activated"
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install dependencies"
    exit 1
}
Write-Host "All dependencies installed successfully"
Write-Host ""

# Create necessary folders
Write-Host "Creating necessary folders..."

$folders = @(
    "data\raw",
    "data\processed",
    "model",
    "notebooks",
    "docs"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
    }
    Write-Host "Created folder: $folder"
}
Write-Host ""

# Create .gitkeep files
Write-Host "Creating .gitkeep files..."

foreach ($folder in $folders) {
    $gitkeepPath = Join-Path $folder ".gitkeep"
    if (-not (Test-Path $gitkeepPath)) {
        New-Item -ItemType File -Path $gitkeepPath -Force | Out-Null
    }
    Write-Host "Created .gitkeep in: $folder"
}
Write-Host ""

Write-Host "======================================"
Write-Host "Setup completed successfully!"
Write-Host "======================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Virtual environment is already activated"
Write-Host "2. Run Streamlit app: streamlit run app/main.py"
Write-Host ""
