"""Lyrics generation with multi-genre and multi-language support."""

import json
import random
import re
from pathlib import Path
from typing import Dict, List, Optional
import pronouncing


class LyricsGenerator:
    """Generate lyrics based on genre, theme, and learned patterns."""
    
    def __init__(self, templates_dir: str = "data/templates"):
        """Initialize the Lyrics Generator.
        
        Args:
            templates_dir: Directory containing lyric templates
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates = self._load_templates()
        self.rhyme_schemes = {
            'AABB': self._generate_aabb,
            'ABAB': self._generate_abab,
            'ABCB': self._generate_abcb,
            'FREE': self._generate_free_verse
        }
    
    def _load_templates(self) -> Dict:
        """Load lyric templates from file."""
        template_file = self.templates_dir / "lyric_templates.json"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default templates
        return self._create_default_templates()
    
    def _create_default_templates(self) -> Dict:
        """Create default lyric templates."""
        templates = {
            'pop': {
                'structure': ['verse', 'chorus', 'verse', 'chorus', 'bridge', 'chorus'],
                'themes': ['love', 'heartbreak', 'celebration', 'freedom'],
                'vocabulary': {
                    'love': ['heart', 'soul', 'forever', 'together', 'dance', 'night'],
                    'heartbreak': ['tears', 'alone', 'goodbye', 'memories', 'rain', 'cold'],
                    'celebration': ['party', 'shine', 'bright', 'high', 'free', 'wild'],
                    'freedom': ['fly', 'dreams', 'sky', 'open', 'road', 'endless']
                }
            },
            'rock': {
                'structure': ['verse', 'chorus', 'verse', 'chorus', 'solo', 'chorus'],
                'themes': ['rebellion', 'power', 'struggle', 'freedom'],
                'vocabulary': {
                    'rebellion': ['fight', 'rise', 'rebel', 'break', 'chains', 'fire'],
                    'power': ['strong', 'thunder', 'lightning', 'roar', 'storm', 'force'],
                    'struggle': ['battle', 'survive', 'climb', 'struggle', 'push', 'fight'],
                    'freedom': ['free', 'wild', 'untamed', 'open', 'road', 'run']
                }
            },
            'hip_hop': {
                'structure': ['verse', 'hook', 'verse', 'hook', 'verse', 'hook'],
                'themes': ['success', 'struggle', 'street', 'ambition'],
                'vocabulary': {
                    'success': ['win', 'top', 'crown', 'gold', 'shine', 'rise'],
                    'struggle': ['grind', 'hustle', 'climb', 'fight', 'survive', 'push'],
                    'street': ['block', 'city', 'streets', 'hood', 'concrete', 'real'],
                    'ambition': ['dream', 'goal', 'strive', 'achieve', 'reach', 'vision']
                }
            }
        }
        
        # Save default templates
        template_file = self.templates_dir / "lyric_templates.json"
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(templates, indent=2, fp=f)
        
        return templates
    
    def generate_lyrics(self, genre: str = 'pop', theme: str = 'love', 
                       rhyme_scheme: str = 'ABAB', num_verses: int = 2,
                       language: str = 'en') -> str:
        """Generate lyrics based on parameters.
        
        Args:
            genre: Music genre (pop, rock, hip_hop)
            theme: Theme/topic for lyrics
            rhyme_scheme: Rhyme pattern (AABB, ABAB, ABCB, FREE)
            num_verses: Number of verses to generate
            language: Language code (currently only 'en' supported)
            
        Returns:
            Generated lyrics as string
        """
        if genre not in self.templates:
            genre = 'pop'
        
        template = self.templates[genre]
        
        # Get vocabulary for theme
        if theme not in template['vocabulary']:
            theme = list(template['vocabulary'].keys())[0]
        
        vocab = template['vocabulary'][theme]
        
        # Generate structure
        structure = template['structure'][:num_verses * 2 + 1]
        
        lyrics_parts = []
        
        for section in structure:
            if section == 'verse':
                lines = self._generate_verse(vocab, rhyme_scheme)
                lyrics_parts.append(f"[Verse]\n{lines}\n")
            elif section == 'chorus' or section == 'hook':
                lines = self._generate_chorus(vocab, theme)
                lyrics_parts.append(f"[Chorus]\n{lines}\n")
            elif section == 'bridge':
                lines = self._generate_bridge(vocab)
                lyrics_parts.append(f"[Bridge]\n{lines}\n")
            elif section == 'solo':
                lyrics_parts.append("[Instrumental Solo]\n")
        
        return '\n'.join(lyrics_parts)
    
    def _generate_verse(self, vocab: List[str], rhyme_scheme: str) -> str:
        """Generate a verse with specified rhyme scheme.
        
        Args:
            vocab: Vocabulary list
            rhyme_scheme: Rhyme pattern
            
        Returns:
            Verse lyrics
        """
        generator = self.rhyme_schemes.get(rhyme_scheme, self._generate_abab)
        return generator(vocab, num_lines=4)
    
    def _generate_chorus(self, vocab: List[str], theme: str) -> str:
        """Generate a chorus/hook.
        
        Args:
            vocab: Vocabulary list
            theme: Theme word
            
        Returns:
            Chorus lyrics
        """
        # Chorus is usually repetitive and catchy
        words = random.sample(vocab, min(3, len(vocab)))
        
        lines = [
            f"{theme.capitalize()} in the {words[0]}",
            f"Can you feel the {words[1]}",
            f"{theme.capitalize()} in the {words[0]}",
            f"Never gonna let it {words[2] if len(words) > 2 else 'go'}"
        ]
        
        return '\n'.join(lines)
    
    def _generate_bridge(self, vocab: List[str]) -> str:
        """Generate a bridge section.
        
        Args:
            vocab: Vocabulary list
            
        Returns:
            Bridge lyrics
        """
        words = random.sample(vocab, min(4, len(vocab)))
        
        lines = [
            f"And when the {words[0]} fades away",
            f"I'll be here, come what may"
        ]
        
        return '\n'.join(lines)
    
    def _generate_aabb(self, vocab: List[str], num_lines: int = 4) -> str:
        """Generate AABB rhyme scheme.
        
        Args:
            vocab: Vocabulary list
            num_lines: Number of lines
            
        Returns:
            Lines with AABB rhyme
        """
        lines = []
        words_used = []
        
        for i in range(0, num_lines, 2):
            word1 = random.choice([w for w in vocab if w not in words_used])
            words_used.append(word1)
            
            # Find rhyme for word1
            rhymes = pronouncing.rhymes(word1)
            word2 = rhymes[0] if rhymes else word1
            
            lines.append(f"Dancing through the {word1} tonight")
            lines.append(f"Everything just feels so {word2}")
        
        return '\n'.join(lines)
    
    def _generate_abab(self, vocab: List[str], num_lines: int = 4) -> str:
        """Generate ABAB rhyme scheme.
        
        Args:
            vocab: Vocabulary list
            num_lines: Number of lines
            
        Returns:
            Lines with ABAB rhyme
        """
        if len(vocab) < 2:
            vocab = vocab + ['night', 'day', 'way', 'light']
        
        word_a = random.choice(vocab)
        word_b = random.choice([w for w in vocab if w != word_a])
        
        rhymes_a = pronouncing.rhymes(word_a)
        rhymes_b = pronouncing.rhymes(word_b)
        
        rhyme_a = rhymes_a[0] if rhymes_a else word_a
        rhyme_b = rhymes_b[0] if rhymes_b else word_b
        
        lines = [
            f"Walking down this empty {word_a}",
            f"Feeling like I've lost my {word_b}",
            f"Looking for a brand new {rhyme_a}",
            f"Hoping I can find my {rhyme_b}"
        ]
        
        return '\n'.join(lines)
    
    def _generate_abcb(self, vocab: List[str], num_lines: int = 4) -> str:
        """Generate ABCB rhyme scheme.
        
        Args:
            vocab: Vocabulary list
            num_lines: Number of lines
            
        Returns:
            Lines with ABCB rhyme
        """
        if len(vocab) < 3:
            vocab = vocab + ['night', 'day', 'way', 'light', 'time', 'free']
        
        word_a = random.choice(vocab)
        word_b = random.choice([w for w in vocab if w != word_a])
        word_c = random.choice([w for w in vocab if w not in [word_a, word_b]])
        
        rhymes_b = pronouncing.rhymes(word_b)
        rhyme_b = rhymes_b[0] if rhymes_b else word_b
        
        lines = [
            f"Standing in the {word_a}",
            f"Waiting for the {word_b}",
            f"Thinking about the {word_c}",
            f"Everything feels {rhyme_b}"
        ]
        
        return '\n'.join(lines)
    
    def _generate_free_verse(self, vocab: List[str], num_lines: int = 4) -> str:
        """Generate free verse (no rhyme scheme).
        
        Args:
            vocab: Vocabulary list
            num_lines: Number of lines
            
        Returns:
            Free verse lines
        """
        patterns = [
            "Walking through the {0}",
            "I can feel the {0}",
            "Lost in the {0}",
            "Running to the {0}",
            "Searching for the {0}",
            "Dancing in the {0}"
        ]
        
        lines = []
        for _ in range(num_lines):
            word = random.choice(vocab)
            pattern = random.choice(patterns)
            lines.append(pattern.format(word))
        
        return '\n'.join(lines)
    
    def save_lyrics(self, lyrics: str, output_file: str, output_dir: str = "data/generated"):
        """Save generated lyrics to file.
        
        Args:
            lyrics: Generated lyrics text
            output_file: Output filename
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / output_file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(lyrics)
        
        print(f"Lyrics saved to {file_path}")
