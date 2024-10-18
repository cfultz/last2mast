import pylast
import mastodon
from datetime import datetime, timedelta
import time
import re
import requests

# Last.fm API credentials
LASTFM_API_KEY = "YOUR_LASTFM_API_KEY"
LASTFM_API_SECRET = "YOUR_LASTFM_API_SECRET"
LASTFM_USERNAME = "YOUR_LASTFM_USERNAME"

# Mastodon API credentials
MASTODON_ACCESS_TOKEN = "YOUR_MASTODON_ACCESS_TOKEN"
MASTODON_API_BASE_URL = "YOUR_MASTODON_INSTANCE_URL"

# Shlink server credentials
SHLINK_API_KEY = "YOUR_SHLINK_API_KEY"
SHLINK_SERVER_URL = "YOUR_SHLINK_SERVER_URL/"

# Initialize Last.fm network
network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
)

# Initialize Mastodon API client
mastodon_client = mastodon.Mastodon(
    access_token=MASTODON_ACCESS_TOKEN,
    api_base_url=MASTODON_API_BASE_URL
)

posted_track_titles = set()
posted_weekly_update = False


def post_loved_track(track):
    """Posts the loved track to Mastodon, avoiding duplicates."""
    artist = track.artist.name
    title = track.title
    album = track.get_album()
    url = track.get_url()
    lastfm_profile = f"https://www.last.fm/user/{LASTFM_USERNAME}"

    if title in posted_track_titles:
        print(f"Skipping duplicate track: {artist} - {title}")
        return

    try:
        response = requests.post(
            f"{SHLINK_SERVER_URL}/rest/v2/short-urls",
            headers={
                "X-Api-Key": f"{SHLINK_API_KEY}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={"longUrl": url},
        )
        response.raise_for_status()
        short_url = response.json()["shortUrl"]

    except requests.exceptions.RequestException as e:
        print(f"Error shortening URL: {e}")
        short_url = url

    hashtags = []
    hashtags.append(f"#{re.sub(r'[^a-zA-Z0-9]', '', artist)}")
    if album:
        hashtags.append(f"#{re.sub(r'[^a-zA-Z0-9]', '', album.title)}")

    try:
        genre = track.get_top_tags()[0].item.name
        hashtags.append(f"#{genre}")
    except IndexError:
        pass

    hashtag_string = " ".join(hashtags)

    message = f"❤️ Loved: {artist} - {title} {short_url}\n\n{hashtag_string}\n\n{lastfm_profile}"

    if len(message) > 500:
        message = message[:497] + "..."

    mastodon_client.status_post(message)
    posted_track_titles.add(title)


def post_weekly_top_artists_and_tracks():
    """Posts the weekly top artists and tracks to Mastodon, only once per Friday."""
    global posted_weekly_update

    if posted_weekly_update:
        return

    top_artists = network.get_user(LASTFM_USERNAME).get_top_artists(
        period='7day',
        limit=5,
    )

    top_tracks = network.get_user(LASTFM_USERNAME).get_top_tracks(
        period='7day',
        limit=5,
    )

    lastfm_profile = f"https://www.last.fm/user/{LASTFM_USERNAME}"
    message = "🎶 Weekly Top Artists and Tracks:\n\n"
    message += "**Top Artists:**\n"
    for artist in top_artists:
        message += f"- {artist.item.name} ({artist.weight} plays)\n"

    message += "\n**Top Tracks:**\n"
    for track in top_tracks:
        message += f"- {track.item.artist.name} - {track.item.title} ({track.weight} plays)\n"

    message += f"\n{lastfm_profile}"

    if len(message) > 500:
        message = message[:497] + "..."

    mastodon_client.status_post(message)
    posted_weekly_update = True


def main():
    last_loved_track = None
    global posted_weekly_update

    while True:
        try:
            loved_tracks = network.get_user(LASTFM_USERNAME).get_loved_tracks(limit=1)

        except pylast.NetworkError as e:
            print(f"Error fetching loved tracks: {e}")
            loved_tracks = None

        # Access the track title correctly
        if loved_tracks and loved_tracks[0].track.title != last_loved_track:  
            post_loved_track(loved_tracks[0].track)  # Pass the Track object
            last_loved_track = loved_tracks[0].track.title  # Store the track title

        if datetime.today().weekday() == 4:  # Friday is 4
            post_weekly_top_artists_and_tracks()
        
        posted_weekly_update = False

        time.sleep(300)

if __name__ == "__main__":
    main()