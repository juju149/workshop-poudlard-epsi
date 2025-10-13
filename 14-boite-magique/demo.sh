#!/bin/bash

# Example usage script for Magic Box
# Demonstrates various features

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    🧪 MAGIC BOX - DEMONSTRATION SCRIPT 🧪                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if binary exists
if [ ! -f "./build/bin/magic-box" ]; then
    echo "❌ Binary not found. Please run ./build.sh first"
    exit 1
fi

MAGIC_BOX="./build/bin/magic-box"

echo "📚 Example 1: Display help"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$MAGIC_BOX --help
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📊 Example 2: Show statistics for Markdown files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$MAGIC_BOX -r . -s -e .md
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📊 Example 3: Show statistics for C++ files"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$MAGIC_BOX -r . -s -e .cpp,.h,.hpp
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📦 Example 4: Create archive of current project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$MAGIC_BOX -r . -o /tmp/magic-box-demo -e .cpp,.h,.md
echo ""
echo "📂 Checking archive contents:"
ls -lR /tmp/magic-box-demo | head -20
echo ""
read -p "Press Enter to continue..."
echo ""

echo "📊 Example 5: Analyze entire workshop structure"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$MAGIC_BOX -r .. -s
echo ""

echo "✅ Demonstration complete!"
echo ""
echo "💡 Try your own commands:"
echo "   $MAGIC_BOX -r <directory> -o <output> -e <extensions>"
