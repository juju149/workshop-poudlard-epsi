#!/bin/bash

# Build script for Magic Box - Linux/macOS
# La Boite Magique de Severus Rogue

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    🧪 LA BOITE MAGIQUE DE SEVERUS ROGUE 🧪                 ║"
echo "║                      Build Script                            ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required tools
echo "🔍 Checking prerequisites..."

if ! command -v cmake &> /dev/null; then
    echo -e "${RED}❌ CMake is not installed${NC}"
    echo "Please install CMake 3.15 or later"
    exit 1
fi

if ! command -v g++ &> /dev/null && ! command -v clang++ &> /dev/null; then
    echo -e "${RED}❌ No C++ compiler found${NC}"
    echo "Please install g++ or clang++"
    exit 1
fi

echo -e "${GREEN}✅ CMake found: $(cmake --version | head -1)${NC}"
if command -v g++ &> /dev/null; then
    echo -e "${GREEN}✅ G++ found: $(g++ --version | head -1)${NC}"
elif command -v clang++ &> /dev/null; then
    echo -e "${GREEN}✅ Clang++ found: $(clang++ --version | head -1)${NC}"
fi

# Create build directory
echo ""
echo "📁 Creating build directory..."
mkdir -p build
cd build

# Configure
echo ""
echo "⚙️  Configuring project with CMake..."
cmake -DCMAKE_BUILD_TYPE=Release ..

# Build
echo ""
echo "🔨 Building project..."
cmake --build . -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 2)

# Check if build was successful
if [ -f bin/magic-box ]; then
    echo ""
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo ""
    echo "📦 Binary location: $(pwd)/bin/magic-box"
    echo ""
    echo "🚀 To run the program:"
    echo "   cd build"
    echo "   ./bin/magic-box --help"
    echo ""
    echo "🔧 To install system-wide (optional):"
    echo "   sudo cmake --install ."
    echo ""
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi
