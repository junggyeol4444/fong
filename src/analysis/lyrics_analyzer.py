"""Lyrics text analysis for extracting patterns and emotional content."""

import json
import re
from pathlib import Path
from typing import Dict, List, Set
from collections import Counter
import nltk
from textblob import TextBlob

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)


class LyricsAnalyzer:
    """Analyze lyrics for patterns, themes, and emotional content."""
    
    def __init__(self, output_dir: str = "data/analyzed"):
        """Initialize the Lyrics Analyzer.
        
        Args:
            output_dir: Directory to save analysis results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_file(self, lyrics_file: Path) -> Dict:
        """Analyze a single lyrics file.
        
        Args:
            lyrics_file: Path to lyrics text file
            
        Returns:
            Dictionary with analysis results
        """
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            lyrics = f.read()
        
        return self.analyze_text(lyrics)
    
    def analyze_text(self, lyrics: str) -> Dict:
        """Analyze lyrics text.
        
        Args:
            lyrics: Lyrics text string
            
        Returns:
            Dictionary with analysis results
        """
        # Clean and tokenize
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        words = re.findall(r'\b\w+\b', lyrics.lower())
        
        # Extract common phrases
        phrases = self._extract_phrases(lyrics)
        
        # Analyze rhyme patterns
        rhyme_pattern = self._analyze_rhyme_pattern(lines)
        
        # Extract emotional keywords
        emotions = self._extract_emotions(lyrics)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(lyrics)
        
        # Word frequency
        word_freq = Counter(words).most_common(20)
        
        # Structure analysis
        structure = self._analyze_structure(lines)
        
        return {
            'line_count': len(lines),
            'word_count': len(words),
            'unique_words': len(set(words)),
            'common_phrases': phrases,
            'rhyme_pattern': rhyme_pattern,
            'emotions': emotions,
            'sentiment': sentiment,
            'word_frequency': word_freq,
            'structure': structure
        }
    
    def _extract_phrases(self, text: str, min_count: int = 2) -> List[Dict]:
        """Extract common phrases from text.
        
        Args:
            text: Input text
            min_count: Minimum occurrence count
            
        Returns:
            List of common phrases with counts
        """
        # Simple n-gram extraction (2-4 words)
        words = re.findall(r'\b\w+\b', text.lower())
        phrases = []
        
        for n in range(2, 5):
            ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
            phrase_counts = Counter(ngrams)
            phrases.extend([
                {'phrase': phrase, 'count': count}
                for phrase, count in phrase_counts.items()
                if count >= min_count
            ])
        
        return sorted(phrases, key=lambda x: x['count'], reverse=True)[:10]
    
    def _analyze_rhyme_pattern(self, lines: List[str]) -> Dict:
        """Analyze rhyme patterns in lyrics.
        
        Args:
            lines: List of lyric lines
            
        Returns:
            Dictionary with rhyme pattern info
        """
        if not lines:
            return {'pattern': 'none', 'rhyme_pairs': []}
        
        # Get last words of each line
        last_words = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line.lower())
            if words:
                last_words.append(words[-1])
        
        # Simple rhyme detection based on suffix matching
        rhyme_pairs = []
        for i in range(len(last_words)):
            for j in range(i+1, min(i+5, len(last_words))):
                if self._words_rhyme(last_words[i], last_words[j]):
                    rhyme_pairs.append((i, j, last_words[i], last_words[j]))
        
        # Detect pattern (simplified)
        pattern = 'free_verse'
        if len(rhyme_pairs) > len(lines) * 0.3:
            pattern = 'rhyming'
        
        return {
            'pattern': pattern,
            'rhyme_pairs': rhyme_pairs[:10],
            'rhyme_density': len(rhyme_pairs) / max(len(lines), 1)
        }
    
    def _words_rhyme(self, word1: str, word2: str) -> bool:
        """Simple rhyme detection based on suffix matching.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            True if words rhyme
        """
        if len(word1) < 2 or len(word2) < 2:
            return False
        
        # Check if last 2-3 characters match
        return (word1[-2:] == word2[-2:] or word1[-3:] == word2[-3:]) and word1 != word2
    
    def _extract_emotions(self, text: str) -> Dict:
        """Extract emotional keywords and themes.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with emotion categories and keywords
        """
        emotion_keywords = {
            'love': ['love', 'heart', 'forever', 'together', 'kiss', 'sweet', 'romance'],
            'sadness': ['sad', 'cry', 'tear', 'alone', 'lost', 'miss', 'goodbye'],
            'happiness': ['happy', 'joy', 'smile', 'laugh', 'bright', 'shine', 'celebrate'],
            'anger': ['angry', 'hate', 'fight', 'rage', 'fury', 'mad', 'scream'],
            'hope': ['hope', 'dream', 'believe', 'faith', 'future', 'tomorrow', 'wish']
        }
        
        text_lower = text.lower()
        emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            matches = [kw for kw in keywords if kw in text_lower]
            if matches:
                emotions[emotion] = {
                    'keywords': matches,
                    'count': sum(text_lower.count(kw) for kw in matches)
                }
        
        return emotions
    
    def _analyze_sentiment(self, text: str) -> Dict:
        """Analyze overall sentiment of lyrics.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment scores
        """
        blob = TextBlob(text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 to 1
            'subjectivity': blob.sentiment.subjectivity,  # 0 to 1
            'overall': 'positive' if blob.sentiment.polarity > 0 else 'negative' if blob.sentiment.polarity < 0 else 'neutral'
        }
    
    def _analyze_structure(self, lines: List[str]) -> Dict:
        """Analyze structural patterns in lyrics.
        
        Args:
            lines: List of lyric lines
            
        Returns:
            Dictionary with structure info
        """
        # Detect verses/chorus by repetition
        line_counts = Counter(lines)
        repeated_lines = [line for line, count in line_counts.items() if count > 1]
        
        return {
            'total_lines': len(lines),
            'repeated_lines': len(repeated_lines),
            'avg_line_length': sum(len(line.split()) for line in lines) / max(len(lines), 1),
            'has_chorus': len(repeated_lines) > 0
        }
    
    def save_analysis(self, analysis: Dict, output_file: str):
        """Save analysis results to JSON file.
        
        Args:
            analysis: Analysis dictionary
            output_file: Output filename
        """
        output_path = self.output_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, indent=2, fp=f)
        
        print(f"Analysis saved to {output_path}")
