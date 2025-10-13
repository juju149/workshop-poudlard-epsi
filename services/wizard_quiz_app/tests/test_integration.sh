#!/bin/bash
# Integration test - requires Flutter SDK installed

set -e

echo "🧪 Integration Test - Wizard Quiz App"
echo "======================================"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed. Please install Flutter SDK first."
    echo "Visit: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "✅ Flutter is installed"

# Navigate to Flutter project
cd src/wizard_quiz

echo ""
echo "📦 Getting dependencies..."
flutter pub get

echo ""
echo "🔍 Analyzing code..."
flutter analyze

echo ""
echo "🧪 Running unit tests..."
flutter test

echo ""
echo "✅ All integration tests passed!"
