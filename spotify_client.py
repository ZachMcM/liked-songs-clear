import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SCOPES = " ".join([
    "user-library-read",
    "user-library-modify",
    "playlist-read-private",
    "playlist-read-collaborative",
])


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.environ["SPOTIPY_CLIENT_ID"],
            client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
            scope=SCOPES,
        ))

    def get_all_liked_songs(self):
        track_ids = []
        results = self.sp.current_user_saved_tracks(limit=50)
        while results:
            for item in results["items"]:
                if item["track"] and item["track"]["id"]:
                    track_ids.append(item["track"]["id"])
            results = self.sp.next(results) if results["next"] else None
        return track_ids

    def remove_all_liked_songs(self, track_ids):
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i + 50]
            self.sp._delete("me/tracks", payload={"ids": batch})
            yield i + len(batch)

    def get_user_playlists(self):
        playlists = []
        results = self.sp.current_user_playlists(limit=50)
        while results:
            for item in results["items"]:
                playlists.append({"id": item["id"], "name": item["name"], "tracks": item["tracks"]["total"]})
            results = self.sp.next(results) if results["next"] else None
        return playlists

    def get_playlist_tracks(self, playlist_id):
        track_ids = []
        results = self.sp.playlist_tracks(playlist_id, limit=100, fields="next,items(track(id,is_local))")
        while results:
            for item in results["items"]:
                track = item.get("track")
                if track and not track.get("is_local") and track.get("id"):
                    track_ids.append(track["id"])
            results = self.sp.next(results) if results["next"] else None
        return track_ids

    def add_to_liked_songs(self, track_ids):
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i + 50]
            self.sp._put("me/tracks", payload={"ids": batch})
            yield i + len(batch)
