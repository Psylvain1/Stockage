#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  9 17:57:04 2025

@author: ssppa
"""

"""
Created on Sat Aug  9 17:57:04 2025
@author: ssppa
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

SPOTIPY_CLIENT_ID = '7faebf878d054042b12d976029aa82a0'
SPOTIPY_CLIENT_SECRET = '82f4f861b531498f8b58ca03d428d90a'
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "playlist-read-private playlist-read-collaborative"

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Extract playlist ID from URL or URI
def extract_playlist_id(playlist_input):
    if "playlist" in playlist_input:
        return playlist_input.split("/")[-1].split("?")[0]
    return playlist_input

# Get playlist tracks
def get_playlist_tracks(playlist_input):
    playlist_id = extract_playlist_id(playlist_input)
    try:
        results = sp.playlist_tracks(playlist_id)
    except spotipy.exceptions.SpotifyException as e:
        print(f"❌ Spotify error: {e}")
        return []
    tracks = []
    for item in results['items']:
        track = item['track']
        if track:
            name = track['name']
            artist = track['artists'][0]['name']
            tracks.append(f"{artist} - {name}")
    return tracks

# Search YouTube
def search_youtube(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if results:
        return f"https://www.youtube.com{results[0]['url_suffix']}"
    return None

# Download from YouTube
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        #'format': '140',
        'outtmpl': '%(title)s.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg',  # or your custom path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True  # ⛔ Prevent downloading entire playlists
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# Main function
def download_playlist_from_spotify(playlist_input):
    tracks = get_playlist_tracks(playlist_input)
    for track in tracks:
        print(f"🔍 Searching for: {track}")
        url = search_youtube(track)
        if url:
            print(f"⬇️ Downloading: {url}")
            download_audio(url)
        else:
            print(f"❌ Not found: {track}")

# Example usage
if __name__ == "__main__":
    playlist_input = "https://open.spotify.com/playlist/37i9dQZF1DX6hvx9KDaW4s?si=_DAu8RUnSaqSU7-BN8mNRA"
    download_playlist_from_spotify(playlist_input)
