# Implementation Details

## Project Overview

The Auto Music Creator is a comprehensive MVP system implementing all 5 phases of automated music generation:

- **Phase 1**: YouTube Music Crawler
- **Phase 2**: Analysis Module (Lyrics & Music)
- **Phase 3**: Generation Engine (Lyrics & Music)
- **Phase 4**: Voice Synthesis
- **Phase 5**: Integration & CLI

## Architecture

### Module Structure

```
src/
├── crawler/              - YouTube data collection
│   └── youtube_crawler.py (277 lines)
├── analysis/            - Data analysis
│   ├── lyrics_analyzer.py (268 lines)
│   └── music_analyzer.py (229 lines)
├── generation/          - Content generation
│   ├── lyrics_generator.py (366 lines)
│   └── music_generator.py (267 lines)
├── voice_synthesis/     - Voice & audio
│   └── voice_synthesizer.py (290 lines)
└── cli/                 - User interface
    └── main_cli.py (416 lines)
```

Total: ~1,800+ lines of production code

## Phase Implementation Details

### Phase 1: YouTube Music Crawler

**File**: `src/crawler/youtube_crawler.py`

**Key Features**:
- Downloads audio, metadata, and lyrics from YouTube
- Progress tracking with `progress.json`
- Duplicate detection
- Resume capability
- Playlist support

**Technologies**:
- `yt-dlp`: Video/audio downloading
- `youtube-transcript-api`: Lyrics extraction
- JSON: Progress persistence

**Usage**:
```bash
# Single video
python music_creator.py crawl "URL" --genre pop

# Playlist
python music_creator.py crawl "URL" --playlist --genre rock

# Resume
python music_creator.py crawl "URL" --resume
```

### Phase 2: Analysis Module

#### Lyrics Analysis
**File**: `src/analysis/lyrics_analyzer.py`

**Capabilities**:
- Common phrase extraction (n-grams)
- Rhyme pattern detection
- Sentiment analysis
- Emotional keyword extraction
- Structure analysis (verse/chorus detection)

**Output**: JSON files with:
- Word frequency
- Rhyme density
- Sentiment scores (polarity, subjectivity)
- Emotional themes
- Line/word counts

#### Music Analysis
**File**: `src/analysis/music_analyzer.py`

**Capabilities**:
- BPM (tempo) detection
- Key signature extraction
- Chord progression analysis
- Spectral feature extraction
- Chroma features for harmony

**Technologies**:
- `librosa`: Audio analysis
- NumPy: Numerical processing

**Output**: JSON files with:
- Tempo (BPM) and category
- Musical key and confidence
- Chroma distribution
- Spectral features (centroid, rolloff, MFCC)

### Phase 3: Generation Engine

#### Lyrics Generator
**File**: `src/generation/lyrics_generator.py`

**Features**:
- Multi-genre support (pop, rock, hip-hop)
- Theme-based generation
- Multiple rhyme schemes:
  - AABB (couplets)
  - ABAB (alternating)
  - ABCB (ballad)
  - FREE (free verse)
- Structured output (verse, chorus, bridge)

**Technology**:
- `pronouncing`: Rhyme detection
- Template-based generation
- Vocabulary mapping

**Genres Implemented**:
- Pop: Love, celebration, freedom
- Rock: Rebellion, power, struggle
- Hip-Hop: Success, ambition, street

#### Music Generator
**File**: `src/generation/music_generator.py`

**Features**:
- MIDI file generation
- Genre-specific patterns
- Customizable parameters:
  - BPM (tempo)
  - Key signature
  - Duration
  - Genre style

**Technologies**:
- `midiutil`: MIDI file creation
- Music theory algorithms

**Genres Implemented**:
- Pop: I-IV-V-I progression
- Rock: I-vi-IV-V progression
- Jazz: I-IV-ii-V progression
- Blues: 12-bar blues pattern

### Phase 4: Voice Synthesis

**File**: `src/voice_synthesis/voice_synthesizer.py`

**Features**:
- Text-to-speech for lyrics
- Voice cloning support
- Audio mixing (vocals + instrumental)
- Complete song creation pipeline

**Technologies**:
- `TTS` (Coqui): Voice synthesis
- `pydub`: Audio manipulation
- Pre-trained models

**Capabilities**:
- Synthesize vocals from lyrics
- Clone voice from reference audio
- Mix multiple audio tracks
- Export in various formats

### Phase 5: Integration & CLI

**File**: `src/cli/main_cli.py`

**Commands**:
1. `crawl`: Download music data
2. `analyze`: Analyze lyrics/music
3. `generate`: Create lyrics/music
4. `synthesize`: Generate vocals/songs

**Features**:
- Colored output (colorama)
- Progress feedback
- Error handling
- Help system
- Parameter validation

## Data Flow

```
1. Crawl → data/raw/
   ├── audio files (.mp3)
   ├── metadata (.json)
   └── lyrics (.txt)

2. Analyze → data/analyzed/
   ├── lyrics_analysis.json
   └── music_analysis.json

3. Generate → data/generated/
   ├── lyrics (.txt)
   └── music (.mid)

4. Synthesize → data/generated/
   ├── vocals (.wav)
   └── complete_song (.mp3)
```

## Configuration

### Lyric Templates

Location: `data/templates/lyric_templates.json`

Structure:
```json
{
  "genre": {
    "structure": ["verse", "chorus", ...],
    "themes": ["theme1", "theme2"],
    "vocabulary": {
      "theme1": ["word1", "word2", ...]
    }
  }
}
```

### Progress Tracking

Location: `progress.json` (auto-generated)

Tracks:
- Downloaded video IDs
- Failed downloads
- Statistics
- Last URL

## Dependencies

### Core Libraries
- **yt-dlp**: YouTube downloading
- **librosa**: Audio processing
- **NLTK**: Natural language processing
- **TTS**: Voice synthesis
- **midiutil**: MIDI generation

### Analysis
- **music21**: Music theory
- **textblob**: Sentiment analysis
- **spacy**: NLP

### Audio
- **pydub**: Audio manipulation
- **soundfile**: Audio I/O

## Testing

### Structure Verification
```bash
python verify_structure.py
```

### Full Test Suite
```bash
python test_system.py
```

Tests:
1. Module imports
2. Directory structure
3. Lyrics generation
4. Music generation
5. Lyrics analysis

## Limitations (MVP)

1. **Voice Training**: Full training not implemented, uses pre-trained models
2. **MIDI to Audio**: Requires external tools (FluidSynth, TiMidity++)
3. **Language**: English only (MVP)
4. **Chord Detection**: Simplified algorithm
5. **Voice Quality**: Depends on pre-trained model quality

## Future Enhancements

### Short-term
- Multi-language support
- More genre templates
- Advanced rhyme detection
- Better chord progression

### Long-term
- Custom voice model training
- Real-time generation
- Web interface
- Style transfer
- Collaborative filtering
- Advanced mixing/mastering

## Performance

### Expected Times
- Crawl single video: 30-60 seconds
- Analyze lyrics: < 1 second
- Analyze music: 5-10 seconds
- Generate lyrics: < 1 second
- Generate MIDI: < 1 second
- Synthesize voice: 10-30 seconds

### Resource Requirements
- Disk: 100MB per song (audio + data)
- RAM: 2GB minimum, 4GB recommended
- CPU: Multi-core recommended for analysis
- GPU: Optional, improves TTS speed

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Solution: `pip install -r requirements.txt`

2. **FFmpeg Not Found**
   - Solution: Install FFmpeg from system package manager

3. **TTS Model Download**
   - Solution: Ensure internet connection, models auto-download

4. **NLTK Data Missing**
   - Solution: Run NLTK download commands in README

5. **Permission Errors**
   - Solution: Check file permissions, run with appropriate user

## Code Quality

### Standards
- PEP 8 compliance
- Type hints where applicable
- Comprehensive docstrings
- Error handling
- Progress feedback

### Documentation
- README.md: User guide
- QUICKSTART.md: Quick start
- IMPLEMENTATION.md: Technical details
- Inline comments: Complex logic
- Examples: examples.json

## Maintenance

### Adding New Genres

1. Add template to `data/templates/lyric_templates.json`
2. Add progression to `MusicGenerator.genre_patterns`
3. Update CLI help text
4. Add examples to documentation

### Adding New Features

1. Create new module in appropriate package
2. Update `__init__.py` imports
3. Add CLI commands if needed
4. Update documentation
5. Add tests

## Security Considerations

1. **API Keys**: Not stored in code
2. **User Data**: Local storage only
3. **Downloads**: Validates URLs
4. **File Operations**: Safe path handling
5. **Dependencies**: Regularly updated

## License & Attribution

- MIT License
- Uses open-source libraries
- Pre-trained models: Coqui TTS
- Respects YouTube's terms of service

## Support & Contribution

### Getting Help
1. Check documentation
2. Review examples.json
3. Run test_system.py
4. Open GitHub issue

### Contributing
1. Fork repository
2. Create feature branch
3. Add tests
4. Update documentation
5. Submit pull request

---

**Version**: 1.0.0 (MVP)
**Date**: January 2026
**Status**: Production Ready (MVP)
