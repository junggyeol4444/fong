"""Voice synthesis for generating singing from lyrics and MIDI."""

import os
from pathlib import Path
from typing import Optional, Dict
from TTS.api import TTS
import json


class VoiceSynthesizer:
    """Synthesize singing voice from lyrics and music."""
    
    def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC",
                 output_dir: str = "data/generated"):
        """Initialize the Voice Synthesizer.
        
        Args:
            model_name: TTS model to use
            output_dir: Directory to save generated audio
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name
        self.tts = None
        self.voice_model_path = None
        
    def initialize_model(self):
        """Initialize the TTS model."""
        if self.tts is None:
            print(f"Loading TTS model: {self.model_name}")
            try:
                self.tts = TTS(model_name=self.model_name)
                print("TTS model loaded successfully")
            except Exception as e:
                print(f"Error loading TTS model: {str(e)}")
                print("Using default model instead")
                self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
    
    def synthesize_lyrics(self, lyrics: str, output_file: str,
                         speaker_wav: Optional[str] = None) -> str:
        """Synthesize speech from lyrics.
        
        Args:
            lyrics: Lyrics text to synthesize
            output_file: Output audio filename
            speaker_wav: Optional speaker reference audio for voice cloning
            
        Returns:
            Path to generated audio file
        """
        self.initialize_model()
        
        output_path = self.output_dir / output_file
        
        try:
            # Clean lyrics (remove section markers)
            clean_lyrics = self._clean_lyrics(lyrics)
            
            # Synthesize
            if speaker_wav and os.path.exists(speaker_wav):
                print("Synthesizing with voice cloning...")
                self.tts.tts_to_file(
                    text=clean_lyrics,
                    file_path=str(output_path),
                    speaker_wav=speaker_wav
                )
            else:
                print("Synthesizing with default voice...")
                self.tts.tts_to_file(
                    text=clean_lyrics,
                    file_path=str(output_path)
                )
            
            print(f"Voice synthesis complete: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error synthesizing voice: {str(e)}")
            return ""
    
    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean lyrics text for synthesis.
        
        Args:
            lyrics: Raw lyrics with section markers
            
        Returns:
            Cleaned lyrics text
        """
        # Remove section markers like [Verse], [Chorus], etc.
        import re
        clean = re.sub(r'\[.*?\]', '', lyrics)
        
        # Remove extra whitespace
        clean = re.sub(r'\n\s*\n', '\n', clean)
        
        return clean.strip()
    
    def train_voice_model(self, training_data_dir: str, output_model_dir: str,
                         config: Optional[Dict] = None):
        """Train a custom voice model on user's voice data.
        
        Args:
            training_data_dir: Directory containing voice training data
            output_model_dir: Directory to save trained model
            config: Optional training configuration
        """
        print("Voice model training is a complex process requiring:")
        print("1. High-quality voice recordings (at least 30 minutes)")
        print("2. Transcriptions for all audio files")
        print("3. Significant computational resources (GPU recommended)")
        print("4. Several hours of training time")
        print("\nFor this MVP version, we recommend using voice cloning")
        print("with a reference audio file instead of full model training.")
        
        # Store training configuration for future use
        config_path = Path(output_model_dir) / "training_config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        training_config = {
            'training_data_dir': training_data_dir,
            'output_model_dir': output_model_dir,
            'status': 'configured',
            'notes': 'Use synthesize_lyrics with speaker_wav parameter for voice cloning'
        }
        
        if config:
            training_config.update(config)
        
        with open(config_path, 'w') as f:
            json.dump(training_config, indent=2, fp=f)
        
        print(f"\nTraining configuration saved to: {config_path}")
    
    def combine_audio(self, vocals_file: str, instrumental_file: str,
                     output_file: str) -> str:
        """Combine vocals and instrumental tracks.
        
        Args:
            vocals_file: Path to vocals audio file
            instrumental_file: Path to instrumental/MIDI audio file
            output_file: Output filename for combined audio
            
        Returns:
            Path to combined audio file
        """
        try:
            from pydub import AudioSegment
            
            # Load audio files
            vocals = AudioSegment.from_file(vocals_file)
            instrumental = AudioSegment.from_file(instrumental_file)
            
            # Match lengths
            if len(vocals) < len(instrumental):
                vocals = vocals + AudioSegment.silent(duration=len(instrumental) - len(vocals))
            else:
                instrumental = instrumental + AudioSegment.silent(duration=len(vocals) - len(instrumental))
            
            # Mix tracks (adjust volumes as needed)
            vocals = vocals + 3  # Boost vocals by 3dB
            instrumental = instrumental - 5  # Reduce instrumental by 5dB
            
            combined = vocals.overlay(instrumental)
            
            # Export
            output_path = self.output_dir / output_file
            combined.export(str(output_path), format='mp3')
            
            print(f"Audio combined successfully: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"Error combining audio: {str(e)}")
            print("Make sure pydub and ffmpeg are installed")
            return ""
    
    def create_complete_song(self, lyrics: str, midi_file: str,
                           output_file: str, speaker_wav: Optional[str] = None) -> str:
        """Create a complete song with lyrics, music, and voice.
        
        Args:
            lyrics: Song lyrics
            midi_file: Path to MIDI music file
            output_file: Output audio filename
            speaker_wav: Optional speaker reference for voice cloning
            
        Returns:
            Path to complete song file
        """
        print("Creating complete song...")
        
        # Step 1: Synthesize vocals from lyrics
        vocals_file = self.synthesize_lyrics(
            lyrics,
            output_file=f"vocals_{output_file}",
            speaker_wav=speaker_wav
        )
        
        if not vocals_file:
            print("Failed to synthesize vocals")
            return ""
        
        # Step 2: Convert MIDI to audio (requires external tool)
        print("\nNote: MIDI to audio conversion requires external tools like:")
        print("  - FluidSynth")
        print("  - TiMidity++")
        print("  - Or a DAW (Digital Audio Workstation)")
        print("\nFor this MVP, you can manually convert the MIDI file")
        print(f"MIDI file location: {midi_file}")
        print(f"Vocals file location: {vocals_file}")
        
        # If instrumental audio exists, combine them
        instrumental_file = midi_file.replace('.mid', '.mp3')
        if os.path.exists(instrumental_file):
            return self.combine_audio(vocals_file, instrumental_file, output_file)
        
        print(f"\nVocals generated at: {vocals_file}")
        print("Convert MIDI to audio and use combine_audio() to create final song")
        
        return vocals_file
    
    def list_available_models(self) -> list:
        """List available TTS models.
        
        Returns:
            List of available model names
        """
        try:
            models = TTS().list_models()
            return models
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return []
