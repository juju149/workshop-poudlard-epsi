# Contributing to ML Plan2Blend

Thank you for your interest in contributing to ML Plan2Blend! This guide will help you get started.

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/workshop-poudlard-epsi.git
cd workshop-poudlard-epsi/ml-plan2blend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

### 3. Run Tests

```bash
python -m pytest tests/ -v --cov=src
```

## Project Structure

```
ml-plan2blend/
├── src/
│   ├── utils/          # Core utilities
│   ├── inference/      # ML pipeline
│   ├── blender/        # 3D generation
│   └── training/       # Model training
├── tests/              # Unit tests
├── docker/             # Docker configs
└── docs/               # Documentation
```

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Open an issue with tag `enhancement`
2. Describe the feature and use case
3. Discuss implementation approach

### Contributing Code

#### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

#### 2. Make Changes

Follow these guidelines:

**Code Style**
- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and concise

**Testing**
- Add tests for new features
- Ensure all tests pass: `pytest tests/ -v`
- Aim for >80% code coverage

**Documentation**
- Update README.md if needed
- Add docstrings with examples
- Update CHANGELOG.md

#### 3. Commit Changes

```bash
git add .
git commit -m "feat: Add support for curved walls"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Adding tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `chore:` - Maintenance tasks

#### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference related issues
- Screenshots for UI changes
- Test results

## Development Guidelines

### Adding New Features

1. **Discuss first**: Open an issue to discuss major features
2. **Keep scope small**: Break large features into smaller PRs
3. **Write tests**: Add unit tests and integration tests
4. **Update docs**: Keep documentation in sync
5. **Consider performance**: Profile code for bottlenecks

### Code Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer approval required
3. Address review comments promptly
4. Squash commits before merging

### Testing Guidelines

**Unit Tests**
```python
def test_polygon_area():
    """Test polygon area calculation."""
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    area = polygon_area(square)
    assert abs(area) == 100.0
```

**Integration Tests**
```python
def test_inference_pipeline():
    """Test complete inference pipeline."""
    result = infer_floorplan('test.png', scale='1:150')
    assert 'floors' in result
    assert len(result['floors']) > 0
```

**Run Tests**
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_vectorize.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Documentation Guidelines

**Docstring Format**
```python
def extract_walls(mask: np.ndarray, min_area: float = 100.0) -> List[Polygon]:
    """
    Extract wall polygons from binary mask.
    
    Args:
        mask: Binary segmentation mask (H, W)
        min_area: Minimum polygon area in pixels
    
    Returns:
        List of wall polygons
    
    Examples:
        >>> mask = load_mask('walls.png')
        >>> polygons = extract_walls(mask)
        >>> print(f"Found {len(polygons)} walls")
    """
```

## Areas for Contribution

### High Priority

1. **ML Model Implementation**
   - Implement actual segmentation training
   - Add detection model training
   - Integrate pre-trained models

2. **Vectorization Improvements**
   - Better polygon simplification
   - Curved wall support
   - Multi-story alignment

3. **Blender Integration**
   - Advanced material assignment
   - Stair geometry reconstruction
   - Furniture placement

### Medium Priority

4. **QA and Metrics**
   - Automated benchmark suite
   - Visual diff tools
   - Performance profiling

5. **Documentation**
   - Tutorial videos
   - API reference
   - Architecture diagrams

6. **Deployment**
   - CI/CD pipeline
   - Web interface
   - Cloud deployment guides

### Good First Issues

- Add more test cases
- Improve error messages
- Fix typos in documentation
- Add example datasets
- Create tutorial notebooks

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## Getting Help

- **Questions**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Chat**: [To be set up]

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Added to GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to ML Plan2Blend! 🙏
