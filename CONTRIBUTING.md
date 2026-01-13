# Contributing to Auto Music Creator

Thank you for your interest in contributing to Auto Music Creator! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages and logs

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test your changes: `python test_system.py`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fong.git
cd fong

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and small

## Testing

- Add tests for new features
- Ensure existing tests pass
- Run `python test_system.py` before submitting

## Documentation

- Update README.md for user-facing changes
- Update IMPLEMENTATION.md for technical changes
- Add examples to examples.json
- Include docstrings in code

## Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Write clear commit messages
- Update documentation
- Add tests if applicable
- Ensure all tests pass

## Areas for Contribution

### High Priority
- Multi-language support for lyrics
- Improved chord detection algorithms
- More genre templates
- Better voice synthesis integration

### Medium Priority
- Web interface
- Real-time generation
- Additional analysis features
- Performance optimizations

### Documentation
- Tutorial videos
- More examples
- Troubleshooting guide
- API documentation

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the project goals

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues/PRs

Thank you for contributing!
