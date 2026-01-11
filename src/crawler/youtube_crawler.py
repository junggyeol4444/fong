"""YouTube Music Crawler for collecting song metadata, lyrics, and audio files."""

import os
import json
import yt_dlp
from pathlib import Path
from typing import Dict, List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm


class YouTubeMusicCrawler:
    """Crawler for YouTube Music data collection."""
    
    def __init__(self, output_dir: str = "data/raw", progress_file: str = "progress.json"):
        """Initialize the YouTube Music Crawler.
        
        Args:
            output_dir: Directory to save downloaded files
            progress_file: Path to progress tracking file
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = Path(progress_file)
        self.progress = self._load_progress()
        self.is_running = False
        
    def _load_progress(self) -> Dict:
        """Load progress from file or create new progress tracker."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'downloaded': [],
            'failed': [],
            'last_url': None,
            'stats': {
                'total_downloads': 0,
                'total_failures': 0
            }
        }
    
    def _save_progress(self):
        """Save current progress to file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, indent=2, fp=f)
    
    def _is_duplicate(self, video_id: str) -> bool:
        """Check if video has already been downloaded.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if already downloaded, False otherwise
        """
        return video_id in self.progress['downloaded']
    
    def _extract_lyrics(self, video_id: str) -> Optional[str]:
        """Extract lyrics from YouTube video using transcript API.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Extracted lyrics or None if not available
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            lyrics = ' '.join([entry['text'] for entry in transcript_list])
            return lyrics
        except Exception as e:
            print(f"Could not extract lyrics for {video_id}: {str(e)}")
            return None
    
    def download_song(self, url: str, genre: Optional[str] = None) -> bool:
        """Download a single song with metadata and lyrics.
        
        Args:
            url: YouTube video URL
            genre: Optional genre tag for organization
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract video ID
            video_id = self._extract_video_id(url)
            
            # Check for duplicates
            if self._is_duplicate(video_id):
                print(f"Skipping duplicate: {video_id}")
                return True
            
            # Configure yt-dlp options
            genre_path = f"{genre}/" if genre else ""
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.output_dir / genre_path / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'writeinfojson': True,
                'writethumbnail': True,
                'quiet': False,
                'no_warnings': False,
            }
            
            # Download audio and metadata
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Extract and save lyrics
                lyrics = self._extract_lyrics(video_id)
                if lyrics:
                    lyrics_file = self.output_dir / genre_path / f"{video_id}_lyrics.txt"
                    lyrics_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(lyrics_file, 'w', encoding='utf-8') as f:
                        f.write(lyrics)
                
                # Update progress
                self.progress['downloaded'].append(video_id)
                self.progress['last_url'] = url
                self.progress['stats']['total_downloads'] += 1
                self._save_progress()
                
                return True
                
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            self.progress['failed'].append({'url': url, 'error': str(e)})
            self.progress['stats']['total_failures'] += 1
            self._save_progress()
            return False
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL.
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID
        """
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'watch?v=' in url:
            return url.split('watch?v=')[-1].split('&')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[-1].split('?')[0]
        else:
            return url
    
    def crawl_playlist(self, playlist_url: str, genre: Optional[str] = None, 
                      start_index: int = 0, max_count: Optional[int] = None):
        """Crawl an entire YouTube playlist.
        
        Args:
            playlist_url: URL of YouTube playlist
            genre: Optional genre tag
            start_index: Index to start from (for resuming)
            max_count: Maximum number of videos to download
        """
        self.is_running = True
        
        try:
            ydl_opts = {
                'extract_flat': True,
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                
                if 'entries' not in playlist_info:
                    print("No videos found in playlist")
                    return
                
                videos = playlist_info['entries']
                total = len(videos)
                
                if max_count:
                    videos = videos[start_index:start_index + max_count]
                else:
                    videos = videos[start_index:]
                
                print(f"Starting crawl from index {start_index}, total videos: {len(videos)}")
                
                for idx, video in enumerate(tqdm(videos, desc=f"Downloading {genre or 'music'}")):
                    if not self.is_running:
                        print("\nCrawling stopped by user")
                        break
                    
                    if video is None:
                        continue
                        
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                    self.download_song(video_url, genre)
                    
        except Exception as e:
            print(f"Error crawling playlist: {str(e)}")
        finally:
            self.is_running = False
            print(f"\nCrawling complete. Stats: {self.progress['stats']}")
    
    def stop(self):
        """Stop the crawling process."""
        self.is_running = False
        print("Stopping crawler...")
    
    def get_stats(self) -> Dict:
        """Get crawling statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_downloaded': len(self.progress['downloaded']),
            'total_failed': len(self.progress['failed']),
            'last_url': self.progress.get('last_url'),
            'stats': self.progress['stats']
        }
    
    def resume(self, playlist_url: str, genre: Optional[str] = None):
        """Resume crawling from last progress.
        
        Args:
            playlist_url: URL of YouTube playlist
            genre: Optional genre tag
        """
        downloaded_count = len(self.progress['downloaded'])
        print(f"Resuming from {downloaded_count} previously downloaded videos")
        self.crawl_playlist(playlist_url, genre, start_index=downloaded_count)
