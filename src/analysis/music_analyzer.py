"""Music analysis for extracting BPM, chord progressions, and key signatures."""

import json
import librosa
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional


class MusicAnalyzer:
    """Analyze music files for BPM, chords, and key signatures."""
    
    def __init__(self, output_dir: str = "data/analyzed"):
        """Initialize the Music Analyzer.
        
        Args:
            output_dir: Directory to save analysis results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_file(self, audio_file: Path) -> Dict:
        """Analyze a single audio file.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load audio file
            y, sr = librosa.load(str(audio_file), sr=22050)
            
            # Extract features
            bpm = self._extract_bpm(y, sr)
            key = self._extract_key(y, sr)
            chroma = self._extract_chroma_features(y, sr)
            spectral = self._extract_spectral_features(y, sr)
            
            return {
                'file': str(audio_file.name),
                'duration': len(y) / sr,
                'sample_rate': sr,
                'bpm': bpm,
                'key': key,
                'chroma_features': chroma,
                'spectral_features': spectral
            }
            
        except Exception as e:
            print(f"Error analyzing {audio_file}: {str(e)}")
            return {'error': str(e), 'file': str(audio_file.name)}
    
    def _extract_bpm(self, y: np.ndarray, sr: int) -> Dict:
        """Extract BPM (tempo) from audio.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Dictionary with BPM info
        """
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        return {
            'tempo': float(tempo),
            'beats_count': len(beats),
            'tempo_category': self._categorize_tempo(tempo)
        }
    
    def _categorize_tempo(self, bpm: float) -> str:
        """Categorize tempo into music terms.
        
        Args:
            bpm: Beats per minute
            
        Returns:
            Tempo category string
        """
        if bpm < 60:
            return 'Largo'
        elif bpm < 76:
            return 'Adagio'
        elif bpm < 108:
            return 'Andante'
        elif bpm < 120:
            return 'Moderato'
        elif bpm < 156:
            return 'Allegro'
        elif bpm < 176:
            return 'Vivace'
        else:
            return 'Presto'
    
    def _extract_key(self, y: np.ndarray, sr: int) -> Dict:
        """Extract key signature from audio.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Dictionary with key info
        """
        # Extract chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Average chroma across time
        chroma_mean = np.mean(chroma, axis=1)
        
        # Key names
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Find dominant key
        key_index = int(np.argmax(chroma_mean))
        confidence = float(chroma_mean[key_index])
        
        return {
            'key': keys[key_index],
            'confidence': confidence,
            'chroma_distribution': {keys[i]: float(chroma_mean[i]) for i in range(12)}
        }
    
    def _extract_chroma_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract chroma features for chord analysis.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Dictionary with chroma features
        """
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        return {
            'chroma_stft_mean': chroma_stft.mean(axis=1).tolist(),
            'chroma_cqt_mean': chroma_cqt.mean(axis=1).tolist(),
            'chroma_variation': float(np.std(chroma_stft))
        }
    
    def _extract_spectral_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract spectral features.
        
        Args:
            y: Audio time series
            sr: Sample rate
            
        Returns:
            Dictionary with spectral features
        """
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        
        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        return {
            'spectral_centroid_mean': float(np.mean(spectral_centroids)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'zero_crossing_rate_mean': float(np.mean(zcr)),
            'mfcc_mean': np.mean(mfcc, axis=1).tolist()
        }
    
    def extract_chord_progression(self, audio_file: Path, num_chords: int = 8) -> List[str]:
        """Extract simplified chord progression from audio.
        
        Args:
            audio_file: Path to audio file
            num_chords: Number of chords to extract
            
        Returns:
            List of chord names
        """
        try:
            y, sr = librosa.load(str(audio_file), sr=22050)
            
            # Extract chroma features
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            
            # Segment the song
            segment_length = chroma.shape[1] // num_chords
            chords = []
            
            chord_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            
            for i in range(num_chords):
                start = i * segment_length
                end = start + segment_length
                segment = chroma[:, start:end]
                
                # Find dominant note in segment
                dominant = np.argmax(np.mean(segment, axis=1))
                chords.append(chord_names[dominant])
            
            return chords
            
        except Exception as e:
            print(f"Error extracting chords from {audio_file}: {str(e)}")
            return []
    
    def save_analysis(self, analysis: Dict, output_file: str):
        """Save analysis results to JSON file.
        
        Args:
            analysis: Analysis dictionary
            output_file: Output filename
        """
        output_path = self.output_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, indent=2, fp=f)
        
        print(f"Music analysis saved to {output_path}")
