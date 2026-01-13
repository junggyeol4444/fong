# Quick Start Guide

## Installation

### Option 1: Easy Installation (Recommended)

**For Linux/Mac:**
```bash
# 1. Clone the repository
git clone https://github.com/junggyeol4444/fong.git
cd fong

# 2. Run installation script
./install.sh
```

**For Windows:**
```cmd
REM 1. Clone the repository
git clone https://github.com/junggyeol4444/fong.git
cd fong

REM 2. Run installation script
install.bat
```

The installation script will automatically set up everything for you!

### Option 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/junggyeol4444/fong.git
cd fong

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

## Quick Test

### Using Executable Scripts (Easiest)

**For Linux/Mac:**
```bash
# Generate lyrics
./music-creator.sh generate lyrics --genre pop --theme love --num-verses 2

# Generate music
./music-creator.sh generate music --genre pop --key C --bpm 120
```

**For Windows:**
```cmd
REM Generate lyrics
music-creator.bat generate lyrics --genre pop --theme love --num-verses 2

REM Generate music
music-creator.bat generate music --genre pop --key C --bpm 120
```

### Using Python Directly

### 1. Generate Lyrics (No external dependencies)

```bash
python music_creator.py generate lyrics --genre pop --theme love --num-verses 2
```

Output: `data/generated/pop_love_lyrics.txt`

### 2. Generate Music (No external dependencies)

```bash
python music_creator.py generate music --genre pop --key C --bpm 120
```

Output: `data/generated/pop_C_120bpm.mid`

### 3. Analyze Lyrics (If you have a lyrics file)

```bash
# Create a sample lyrics file first
echo "Love is in the air
Dancing without care
Hearts are everywhere
This moment we share" > test_lyrics.txt

python music_creator.py analyze lyrics test_lyrics.txt
```

Output: `data/analyzed/test_lyrics_analysis.json`

## Full Workflow Example

```bash
# Step 1: Generate lyrics for a pop song about freedom
python music_creator.py generate lyrics --genre pop --theme freedom --rhyme-scheme ABAB --num-verses 2

# Step 2: Generate corresponding music
python music_creator.py generate music --genre pop --key C --bpm 120 --duration 32

# Step 3: Check generated files
ls -la data/generated/

# Step 4 (Optional): Synthesize voice if TTS is working
python music_creator.py synthesize lyrics --lyrics-file data/generated/pop_freedom_lyrics.txt
```

## Testing Individual Modules

### Test Lyrics Generator

```python
from src.generation.lyrics_generator import LyricsGenerator

generator = LyricsGenerator()
lyrics = generator.generate_lyrics(genre='pop', theme='love', rhyme_scheme='ABAB')
print(lyrics)
```

### Test Music Generator

```python
from src.generation.music_generator import MusicGenerator

generator = MusicGenerator()
midi_file = generator.generate_midi(genre='rock', key='D', bpm=140)
print(f"Generated: {midi_file}")
```

### Test Lyrics Analyzer

```python
from src.analysis.lyrics_analyzer import LyricsAnalyzer

analyzer = LyricsAnalyzer()
analysis = analyzer.analyze_text("Your lyrics here...")
print(analysis)
```

## Common Issues

### Issue: Import errors
**Solution**: Make sure you're in the project root directory and have installed all dependencies.

### Issue: TTS model download fails
**Solution**: This is normal on first run. The system will download models automatically. Ensure you have internet connection and sufficient disk space.

### Issue: FFmpeg not found
**Solution**: Install FFmpeg:
- Ubuntu/Debian: `sudo apt-get install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: Download from ffmpeg.org

### Issue: MIDI file won't play
**Solution**: Use a MIDI player or convert to audio:
- Online: Upload to https://www.onlineconverter.com/midi-to-mp3
- Command line: `timidity file.mid -Ow -o file.wav`

## Next Steps

1. Read the full README.md for detailed documentation
2. Check examples.json for more usage examples
3. Customize lyric templates in data/templates/
4. Explore the source code in src/ directory

## Support

If you encounter issues:
1. Check this guide first
2. Review the main README.md
3. Open an issue on GitHub with error details
