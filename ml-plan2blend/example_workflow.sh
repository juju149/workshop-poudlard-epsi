#!/usr/bin/env bash
# Example workflow script for ML Plan2Blend
# Demonstrates the complete pipeline from PDF to .blend file

set -e  # Exit on error

echo "=========================================="
echo "ML Plan2Blend - Example Workflow"
echo "=========================================="
echo ""

# Configuration
INPUT_PDF="${INPUT_PDF:-data/input/PRIVE_Plans_THALIE_Montpellier.pdf}"
WORK_DIR="data/work"
OUTPUT_DIR="build/out"
REPORTS_DIR="build/reports"
SCALE="${SCALE:-1:150}"
DPI="${DPI:-600}"

# Create directories
mkdir -p "$WORK_DIR" "$OUTPUT_DIR" "$REPORTS_DIR"

echo "Configuration:"
echo "  Input PDF: $INPUT_PDF"
echo "  Scale: $SCALE"
echo "  DPI: $DPI"
echo ""

# Step 1: Convert PDF to PNG
echo "Step 1: Converting PDF to PNG..."
if [ -f "$INPUT_PDF" ]; then
    python -m src.utils.io pdf2png \
        --pdf "$INPUT_PDF" \
        --out "$WORK_DIR/plan_600dpi.png" \
        --dpi "$DPI"
    echo "✓ PDF converted"
else
    echo "⚠ PDF not found, creating test image instead..."
    python -c "
import numpy as np
import cv2

# Create a simple test floor plan
img = np.ones((800, 1000, 3), dtype=np.uint8) * 255

# Draw walls
cv2.rectangle(img, (50, 50), (950, 750), (0, 0, 0), 20)
cv2.line(img, (50, 400), (950, 400), (0, 0, 0), 20)
cv2.line(img, (500, 50), (500, 750), (0, 0, 0), 20)

cv2.imwrite('$WORK_DIR/plan_600dpi.png', img)
print('✓ Test plan created')
"
fi
echo ""

# Step 2: Run inference (Image → JSON)
echo "Step 2: Running inference pipeline..."
python -m src.inference.infer \
    --image "$WORK_DIR/plan_600dpi.png" \
    --scale "$SCALE" \
    --dpi "$DPI" \
    --floor-code "RDC" \
    --floor-name "Rez-de-chaussée" \
    --out "$OUTPUT_DIR/floorplan.json"
echo "✓ Inference complete"
echo ""

# Step 3: Validate JSON
echo "Step 3: Validating JSON..."
python -m src.utils.io validate \
    --json "$OUTPUT_DIR/floorplan.json"
echo ""

# Step 4: Generate Blender file (if Blender is available)
echo "Step 4: Generating Blender file..."
if command -v blender &> /dev/null; then
    blender -b -P src/blender/json_to_blender.py -- \
        "$OUTPUT_DIR/floorplan.json" \
        "$OUTPUT_DIR/thalie.blend" \
        --wall_thickness 0.20 \
        --wall_height 2.80
    echo "✓ Blender file generated"
    echo "  Output: $OUTPUT_DIR/thalie.blend"
    echo "  Output: $OUTPUT_DIR/thalie.glb"
else
    echo "⚠ Blender not found, skipping 3D generation"
    echo "  To install Blender: https://www.blender.org/download/"
fi
echo ""

# Step 5: Run QA metrics (if ground truth available)
echo "Step 5: Quality assurance..."
echo "⚠ QA metrics require ground truth masks (not available in this demo)"
echo "  To run QA: python -m src.inference.metrics \\"
echo "    --plan $WORK_DIR/plan_600dpi.png \\"
echo "    --pred-mask [predicted_mask.png] \\"
echo "    --gt-mask [ground_truth_mask.png] \\"
echo "    --out $REPORTS_DIR"
echo ""

# Summary
echo "=========================================="
echo "Workflow Complete!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  - Plan image: $WORK_DIR/plan_600dpi.png"
echo "  - Floorplan JSON: $OUTPUT_DIR/floorplan.json"
if [ -f "$OUTPUT_DIR/thalie.blend" ]; then
    echo "  - Blender file: $OUTPUT_DIR/thalie.blend"
    echo "  - glTF export: $OUTPUT_DIR/thalie.glb"
fi
echo ""
echo "Next steps:"
echo "  1. Annotate training data (CVAT/Label Studio)"
echo "  2. Train segmentation model: python -m src.training.train_segmentation"
echo "  3. Train detection model: python -m src.training.train_detection"
echo "  4. Run inference on real plans"
echo "  5. Validate with QA metrics"
echo ""
