import sys
from dotenv import load_dotenv
from spotify_client import SpotifyClient


def prompt_playlist_selection(playlists):
    print("\nYour playlists:")
    for i, pl in enumerate(playlists, 1):
        print(f"  {i:3}. {pl['name']} ({pl['tracks']} tracks)")
    print()

    while True:
        raw = input("Select playlists by number (e.g. 1 3 5): ").strip()
        if not raw:
            print("No playlists selected.")
            continue
        try:
            indices = [int(x) for x in raw.split()]
        except ValueError:
            print("Enter space-separated numbers only.")
            continue
        if any(i < 1 or i > len(playlists) for i in indices):
            print(f"Numbers must be between 1 and {len(playlists)}.")
            continue
        return [playlists[i - 1] for i in indices]


def confirm(prompt):
    return input(prompt).strip().lower() == "y"


def main():
    load_dotenv()

    print("Connecting to Spotify...")
    client = SpotifyClient()

    print("Fetching liked songs...")
    liked_ids = client.get_all_liked_songs()
    print(f"You have {len(liked_ids)} liked songs.")

    playlists = client.get_user_playlists()
    if not playlists:
        print("No playlists found.")
        sys.exit(1)

    selected = prompt_playlist_selection(playlists)

    print("\nSelected playlists:")
    for pl in selected:
        print(f"  - {pl['name']}")

    print(f"\nThis will:")
    print(f"  1. Remove all {len(liked_ids)} liked songs")
    print(f"  2. Re-add tracks from {len(selected)} playlist(s)")

    if not confirm("\nProceed? (y/N): "):
        print("Aborted.")
        sys.exit(0)

    # Clear liked songs
    if liked_ids:
        print(f"\nRemoving {len(liked_ids)} liked songs...")
        for done in client.remove_all_liked_songs(liked_ids):
            print(f"  Removed {done}/{len(liked_ids)}...", end="\r")
        print(f"  Removed {len(liked_ids)}/{len(liked_ids)}   ")
    else:
        print("\nNo liked songs to remove.")

    # Collect tracks from selected playlists
    print("\nFetching tracks from selected playlists...")
    seen = set()
    new_track_ids = []
    for pl in selected:
        ids = client.get_playlist_tracks(pl["id"])
        before = len(new_track_ids)
        for tid in ids:
            if tid not in seen:
                seen.add(tid)
                new_track_ids.append(tid)
        added = len(new_track_ids) - before
        print(f"  {pl['name']}: {added} tracks ({len(ids) - added} duplicates skipped)")

    if not new_track_ids:
        print("\nNo tracks to add.")
        sys.exit(0)

    # Add to liked songs
    print(f"\nAdding {len(new_track_ids)} tracks to liked songs...")
    for done in client.add_to_liked_songs(new_track_ids):
        print(f"  Added {done}/{len(new_track_ids)}...", end="\r")
    print(f"  Added {len(new_track_ids)}/{len(new_track_ids)}   ")

    print(f"\nDone! Liked songs reset to {len(new_track_ids)} tracks from {len(selected)} playlist(s).")


if __name__ == "__main__":
    main()
