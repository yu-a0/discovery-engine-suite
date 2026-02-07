# Discovery Engine Suite 🎬 ⛩️

A Python-based desktop application suite for discovering movies via TMDB and anime via AniList.

## Features
- **Draggable UI:** Resizable sidebars for long titles.
- **Smart Search:** Autocomplete suggestions as you type.
- **Save System:** Keep track of your favorites in a local watchlist.

## Setup
1. Clone this repo.
2. Create a `.env` file with your `TMDB_TOKEN`.
3. Install requirements: `pip install -r requirements.txt`.

### 📂 Project Structure

| File | Description |
| :--- | :--- |
| **gui_app.py** | The main Movie Discovery Engine (TMDB API) |
| **anime_app.py** | The Anime Discovery Engine (AniList GraphQL) |
| **explorer.py** | A CLI tool to browse TMDB genres and technical IDs |
| **push.bat** | Automation script for staging and pushing edits |
| **.env.example** | Template for API keys (rename to .env) |
| **requirements.txt** | List of Python libraries needed to run the apps |