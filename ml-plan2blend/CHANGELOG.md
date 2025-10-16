# Changelog

All notable changes to ML Plan2Blend will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Real ML model training implementation
- Curved wall support
- Multi-page PDF processing
- Web interface for easy usage
- Pre-trained model weights
- Extended test coverage
- Performance benchmarks

## [1.0.0] - 2025-10-16

### Added
- Initial release of ML Plan2Blend
- Complete project structure with modular architecture
- Core utility modules:
  - PDF to PNG conversion (600+ DPI)
  - Scale parsing and coordinate conversion
  - JSON I/O with validation
  - Comprehensive geometry utilities
- Inference pipeline:
  - End-to-end image to JSON conversion
  - Wall polygon extraction and vectorization
  - Door/window detection and projection
  - Room detection from closed regions
  - Orthogonalization and snap/merge
- Blender integration:
  - JSON to .blend conversion
  - Wall extrusion with proper thickness
  - Boolean cutters for doors/windows
  - Floor slab generation
  - Multi-floor support with collections
  - glTF export (.glb)
- QA and metrics:
  - IoU computation for segmentation
  - AP metrics for detection
  - Hausdorff distance calculation
  - Overlay visualization generation
  - Comprehensive metrics reporting
- Training infrastructure (placeholders):
  - Segmentation training script
  - Detection training script
  - Data augmentation strategies
- Testing:
  - 23 unit tests (geometry, vectorization, metrics)
  - 100% test pass rate
  - Integration test examples
- Docker support:
  - Training container
  - Blender container
  - Docker Compose orchestration
- Documentation:
  - Comprehensive README
  - Quick Start guide
  - Model Card with training details
  - Contributing guidelines
  - Example workflow script
- Example workflow demonstrating full pipeline

### Technical Details
- Python 3.10+ support
- PyTorch-ready architecture
- Blender 3.x+ compatible
- OpenCV-based image processing
- Shapely for geometry operations
- pytest for testing
- Type hints throughout

### Known Limitations
- Dummy ML models (placeholders for actual training)
- Basic wall detection (grid-based for demo)
- Simplified door/window projection
- No curved wall support in v1.0
- French building plans optimized

## [0.1.0] - 2025-10-16

### Added
- Project initialization
- Directory structure setup
- Basic module scaffolding

---

## Release Notes

### v1.0.0 - Initial Release

This is the first stable release of ML Plan2Blend, providing a complete framework for converting 2D architectural floor plans into 3D Blender models.

**Highlights:**
- ✅ Full inference pipeline (PDF → PNG → JSON → .blend/.glb)
- ✅ Modular architecture for easy extension
- ✅ Comprehensive test suite (23 tests)
- ✅ Docker support for reproducible deployment
- ✅ Detailed documentation and examples

**What Works:**
- PDF/PNG to structured JSON conversion
- Scale-aware coordinate transformation
- Wall polygon extraction and processing
- Blender 3D model generation
- Quality metrics computation

**What's Next (v1.1+):**
- Implement actual ML model training
- Add pre-trained weights
- Support curved walls
- Improve detection accuracy
- Add web interface
- Expand test coverage

**Installation:**
```bash
cd ml-plan2blend
pip install -r requirements.txt
bash example_workflow.sh
```

**Upgrade Path:**
This is the initial release. Future versions will maintain backward compatibility for the JSON schema.

---

For more details, see the [full documentation](README.md) and [Model Card](MODEL_CARD.md).
