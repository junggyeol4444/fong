"""Main CLI interface for Auto Music Creator system."""

import argparse
import sys
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

from src.crawler.youtube_crawler import YouTubeMusicCrawler
from src.analysis.lyrics_analyzer import LyricsAnalyzer
from src.analysis.music_analyzer import MusicAnalyzer
from src.generation.lyrics_generator import LyricsGenerator
from src.generation.music_generator import MusicGenerator
from src.voice_synthesis.voice_synthesizer import VoiceSynthesizer


def print_banner():
    """Print application banner."""
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
║      Auto Music Creator - MVP v1.0         ║
║   Automated Music Generation System        ║
╚════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def crawl_command(args):
    """Handle crawl command."""
    print(f"\n{Fore.YELLOW}Starting YouTube Music Crawler...{Style.RESET_ALL}")
    
    crawler = YouTubeMusicCrawler(
        output_dir=args.output_dir,
        progress_file=args.progress_file
    )
    
    if args.resume:
        print(f"{Fore.GREEN}Resuming from previous progress...{Style.RESET_ALL}")
        crawler.resume(args.url, genre=args.genre)
    elif args.playlist:
        crawler.crawl_playlist(
            args.url,
            genre=args.genre,
            max_count=args.max_count
        )
    else:
        result = crawler.download_song(args.url, genre=args.genre)
        if result:
            print(f"{Fore.GREEN}✓ Download successful{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ Download failed{Style.RESET_ALL}")
    
    # Show statistics
    stats = crawler.get_stats()
    print(f"\n{Fore.CYAN}Crawling Statistics:{Style.RESET_ALL}")
    print(f"  Total downloaded: {stats['total_downloaded']}")
    print(f"  Total failed: {stats['total_failed']}")


def analyze_command(args):
    """Handle analyze command."""
    print(f"\n{Fore.YELLOW}Starting Analysis...{Style.RESET_ALL}")
    
    if args.type == 'lyrics':
        analyzer = LyricsAnalyzer(output_dir=args.output_dir)
        
        lyrics_file = Path(args.input_file)
        if not lyrics_file.exists():
            print(f"{Fore.RED}Error: File not found: {args.input_file}{Style.RESET_ALL}")
            return
        
        print(f"Analyzing lyrics: {lyrics_file.name}")
        analysis = analyzer.analyze_file(lyrics_file)
        
        # Save analysis
        output_file = f"{lyrics_file.stem}_analysis.json"
        analyzer.save_analysis(analysis, output_file)
        
        # Print summary
        print(f"\n{Fore.CYAN}Analysis Summary:{Style.RESET_ALL}")
        print(f"  Lines: {analysis['line_count']}")
        print(f"  Words: {analysis['word_count']}")
        print(f"  Unique words: {analysis['unique_words']}")
        print(f"  Sentiment: {analysis['sentiment']['overall']}")
        print(f"  Rhyme pattern: {analysis['rhyme_pattern']['pattern']}")
        
    elif args.type == 'music':
        analyzer = MusicAnalyzer(output_dir=args.output_dir)
        
        audio_file = Path(args.input_file)
        if not audio_file.exists():
            print(f"{Fore.RED}Error: File not found: {args.input_file}{Style.RESET_ALL}")
            return
        
        print(f"Analyzing music: {audio_file.name}")
        analysis = analyzer.analyze_file(audio_file)
        
        if 'error' in analysis:
            print(f"{Fore.RED}Error: {analysis['error']}{Style.RESET_ALL}")
            return
        
        # Save analysis
        output_file = f"{audio_file.stem}_analysis.json"
        analyzer.save_analysis(analysis, output_file)
        
        # Print summary
        print(f"\n{Fore.CYAN}Music Analysis Summary:{Style.RESET_ALL}")
        print(f"  Duration: {analysis['duration']:.2f} seconds")
        print(f"  BPM: {analysis['bpm']['tempo']:.1f}")
        print(f"  Tempo: {analysis['bpm']['tempo_category']}")
        print(f"  Key: {analysis['key']['key']}")
        
        # Extract chord progression if requested
        if args.extract_chords:
            chords = analyzer.extract_chord_progression(audio_file)
            print(f"  Chord progression: {' - '.join(chords)}")


def generate_command(args):
    """Handle generate command."""
    print(f"\n{Fore.YELLOW}Starting Generation...{Style.RESET_ALL}")
    
    if args.type == 'lyrics':
        generator = LyricsGenerator()
        
        print(f"Generating {args.genre} lyrics with theme: {args.theme}")
        lyrics = generator.generate_lyrics(
            genre=args.genre,
            theme=args.theme,
            rhyme_scheme=args.rhyme_scheme,
            num_verses=args.num_verses,
            language=args.language
        )
        
        # Save lyrics
        output_file = f"{args.genre}_{args.theme}_lyrics.txt"
        generator.save_lyrics(lyrics, output_file, output_dir=args.output_dir)
        
        # Print preview
        print(f"\n{Fore.CYAN}Generated Lyrics Preview:{Style.RESET_ALL}")
        lines = lyrics.split('\n')
        for line in lines[:15]:  # Show first 15 lines
            print(f"  {line}")
        if len(lines) > 15:
            print(f"  ... ({len(lines) - 15} more lines)")
        
    elif args.type == 'music':
        generator = MusicGenerator(output_dir=args.output_dir)
        
        print(f"Generating {args.genre} music in key {args.key} at {args.bpm} BPM")
        output_file = generator.generate_midi(
            genre=args.genre,
            key=args.key,
            bpm=args.bpm,
            duration=args.duration
        )
        
        print(f"{Fore.GREEN}✓ MIDI file generated: {output_file}{Style.RESET_ALL}")
        
        # Show chord progression
        chords = generator.generate_chord_progression(args.key, args.genre)
        print(f"\n{Fore.CYAN}Chord Progression:{Style.RESET_ALL}")
        print(f"  {' → '.join(chords)}")


def synthesize_command(args):
    """Handle synthesize command."""
    print(f"\n{Fore.YELLOW}Starting Voice Synthesis...{Style.RESET_ALL}")
    
    synthesizer = VoiceSynthesizer(output_dir=args.output_dir)
    
    if args.action == 'lyrics':
        # Read lyrics from file
        lyrics_file = Path(args.lyrics_file)
        if not lyrics_file.exists():
            print(f"{Fore.RED}Error: Lyrics file not found: {args.lyrics_file}{Style.RESET_ALL}")
            return
        
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        
        output_file = f"vocals_{lyrics_file.stem}.wav"
        result = synthesizer.synthesize_lyrics(
            lyrics,
            output_file=output_file,
            speaker_wav=args.speaker_wav
        )
        
        if result:
            print(f"{Fore.GREEN}✓ Voice synthesis complete: {result}{Style.RESET_ALL}")
        
    elif args.action == 'song':
        # Create complete song
        lyrics_file = Path(args.lyrics_file)
        if not lyrics_file.exists():
            print(f"{Fore.RED}Error: Lyrics file not found: {args.lyrics_file}{Style.RESET_ALL}")
            return
        
        midi_file = Path(args.midi_file)
        if not midi_file.exists():
            print(f"{Fore.RED}Error: MIDI file not found: {args.midi_file}{Style.RESET_ALL}")
            return
        
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        
        output_file = f"song_{lyrics_file.stem}.mp3"
        result = synthesizer.create_complete_song(
            lyrics,
            str(midi_file),
            output_file=output_file,
            speaker_wav=args.speaker_wav
        )
        
        if result:
            print(f"{Fore.GREEN}✓ Complete song created: {result}{Style.RESET_ALL}")
    
    elif args.action == 'train':
        print(f"{Fore.YELLOW}Setting up voice model training...{Style.RESET_ALL}")
        synthesizer.train_voice_model(
            args.training_data_dir,
            args.model_output_dir
        )


def main():
    """Main CLI entry point."""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Auto Music Creator - Automated music generation system',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl YouTube Music for data')
    crawl_parser.add_argument('url', help='YouTube video or playlist URL')
    crawl_parser.add_argument('--genre', default=None, help='Genre tag for organization')
    crawl_parser.add_argument('--playlist', action='store_true', help='Crawl entire playlist')
    crawl_parser.add_argument('--resume', action='store_true', help='Resume from last progress')
    crawl_parser.add_argument('--max-count', type=int, default=None, help='Max videos to download')
    crawl_parser.add_argument('--output-dir', default='data/raw', help='Output directory')
    crawl_parser.add_argument('--progress-file', default='progress.json', help='Progress file path')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze lyrics or music files')
    analyze_parser.add_argument('type', choices=['lyrics', 'music'], help='Type of analysis')
    analyze_parser.add_argument('input_file', help='Input file to analyze')
    analyze_parser.add_argument('--output-dir', default='data/analyzed', help='Output directory')
    analyze_parser.add_argument('--extract-chords', action='store_true', help='Extract chord progression (music only)')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate lyrics or music')
    generate_parser.add_argument('type', choices=['lyrics', 'music'], help='Type of generation')
    generate_parser.add_argument('--genre', default='pop', help='Music genre')
    generate_parser.add_argument('--theme', default='love', help='Lyrics theme (lyrics only)')
    generate_parser.add_argument('--rhyme-scheme', default='ABAB', choices=['AABB', 'ABAB', 'ABCB', 'FREE'], help='Rhyme scheme (lyrics only)')
    generate_parser.add_argument('--num-verses', type=int, default=2, help='Number of verses (lyrics only)')
    generate_parser.add_argument('--language', default='en', help='Language code (lyrics only)')
    generate_parser.add_argument('--key', default='C', help='Musical key (music only)')
    generate_parser.add_argument('--bpm', type=int, default=120, help='Beats per minute (music only)')
    generate_parser.add_argument('--duration', type=int, default=32, help='Duration in beats (music only)')
    generate_parser.add_argument('--output-dir', default='data/generated', help='Output directory')
    
    # Synthesize command
    synthesize_parser = subparsers.add_parser('synthesize', help='Synthesize voice and create songs')
    synthesize_parser.add_argument('action', choices=['lyrics', 'song', 'train'], help='Synthesis action')
    synthesize_parser.add_argument('--lyrics-file', help='Lyrics file path')
    synthesize_parser.add_argument('--midi-file', help='MIDI file path (for song creation)')
    synthesize_parser.add_argument('--speaker-wav', default=None, help='Speaker reference WAV file for voice cloning')
    synthesize_parser.add_argument('--output-dir', default='data/generated', help='Output directory')
    synthesize_parser.add_argument('--training-data-dir', help='Training data directory (for train action)')
    synthesize_parser.add_argument('--model-output-dir', help='Model output directory (for train action)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'crawl':
            crawl_command(args)
        elif args.command == 'analyze':
            analyze_command(args)
        elif args.command == 'generate':
            generate_command(args)
        elif args.command == 'synthesize':
            synthesize_command(args)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
