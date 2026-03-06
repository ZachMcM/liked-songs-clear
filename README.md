# liked-songs-clear

CLI tool to reset your Spotify liked songs to exactly the tracks in your chosen playlists.

**What it does:**
1. Shows your current liked song count
2. Lists your playlists for selection (multi-select supported)
3. Clears all liked songs
4. Re-adds every track from the selected playlists (deduplicated)

## Setup

**1. Create a Spotify app**

Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), create an app, and add `http://127.0.0.1:8888/callback` as a redirect URI.

**2. Configure credentials**

```bash
cp .env.example .env
```

Fill in your `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` from the dashboard.

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

A browser window will open for OAuth on the first run. Select your playlists by number (e.g. `1 3 5`), confirm, and the tool handles the rest.
