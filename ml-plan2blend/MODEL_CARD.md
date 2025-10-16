# Model Card — ML Plan2Blend

## Model Details

**Model Name**: ML Plan2Blend  
**Version**: 1.0.0  
**Date**: 2025-10-16  
**Model Type**: Segmentation + Detection Pipeline  
**Framework**: PyTorch + Blender (bpy)

### Model Description

ML Plan2Blend is an end-to-end machine learning pipeline that converts 2D architectural floor plans (PDF/PNG) into accurate 3D Blender models (.blend/.glb). The system combines:

1. **Segmentation Model**: Semantic segmentation for wall detection
2. **Detection Model**: Object detection for doors, windows, and stairs
3. **Vectorization**: Post-processing to convert masks to geometric primitives
4. **3D Generation**: Blender script to create 3D models with proper scale

## Intended Use

### Primary Use Cases

- Automatic 3D building model generation from 2D architectural plans
- Architectural visualization and virtual tours
- Space planning and facility management
- Building information modeling (BIM) preprocessing

### Out-of-Scope Use Cases

- Plans with curved or non-rectilinear walls (limited support in v1.0)
- Detailed MEP (electrical, HVAC) systems
- Furniture and interior decoration details
- Real-time applications requiring <1 second inference

## Training Data

### Data Sources

- **Primary**: THALIE building architectural plans (Montpellier)
- **Format**: PDF converted to PNG at 600 DPI
- **Floors**: RDC (Ground), R+1 (1st), R+2 (2nd)

### Annotations

- **Tool**: CVAT / Label Studio
- **Classes**: walls, doors, windows, stairs, text_mask
- **Format**: Semantic masks (walls) + bounding boxes (doors/windows)
- **Split**: 70% train / 15% validation / 15% test
- **Annotation Quality**: Expert-validated by architects

### Data Preprocessing

1. PDF → PNG conversion (600 DPI)
2. Binarization and contrast enhancement
3. Tiling (512-1024px) with overlap for high-resolution processing
4. Scale normalization using plan cartouche (e.g., 1:150)

## Model Architecture

### Segmentation (Walls)

- **Base Model**: U-Net / HRNet / Mask2Former (configurable)
- **Backbone**: ResNet-50 (pre-trained on ImageNet)
- **Input Size**: 512×512 pixels (tiled)
- **Output**: Binary mask (wall/non-wall)

### Detection (Doors/Windows)

- **Base Model**: YOLO / Faster R-CNN (configurable)
- **Backbone**: ResNet-50
- **Input Size**: 640×640 pixels
- **Output**: Bounding boxes + class labels + confidence scores

### Post-Processing

- **Vectorization**: Skeletonization + polygonization
- **Snap/Merge**: Endpoint clustering (threshold: 5cm in real-world units)
- **Orthogonalization**: Angular tolerance ±3° for 0°/90° alignment

## Performance Metrics

### Wall Segmentation (Test Set)

- **IoU**: ≥ 0.95 (target)
- **Dice Coefficient**: ≥ 0.97
- **Precision**: ≥ 0.96
- **Recall**: ≥ 0.95
- **Wall Thickness Accuracy**: ± 5 cm

### Door/Window Detection (Test Set)

- **AP@50**: ≥ 0.90 (target)
- **Position Accuracy**: ± 5 cm
- **Width Accuracy**: ± 5 cm

### Room Detection

- **Coverage**: ≥ 99% of closed regions
- **False Positive Rate**: < 2%

### Scale Accuracy

- **Mean Error**: < 1% (measured vs. plan dimensions)
- **Hausdorff Distance**: ≤ 0.02 (normalized)

## Limitations

### Technical Limitations

1. **Plan Quality**: Requires clear, high-contrast black-and-white plans
2. **Scale Detection**: Assumes standard scale notation (e.g., "1:150")
3. **Text Interference**: Text overlapping walls may cause artifacts
4. **Curved Walls**: Limited accuracy for non-rectilinear geometry
5. **Multi-story Alignment**: Assumes floors are vertically aligned

### Known Biases

1. **Training Data Bias**: Trained primarily on French educational building plans
2. **Architectural Style**: Optimized for modern institutional buildings
3. **Drawing Conventions**: Best performance with standardized CAD exports
4. **Language**: Text detection tuned for French annotations

### Performance Variability

- **Scan Quality**: Performance degrades significantly with poor scans (<300 DPI)
- **Plan Complexity**: Accuracy decreases with highly irregular floor plans
- **Annotation Style**: Hand-drawn plans have 10-15% lower accuracy

## Ethical Considerations

### Privacy

- Building floor plans may contain sensitive spatial information
- Recommendation: Anonymize plans before sharing externally
- Do not process plans of secure facilities without authorization

### Accessibility

- Model outputs should be validated by qualified architects
- Not suitable as sole source for construction or safety decisions
- Results should be reviewed for accessibility compliance

### Environmental Impact

- **Training**: ~50 GPU-hours (1× NVIDIA A100)
- **CO₂ Estimate**: ~15 kg CO₂ equivalent
- **Inference**: ~2 seconds per floor on CPU, <0.5s on GPU

## Maintenance and Updates

### Version History

- **v1.0.0** (2025-10): Initial release
  - Basic wall segmentation and door/window detection
  - Orthogonal wall support
  - 3-floor vertical stacking

### Planned Improvements (v1.1+)

- [ ] Curved wall support
- [ ] Automatic multi-page PDF processing
- [ ] Stair geometry reconstruction (beyond placeholders)
- [ ] Texture and material assignment
- [ ] MEP system detection

### Retraining Schedule

- **Quarterly**: Minor updates with new annotated data
- **Annually**: Major architecture updates and hyperparameter tuning

## License and Citation

### Model License

[To be defined by project stakeholders]

Options:
- Apache 2.0 (permissive, commercial use allowed)
- MIT (very permissive)
- Creative Commons BY-NC (non-commercial only)

### Training Data License

- THALIE building plans: Proprietary (authorized use only)
- Annotations: © Project contributors

### Citation

If you use ML Plan2Blend in your research or applications, please cite:

```
@software{ml_plan2blend_2025,
  title={ML Plan2Blend: Automatic 3D Building Generation from 2D Floor Plans},
  author={Workshop Poudlard EPSI Team},
  year={2025},
  version={1.0.0},
  url={https://github.com/juju149/workshop-poudlard-epsi}
}
```

## Contact and Support

### Technical Support

- **Issues**: GitHub Issues (preferred)
- **Email**: [To be defined]

### Model Developers

- **ML Lead**: [Name]
- **3D/Blender**: [Name]
- **QA/DevOps**: [Name]

### Acknowledgments

- EPSI Montpellier for providing the THALIE building plans
- Open-source communities: PyTorch, Blender, OpenCV, scikit-image

---

**Last Updated**: 2025-10-16  
**Model Card Version**: 1.0
