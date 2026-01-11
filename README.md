# Auto Music Creator 🎵

An automated music generation system that creates original music using YouTube Music data, AI analysis, and synthesis.

## Overview

The Auto Music Creator is a comprehensive system designed to generate music automatically through five integrated phases:

1. **Crawling Module** - Collect music data from YouTube
2. **Analysis Module** - Extract patterns from lyrics and music
3. **Generation Engine** - Create original lyrics and MIDI music
4. **Voice Synthesis** - Generate singing voice
5. **Integration** - Combine everything into complete songs

## Features

### Phase 1: YouTube Music Crawler
- Download songs, metadata, and lyrics from YouTube
- Support for individual videos and entire playlists
- Progress tracking with automatic resume capability
- Duplicate detection to avoid re-downloading
- Multi-genre support

### Phase 2: Analysis Module
- **Lyrics Analysis:**
  - Extract common phrases and patterns
  - Identify rhyme schemes
  - Detect emotional keywords and sentiment
  - Analyze song structure

- **Music Analysis:**
  - Extract BPM (tempo)
  - Detect key signatures
  - Analyze chord progressions
  - Extract spectral and chroma features

### Phase 3: Generation Engine
- **Lyrics Generator:**
  - Multi-genre support (pop, rock, hip-hop)
  - Multiple rhyme schemes (AABB, ABAB, ABCB, free verse)
  - Theme-based generation
  - Multi-language support (MVP: English)

- **Music Generator:**
  - MIDI file generation
  - Genre-specific patterns
  - Customizable BPM, key, and duration
  - Chord progression generation

### Phase 4: Voice Synthesis
- Text-to-speech for singing
- Voice cloning from reference audio
- Audio mixing capabilities
- Complete song creation (lyrics + music + voice)

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for audio processing)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/junggyeol4444/fong.git
cd fong
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (first time only):
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

## Usage

The system provides a command-line interface with four main commands:

### 1. Crawl YouTube Music

Download a single video:
```bash
python music_creator.py crawl "https://www.youtube.com/watch?v=VIDEO_ID" --genre pop
```

Download a playlist:
```bash
python music_creator.py crawl "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --genre rock --max-count 10
```

Resume previous crawl:
```bash
python music_creator.py crawl "PLAYLIST_URL" --resume --genre pop
```

### 2. Analyze Music Data

Analyze lyrics:
```bash
python music_creator.py analyze lyrics data/raw/VIDEO_ID_lyrics.txt
```

Analyze music:
```bash
python music_creator.py analyze music data/raw/VIDEO_ID.mp3 --extract-chords
```

### 3. Generate Content

Generate lyrics:
```bash
python music_creator.py generate lyrics --genre pop --theme love --rhyme-scheme ABAB --num-verses 3
```

Generate music:
```bash
python music_creator.py generate music --genre rock --key D --bpm 140 --duration 64
```

### 4. Synthesize Voice

Synthesize lyrics to voice:
```bash
python music_creator.py synthesize lyrics --lyrics-file data/generated/pop_love_lyrics.txt
```

Create complete song:
```bash
python music_creator.py synthesize song --lyrics-file data/generated/lyrics.txt --midi-file data/generated/music.mid
```

Use voice cloning:
```bash
python music_creator.py synthesize lyrics --lyrics-file lyrics.txt --speaker-wav reference_voice.wav
```

## Project Structure

```
fong/
├── src/
│   ├── crawler/           # YouTube music crawler
│   │   └── youtube_crawler.py
│   ├── analysis/          # Lyrics and music analysis
│   │   ├── lyrics_analyzer.py
│   │   └── music_analyzer.py
│   ├── generation/        # Content generation
│   │   ├── lyrics_generator.py
│   │   └── music_generator.py
│   ├── voice_synthesis/   # Voice synthesis and audio mixing
│   │   └── voice_synthesizer.py
│   └── cli/              # Command-line interface
│       └── main_cli.py
├── data/
│   ├── raw/              # Downloaded music data
│   ├── analyzed/         # Analysis results
│   ├── generated/        # Generated content
│   └── templates/        # Lyric templates
├── music_creator.py      # Main entry point
├── requirements.txt      # Python dependencies
└── README.md
```

## Example Workflow

Complete workflow from data collection to song creation:

```bash
# 1. Collect music data
python music_creator.py crawl "PLAYLIST_URL" --playlist --genre pop --max-count 5

# 2. Analyze collected data
python music_creator.py analyze lyrics data/raw/VIDEO_ID_lyrics.txt
python music_creator.py analyze music data/raw/VIDEO_ID.mp3

# 3. Generate new content
python music_creator.py generate lyrics --genre pop --theme freedom --num-verses 2
python music_creator.py generate music --genre pop --key C --bpm 120

# 4. Create final song
python music_creator.py synthesize song \
  --lyrics-file data/generated/pop_freedom_lyrics.txt \
  --midi-file data/generated/pop_C_120bpm.mid
```

## Configuration

### Custom Lyric Templates

Create custom templates in `data/templates/lyric_templates.json`:

```json
{
  "custom_genre": {
    "structure": ["verse", "chorus", "verse", "chorus"],
    "themes": ["theme1", "theme2"],
    "vocabulary": {
      "theme1": ["word1", "word2", "word3"]
    }
  }
}
```

## Technical Details

### Dependencies
- **yt-dlp**: YouTube video/audio downloading
- **youtube-transcript-api**: Lyrics extraction
- **librosa**: Audio analysis
- **music21**: Music theory and analysis
- **NLTK/TextBlob**: Natural language processing
- **MIDIUtil**: MIDI file generation
- **TTS (Coqui)**: Voice synthesis
- **pydub**: Audio manipulation

### Limitations (MVP Version)
- Voice synthesis uses pre-trained models (custom training requires significant resources)
- MIDI to audio conversion requires external tools (FluidSynth, TiMidity++)
- English language only for lyrics generation
- Simplified chord detection and progression

## Development Timeline

This is an MVP (Minimum Viable Product) implementation covering all 5 phases:

- **Week 1-2**: Crawling module and data collection
- **Week 3**: Analysis module implementation
- **Week 4**: Generation engine development
- **Week 5**: Voice synthesis integration
- **Week 6-7**: Testing, optimization, and documentation

## Future Enhancements

- Multi-language lyrics generation
- Advanced chord progression detection
- Custom voice model training interface
- Web-based GUI
- Real-time generation
- Style transfer capabilities
- More genre templates
- Advanced mixing and mastering

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with open-source libraries and tools
- Inspired by various music generation research projects
- Uses pre-trained models from the Coqui TTS project

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example workflows

---

**Note**: This is an MVP implementation. Some features may require additional setup or external tools. See documentation for specific requirements.