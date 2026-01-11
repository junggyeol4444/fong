"""MIDI music generation based on genre, BPM, and key."""

import random
from pathlib import Path
from typing import List, Optional, Dict
from midiutil import MIDIFile


class MusicGenerator:
    """Generate MIDI music files based on parameters."""
    
    def __init__(self, output_dir: str = "data/generated"):
        """Initialize the Music Generator.
        
        Args:
            output_dir: Directory to save generated MIDI files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Musical scales
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10]
        }
        
        # Note mapping
        self.note_map = {
            'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65,
            'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71
        }
        
        # Genre patterns
        self.genre_patterns = {
            'pop': {
                'progression': [0, 3, 4, 0],  # I-IV-V-I
                'rhythm': [1, 0.5, 0.5, 1],
                'scale': 'major'
            },
            'rock': {
                'progression': [0, 5, 3, 4],  # I-vi-IV-V
                'rhythm': [1, 1, 0.5, 0.5],
                'scale': 'minor'
            },
            'jazz': {
                'progression': [0, 3, 1, 4],  # I-IV-ii-V
                'rhythm': [0.75, 0.25, 0.5, 0.5],
                'scale': 'major'
            },
            'blues': {
                'progression': [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4],  # 12-bar blues
                'rhythm': [1, 1, 1, 1],
                'scale': 'blues'
            }
        }
    
    def generate_midi(self, genre: str = 'pop', key: str = 'C', 
                     bpm: int = 120, duration: int = 32,
                     output_file: Optional[str] = None) -> str:
        """Generate a MIDI file based on parameters.
        
        Args:
            genre: Music genre (pop, rock, jazz, blues)
            key: Musical key (C, D, E, F, G, A, B with optional #)
            bpm: Beats per minute
            duration: Duration in beats
            output_file: Output filename (auto-generated if None)
            
        Returns:
            Path to generated MIDI file
        """
        # Create MIDI file
        midi = MIDIFile(2)  # 2 tracks: melody and chords
        
        # Set tempo
        track = 0
        time = 0
        midi.addTempo(track, time, bpm)
        
        # Get genre pattern
        if genre not in self.genre_patterns:
            genre = 'pop'
        
        pattern = self.genre_patterns[genre]
        scale_type = pattern['scale']
        progression = pattern['progression']
        
        # Get base note for key
        if key not in self.note_map:
            key = 'C'
        base_note = self.note_map[key]
        
        # Generate chord track
        self._add_chord_progression(midi, track=0, base_note=base_note,
                                    progression=progression, duration=duration,
                                    scale_type=scale_type)
        
        # Generate melody track
        self._add_melody(midi, track=1, base_note=base_note,
                        scale_type=scale_type, duration=duration)
        
        # Save MIDI file
        if output_file is None:
            output_file = f"{genre}_{key}_{bpm}bpm.mid"
        
        output_path = self.output_dir / output_file
        with open(output_path, 'wb') as f:
            midi.writeFile(f)
        
        print(f"MIDI file generated: {output_path}")
        return str(output_path)
    
    def _add_chord_progression(self, midi: MIDIFile, track: int, base_note: int,
                              progression: List[int], duration: int, scale_type: str):
        """Add chord progression to MIDI file.
        
        Args:
            midi: MIDIFile object
            track: Track number
            base_note: Base MIDI note number
            progression: Chord progression pattern
            duration: Total duration in beats
            scale_type: Type of scale to use
        """
        channel = 0
        volume = 80
        
        scale = self.scales[scale_type]
        beats_per_chord = 4
        time = 0
        
        prog_index = 0
        while time < duration:
            # Get chord root from progression
            chord_degree = progression[prog_index % len(progression)]
            root = base_note + scale[chord_degree % len(scale)]
            
            # Add chord notes (root, third, fifth)
            notes = [
                root,
                root + scale[2],  # third
                root + scale[4]   # fifth
            ]
            
            for note in notes:
                midi.addNote(track, channel, note, time, beats_per_chord, volume)
            
            time += beats_per_chord
            prog_index += 1
    
    def _add_melody(self, midi: MIDIFile, track: int, base_note: int,
                   scale_type: str, duration: int):
        """Add melody line to MIDI file.
        
        Args:
            midi: MIDIFile object
            track: Track number
            base_note: Base MIDI note number
            scale_type: Type of scale to use
            duration: Total duration in beats
        """
        channel = 1
        volume = 100
        
        scale = self.scales[scale_type]
        time = 0
        
        # Melody rhythm patterns
        rhythms = [1, 0.5, 0.5, 1, 2, 0.25, 0.25, 0.25, 0.25]
        
        # Generate melody
        octave_offset = 12  # Melody one octave higher
        prev_note_index = 0
        
        while time < duration:
            # Choose note from scale (tend to move stepwise)
            move = random.choice([-2, -1, 0, 1, 2])
            note_index = (prev_note_index + move) % len(scale)
            
            note = base_note + octave_offset + scale[note_index]
            
            # Choose rhythm
            note_duration = random.choice(rhythms)
            
            # Don't exceed total duration
            if time + note_duration > duration:
                note_duration = duration - time
            
            midi.addNote(track, channel, note, time, note_duration, volume)
            
            time += note_duration
            prev_note_index = note_index
    
    def generate_from_analysis(self, analysis: Dict, output_file: Optional[str] = None) -> str:
        """Generate MIDI based on music analysis data.
        
        Args:
            analysis: Analysis dictionary from MusicAnalyzer
            output_file: Output filename
            
        Returns:
            Path to generated MIDI file
        """
        # Extract parameters from analysis
        bpm = int(analysis.get('bpm', {}).get('tempo', 120))
        key = analysis.get('key', {}).get('key', 'C')
        
        # Infer genre from tempo
        if bpm < 90:
            genre = 'jazz'
        elif bpm < 120:
            genre = 'pop'
        else:
            genre = 'rock'
        
        return self.generate_midi(genre=genre, key=key, bpm=bpm, output_file=output_file)
    
    def generate_chord_progression(self, key: str = 'C', progression_type: str = 'pop') -> List[str]:
        """Generate a chord progression.
        
        Args:
            key: Musical key
            progression_type: Type of progression (pop, rock, jazz, blues)
            
        Returns:
            List of chord names
        """
        if progression_type not in self.genre_patterns:
            progression_type = 'pop'
        
        pattern = self.genre_patterns[progression_type]
        progression_indices = pattern['progression']
        scale = self.scales[pattern['scale']]
        
        # Roman numeral to chord name mapping
        chord_names = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
        
        chords = []
        for idx in progression_indices:
            if idx < len(chord_names):
                chords.append(f"{key} {chord_names[idx]}")
        
        return chords
