# Spotify Lyrics Overlay
<p align="center">
  <img src="Spotify_Overlay.gif" alt="Spotify Overlay Demo" width="850"/>
</p>
A lightweight desktop overlay that displays synchronized Spotify lyrics while you're gaming or working, without the need to alt-tab.

The application connects to the Spotify Web API to detect the currently playing song and automatically searches for synchronized (`.lrc`) lyrics. The overlay remains on top of other applications, creating a clean karaoke-style experience.

---

## Features

- 🎵 Displays the currently playing Spotify song
- 📝 Shows synchronized lyrics in real time
- 🎮 Designed to work while gaming
- 🖥️ Transparent always-on-top overlay
- ⚡ Smooth lyric transitions
- 💾 Local lyrics cache for faster loading
- 🎨 Customizable appearance
- ⌨️ Toggle overlay visibility with **F12**

---


# Requirements

- Python 3.10 or newer
- Spotify Desktop Application
- Spotify Premium account *(recommended for playback detection)*
- Spotify Developer Application

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/spotify-lyrics-overlay.git
cd spotify-lyrics-overlay
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Spotify API Setup

This project uses Spotify's Web API.

Before running the program, you must create your own Spotify Developer application.

## Step 1

Go to:

https://developer.spotify.com/dashboard

Login using your Spotify account.

---

## Step 2

Click:

**Create App**

Fill in:

- App Name
- App Description

Accept the terms and create the application.

---

## Step 3

After creating the app you'll receive:

- Client ID
- Client Secret

Keep both values.

---

## Step 4

Open your application settings.

Under **Redirect URIs**, add:

```
http://localhost:8888/callback
```

*(Or the same Redirect URI configured inside the project.)*

Save the changes.

---

# Configure the Application

Open:

```
config.py
```

Replace the following values:

```python
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8888/callback"
```

Example:

```python
CLIENT_ID = "xxxxxxxxxxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxx"
REDIRECT_URI = "http://localhost:8888/callback"
```

---

# Running the Project

Simply execute:

```bash
python main.py
```

The first time the application runs:

- Your browser will open.
- Spotify will ask you to authorize the application.
- After authorization, the access token will be stored locally.

---

# How It Works

1. Detects the currently playing Spotify song.
2. Retrieves song metadata using Spotify Web API.
3. Searches for synchronized lyrics.
4. Caches downloaded lyrics locally.
5. Displays previous, current and next lyric lines inside the overlay.
6. Updates automatically when the music changes.

---

# Controls

| Key | Action |
|------|--------|
| F12 | Toggle overlay visibility |

---

# Project Structure

```
SpotifyLyricsOverlay/
│
├── cache_manager.py
├── config.py
├── config_manager.py
├── lyrics_manager.py
├── spotify_controller.py
├── overlay.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

- Python
- Tkinter
- Spotipy
- Spotify Web API
- syncedlyrics
- Pillow
- threading

---

# Future Improvements

- [ ] Multiple overlay themes
- [ ] Better lyric animations
- [ ] Automatic font scaling
- [ ] Multi-monitor support
- [ ] Click-through overlay mode
- [ ] Packaging into an executable (.exe)

---

# Disclaimer

This project is not affiliated with Spotify.

Spotify is a trademark of Spotify AB.

---

# License

This project is licensed under the MIT License.
