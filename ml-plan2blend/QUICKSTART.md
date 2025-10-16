# Quick Start Guide — ML Plan2Blend

Get started with ML Plan2Blend in 5 minutes!

## Prerequisites

- Python 3.10+
- (Optional) Blender 3.x+ for 3D generation
- (Optional) Docker for containerized deployment

## Installation

### 1. Clone the repository

```bash
cd ml-plan2blend
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify installation

```bash
python -m pytest tests/ -v
```

You should see all tests passing (23 tests).

## Quick Example

### Run the complete workflow

```bash
bash example_workflow.sh
```

This will:
1. Create a test floor plan image
2. Run inference to generate JSON
3. Validate the output
4. (Optional) Generate Blender file if available

### Step-by-step usage

#### 1. Convert PDF to PNG

```bash
python -m src.utils.io pdf2png \
  --pdf data/input/plan.pdf \
  --out data/work/plan_600dpi.png \
  --dpi 600
```

#### 2. Run inference

```bash
python -m src.inference.infer \
  --image data/work/plan_600dpi.png \
  --scale 1:150 \
  --out build/out/floorplan.json
```

#### 3. Validate JSON

```bash
python -m src.utils.io validate \
  --json build/out/floorplan.json
```

#### 4. Generate Blender file

```bash
blender -b -P src/blender/json_to_blender.py -- \
  build/out/floorplan.json \
  build/out/building.blend \
  --wall_thickness 0.20 \
  --wall_height 2.80
```

## Docker Usage

### Build containers

```bash
cd docker
docker-compose build
```

### Run inference

```bash
docker-compose run inference
```

### Generate Blender file

```bash
docker-compose run blender
```

## Directory Structure

```
ml-plan2blend/
├── data/
│   ├── input/          # Place your PDF plans here
│   └── work/           # Processed images
├── build/
│   ├── out/            # Generated .blend/.glb files
│   └── reports/        # QA metrics and overlays
└── src/
    ├── inference/      # Main pipeline
    ├── blender/        # 3D generation
    └── training/       # ML training (placeholder)
```

## Next Steps

1. **Add your floor plans** to `data/input/`
2. **Run inference** on real architectural plans
3. **Annotate training data** using CVAT or Label Studio
4. **Train custom models** for your specific plan style
5. **Validate results** with QA metrics

## Common Issues

### PyMuPDF not found

```bash
pip install pymupdf
```

### OpenCV errors

```bash
pip install opencv-python opencv-contrib-python
```

### Blender not found

Download from https://www.blender.org/download/ and add to PATH.

### Import errors

Make sure you're running commands from the `ml-plan2blend/` directory.

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review the [Model Card](MODEL_CARD.md) for limitations and performance
- Run tests: `python -m pytest tests/ -v`
- Check example usage in `example_workflow.sh`

## Performance Tips

1. **High DPI**: Use 600+ DPI for best accuracy
2. **Clean scans**: Ensure high-contrast, clear plans
3. **Scale notation**: Include scale bar or text (e.g., "1:150")
4. **Preprocessing**: Remove unnecessary text/annotations before inference

## What's Next?

Once you have the basic pipeline working:

1. **Annotate data**: Create training dataset with CVAT
2. **Train models**: Implement actual ML training (currently placeholder)
3. **Fine-tune**: Adjust parameters for your specific building types
4. **Deploy**: Use Docker for production deployment
5. **Scale up**: Process multiple floors and buildings

Happy modeling! 🏗️
