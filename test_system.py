#!/usr/bin/env python3
"""Test script to verify Auto Music Creator installation and basic functionality."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import init, Fore, Style
init(autoreset=True)


def test_imports():
    """Test if all required modules can be imported."""
    print(f"\n{Fore.CYAN}Testing module imports...{Style.RESET_ALL}")
    
    modules = [
        ('Crawler', 'src.crawler.youtube_crawler', 'YouTubeMusicCrawler'),
        ('Lyrics Analyzer', 'src.analysis.lyrics_analyzer', 'LyricsAnalyzer'),
        ('Music Analyzer', 'src.analysis.music_analyzer', 'MusicAnalyzer'),
        ('Lyrics Generator', 'src.generation.lyrics_generator', 'LyricsGenerator'),
        ('Music Generator', 'src.generation.music_generator', 'MusicGenerator'),
        ('Voice Synthesizer', 'src.voice_synthesis.voice_synthesizer', 'VoiceSynthesizer'),
    ]
    
    success = True
    for name, module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {name}")
        except Exception as e:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} {name}: {str(e)}")
            success = False
    
    return success


def test_lyrics_generation():
    """Test lyrics generation functionality."""
    print(f"\n{Fore.CYAN}Testing lyrics generation...{Style.RESET_ALL}")
    
    try:
        from src.generation.lyrics_generator import LyricsGenerator
        
        generator = LyricsGenerator()
        lyrics = generator.generate_lyrics(
            genre='pop',
            theme='love',
            rhyme_scheme='ABAB',
            num_verses=1
        )
        
        if lyrics and len(lyrics) > 0:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Lyrics generated successfully")
            print(f"\n  Preview (first 200 chars):")
            print(f"  {lyrics[:200]}...")
            return True
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} Generated lyrics is empty")
            return False
            
    except Exception as e:
        print(f"  {Fore.RED}✗{Style.RESET_ALL} Error: {str(e)}")
        return False


def test_music_generation():
    """Test MIDI music generation."""
    print(f"\n{Fore.CYAN}Testing music generation...{Style.RESET_ALL}")
    
    midi_file = None
    try:
        from src.generation.music_generator import MusicGenerator
        import os
        
        generator = MusicGenerator(output_dir='data/generated')
        midi_file = generator.generate_midi(
            genre='pop',
            key='C',
            bpm=120,
            duration=16,
            output_file='test_song.mid'
        )
        
        if os.path.exists(midi_file):
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} MIDI file generated successfully")
            print(f"  Location: {midi_file}")
            return True
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} MIDI file not created")
            return False
            
    except Exception as e:
        print(f"  {Fore.RED}✗{Style.RESET_ALL} Error: {str(e)}")
        return False
    finally:
        # Clean up test file
        if midi_file and os.path.exists(midi_file):
            try:
                os.remove(midi_file)
                print(f"  Test file cleaned up")
            except Exception:
                pass


def test_lyrics_analysis():
    """Test lyrics analysis functionality."""
    print(f"\n{Fore.CYAN}Testing lyrics analysis...{Style.RESET_ALL}")
    
    try:
        from src.analysis.lyrics_analyzer import LyricsAnalyzer
        
        analyzer = LyricsAnalyzer()
        test_lyrics = """
        Walking down this empty road
        Feeling like I've lost my way
        Looking for a new abode
        Hoping for a brighter day
        """
        
        analysis = analyzer.analyze_text(test_lyrics)
        
        if analysis and 'line_count' in analysis:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Lyrics analysis successful")
            print(f"  Lines: {analysis['line_count']}")
            print(f"  Words: {analysis['word_count']}")
            print(f"  Sentiment: {analysis['sentiment']['overall']}")
            return True
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} Analysis incomplete")
            return False
            
    except Exception as e:
        print(f"  {Fore.RED}✗{Style.RESET_ALL} Error: {str(e)}")
        return False


def test_directory_structure():
    """Test if required directories exist."""
    print(f"\n{Fore.CYAN}Testing directory structure...{Style.RESET_ALL}")
    
    dirs = [
        'src/crawler',
        'src/analysis',
        'src/generation',
        'src/voice_synthesis',
        'src/cli',
        'data/raw',
        'data/analyzed',
        'data/generated',
        'data/templates'
    ]
    
    success = True
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {dir_path}")
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} {dir_path} (missing)")
            success = False
    
    return success


def main():
    """Run all tests."""
    print(f"{Fore.CYAN}╔════════════════════════════════════════════╗")
    print(f"║   Auto Music Creator - Test Suite         ║")
    print(f"╚════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    results = []
    
    # Run tests
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Module Imports", test_imports()))
    results.append(("Lyrics Generation", test_lyrics_generation()))
    results.append(("Music Generation", test_music_generation()))
    results.append(("Lyrics Analysis", test_lyrics_analysis()))
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Test Summary:{Style.RESET_ALL}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"  {name}: {status}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"{Fore.GREEN}✓ All tests passed! System is ready to use.{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.YELLOW}⚠ Some tests failed. Check errors above.{Style.RESET_ALL}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
