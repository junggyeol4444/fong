"""Setup configuration for Auto Music Creator."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='auto-music-creator',
    version='1.0.0',
    author='Auto Music Creator Team',
    description='Automated music generation system using YouTube data and AI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/junggyeol4444/fong',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'yt-dlp>=2023.12.30',
        'youtube-transcript-api>=0.6.1',
        'beautifulsoup4>=4.12.2',
        'selenium>=4.15.2',
        'requests>=2.31.0',
        'librosa>=0.10.1',
        'music21>=9.1.0',
        'nltk>=3.8.1',
        'spacy>=3.7.2',
        'textblob>=0.17.1',
        'midiutil>=1.2.1',
        'numpy>=1.24.3',
        'pronouncing>=0.2.0',
        'TTS>=0.22.0',
        'pydub>=0.25.1',
        'soundfile>=0.12.1',
        'python-dotenv>=1.0.0',
        'pyyaml>=6.0.1',
        'tqdm>=4.66.1',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'music-creator=src.cli.main_cli:main',
        ],
    },
    include_package_data=True,
)
