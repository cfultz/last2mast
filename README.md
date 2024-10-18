# Last.fm to Mastodon

This Python script automatically posts your loved tracks from Last.fm to your Mastodon profile. It also posts a weekly update of your top artists and tracks every Friday.

## Features

- Posts newly loved tracks from Last.fm to Mastodon.
- Shortens track URLs using your Shlink server.
- Adds relevant hashtags to posts (artist, album, genre).
- Posts a weekly summary of top artists and tracks every Friday.
- Prevents duplicate posts by checking track titles.

## Requirements

- Python 3.7 or higher
- A Last.fm account
- A Mastodon account
- A Shlink server (optional, for URL shortening)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/cfultz/last2mast
   ```

2. Create a virtual environment: 
```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required libraries:

```bash
pip install pylast mastodon.py requests
```

## Configuration

Obtain API credentials:

Last.fm:Get your API key and secret from the Last.fm API website.
        
Mastodon: Follow the instructions for your Mastodon instance to obtain an access token (usually in the "Settings" or "Development" section).
        
Shlink (optional): Get your API key from your Shlink server settings.

Edit the script: Open the last2mast.py file in a text editor. Replace the placeholder API credentials with your actual credentials:
```bash
            LASTFM_API_KEY
            LASTFM_API_SECRET
            LASTFM_USERNAME
            MASTODON_ACCESS_TOKEN
            MASTODON_API_BASE_URL
            SHLINK_API_KEY
            SHLINK_SERVER_URL (include a trailing slash, e.g., https://your-shlink-server.com/)
```
## Running the script 

1. Activate your virtual environment:

```bash
source .venv/bin/activate
```

2. Run the script:
```bash
python main.py
```
This will run the script in the foreground. To run it in the background, you can use:

```bash
nohup python main.py &
```
For continuous operation, consider using a task scheduler (cron, Task Scheduler) or a systemd service (on Linux) to run the script periodically.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
