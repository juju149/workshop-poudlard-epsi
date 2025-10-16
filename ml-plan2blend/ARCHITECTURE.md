# ML Plan2Blend Architecture

## Overview

ML Plan2Blend is a modular machine learning system that transforms 2D architectural floor plans into precise 3D Blender models. The architecture follows a pipeline design with clear separation of concerns.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  PDF/PNG Plans  →  Scale Detection  →  Preprocessing        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      ML INFERENCE LAYER                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐       ┌─────────────────────┐        │
│  │  Segmentation    │       │    Detection        │        │
│  │  (Walls)         │       │  (Doors/Windows)    │        │
│  │  - U-Net/HRNet   │       │  - YOLO/Faster RCNN │        │
│  │  - Output: Masks │       │  - Output: BBoxes   │        │
│  └──────────────────┘       └─────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  VECTORIZATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  Mask → Contours → Polygons → Snap/Merge → Orthogonalize   │
│                                                               │
│  - Skeletonization                                           │
│  - Polygonization                                            │
│  - Topology checking                                         │
│  - Scale conversion (pixels → meters)                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      JSON SCHEMA LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  {                                                            │
│    "scale": {...},                                           │
│    "floors": [                                               │
│      {                                                        │
│        "walls": [...],                                       │
│        "doors": [...],                                       │
│        "windows": [...],                                     │
│        "rooms": [...]                                        │
│      }                                                        │
│    ]                                                          │
│  }                                                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    3D GENERATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│  Blender (bpy)                                               │
│  - Create wall meshes (extrusion)                           │
│  - Apply boolean cutters (doors/windows)                    │
│  - Generate floor slabs                                     │
│  - Organize by collections                                  │
│  - Export .blend + .glb                                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                         QA LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  - IoU metrics (wall segmentation)                          │
│  - AP metrics (door/window detection)                       │
│  - Hausdorff distance (geometric accuracy)                  │
│  - Overlay visualization                                    │
└─────────────────────────────────────────────────────────────┘
```

## Module Architecture

### 1. Utils Module (`src/utils/`)

**Purpose**: Core utility functions shared across the system

**Components**:
- `io.py`: I/O operations
  - PDF to PNG conversion (PyMuPDF)
  - JSON loading/saving
  - Schema validation
  - Scale parsing
- `geometry.py`: Geometric operations
  - Polygon area/centroid
  - Point-in-polygon tests
  - Orthogonalization
  - Snap/merge operations
  - Self-intersection detection

**Dependencies**: NumPy, PyMuPDF, SciPy

### 2. Inference Module (`src/inference/`)

**Purpose**: ML inference and post-processing pipeline

**Components**:
- `infer.py`: Main pipeline orchestration
  - Image loading and preprocessing
  - ML model invocation
  - Coordinate transformation
  - JSON generation
- `vectorize.py`: Mask to vector conversion
  - Contour extraction
  - Polygon simplification
  - Wall segment detection
  - Door/window projection
  - Room detection
- `metrics.py`: QA and validation
  - IoU/Dice computation
  - AP calculation
  - Overlay generation
  - Report generation

**Dependencies**: OpenCV, scikit-image, NumPy

### 3. Blender Module (`src/blender/`)

**Purpose**: 3D model generation using Blender

**Components**:
- `json_to_blender.py`: Blender integration
  - Scene setup
  - Mesh creation from polygons
  - Wall extrusion
  - Boolean operations
  - Collection organization
  - Export to .blend/.glb

**Dependencies**: Blender (bpy), mathutils

### 4. Training Module (`src/training/`)

**Purpose**: ML model training infrastructure

**Components**:
- `train_segmentation.py`: Wall segmentation training
- `train_detection.py`: Door/window detection training
- `augments.py`: Data augmentation strategies

**Dependencies**: PyTorch, torchvision, albumentations

## Data Flow

### 1. Input Processing

```
PDF → [PyMuPDF] → PNG (600 DPI) → [Scale Detection] → Normalized Coordinates
```

### 2. ML Inference

```
PNG → [Segmentation Model] → Wall Mask
                           ↓
                    [Detection Model] → BBoxes (doors/windows)
```

### 3. Vectorization

```
Wall Mask → [Contour] → [Simplify] → [Orthogonalize] → Polygons
                                                            ↓
BBoxes → [Project onto walls] → Opening positions
```

### 4. JSON Schema

```json
{
  "scale": {"paper": 1, "real": 150},
  "floors": [
    {
      "code": "RDC",
      "walls": [{"poly": [[x,y], ...]}],
      "doors": [{"pos": [[x1,y1],[x2,y2]], "width": W}],
      "windows": [{"pos": [...], "width": W, "sill": H}],
      "rooms": [{"name": "...", "poly": [...], "area_m2": A}]
    }
  ]
}
```

### 5. 3D Generation

```
JSON → [Parse] → [Create Meshes] → [Boolean Ops] → .blend + .glb
```

## Design Patterns

### 1. Pipeline Pattern

Each module performs a specific transformation:
- Input → Preprocessing → Inference → Vectorization → 3D → Output

### 2. Strategy Pattern

Configurable algorithms:
- Segmentation model: U-Net, HRNet, Mask2Former
- Detection model: YOLO, Faster R-CNN
- Vectorization: Contour-based, skeleton-based

### 3. Builder Pattern

Complex object construction:
- Blender scene building
- JSON schema construction

### 4. Facade Pattern

Simplified interfaces:
- `infer_floorplan()` hides complex pipeline
- `create_floorplan_3d()` abstracts Blender operations

## Scalability Considerations

### Horizontal Scaling

- **Batch processing**: Process multiple floors in parallel
- **Distributed training**: Multi-GPU training support
- **Microservices**: Can be deployed as separate services

### Vertical Scaling

- **GPU acceleration**: ML inference on GPU
- **Memory optimization**: Tiling for large images
- **Caching**: Intermediate results caching

## Performance Characteristics

### Time Complexity

- **PDF → PNG**: O(pages)
- **Segmentation**: O(W×H) per image
- **Vectorization**: O(n) where n = contour points
- **Blender generation**: O(walls + openings)

### Space Complexity

- **Image storage**: ~50 MB per floor (600 DPI)
- **Model weights**: ~100-500 MB (segmentation + detection)
- **JSON output**: ~100 KB per floor
- **Blender file**: ~10-50 MB per building

## Error Handling

### Input Validation

- PDF existence and readability
- Scale string format
- Image quality checks
- JSON schema validation

### Runtime Errors

- Model inference failures → fallback to dummy
- Invalid polygons → skip with warning
- Boolean operation failures → retry with tolerance
- Missing dependencies → clear error messages

## Testing Strategy

### Unit Tests

- Geometry operations
- Coordinate transformations
- Polygon processing
- Metric calculations

### Integration Tests

- End-to-end pipeline
- JSON schema validation
- Blender integration

### Performance Tests

- Inference speed benchmarks
- Memory usage profiling
- Large file handling

## Extension Points

### Adding New Models

1. Implement model in `src/training/`
2. Add inference wrapper in `src/inference/`
3. Update configuration options

### Adding New Features

1. Extend JSON schema
2. Update vectorization pipeline
3. Modify Blender script
4. Add tests

### Custom Post-Processing

1. Extend `vectorize.py`
2. Add custom geometry operations
3. Update pipeline in `infer.py`

## Dependencies

### Core Dependencies

- **NumPy**: Numerical operations
- **OpenCV**: Image processing
- **SciPy**: Scientific computing
- **PyMuPDF**: PDF handling
- **Pillow**: Image I/O

### ML Dependencies

- **PyTorch**: Deep learning framework
- **torchvision**: Computer vision models
- **scikit-image**: Image processing algorithms

### 3D Dependencies

- **Blender (bpy)**: 3D modeling
- **mathutils**: Vector math

### Development Dependencies

- **pytest**: Testing framework
- **mypy**: Type checking
- **black**: Code formatting

## Configuration

### Environment Variables

- `ML_PLAN2BLEND_DATA`: Data directory path
- `ML_PLAN2BLEND_MODELS`: Model weights path
- `BLENDER_PATH`: Blender executable path

### Config Files

- `requirements.txt`: Python dependencies
- `docker-compose.yml`: Container orchestration
- `.gitignore`: Version control exclusions

## Deployment

### Local Deployment

```bash
pip install -r requirements.txt
bash example_workflow.sh
```

### Docker Deployment

```bash
docker-compose up
```

### Cloud Deployment

- Container registry: Push Docker images
- Kubernetes: Deploy with K8s manifests
- Serverless: AWS Lambda / Google Cloud Functions

## Monitoring

### Metrics to Track

- Inference time per floor
- Model accuracy (IoU, AP)
- Memory usage
- Error rates
- User feedback

### Logging

- Structured logging (JSON)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Output: stdout, file, cloud logging

---

For implementation details, see individual module documentation.
