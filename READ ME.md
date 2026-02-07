# 🎬 Movie Discovery Engine

A Python-based CLI application that helps users find movies using the TMDB (The Movie Database) API. It supports intelligent recommendations, genre/keyword discovery, and interactive features like watching trailers and saving a personal watchlist.

## 🚀 Features
* **Smart Search:** Search based on a "Base Movie" for recommendations or use filters for Discovery.
* **Deep Filtering:** Filter by Year, Genre, Actor/Actress, or specific Keywords (e.g., "Time Travel").
* **Interactive Randomizer:** Stuck on what to watch? Let the app pick a "Surprise Movie" based on your filters.
* **Media Integration:** Instantly open YouTube trailers in your default web browser.
* **Local Caching:** Saves recommendation results locally to `tmdb_pantry.json` to speed up repeat searches and reduce API calls.
* **Personal Watchlist:** Save your favorite finds to a persistent text file.

---

## 📂 File Structure Explained

| File | Purpose |
| :--- | :--- |
| **`app.py`** | The "Brain." Contains the logic for API requests, caching, the randomizer, and the user interface. |
| **`.env`** | The "Safe." Stores your private TMDB API Token. **Never share this file.** |
| **`tmdb_pantry.json`** | The "Memory." A local cache that stores movie data so the app doesn't have to ask the internet for the same thing twice. |
| **`watchlist.txt`** | The "Notebook." A simple text file where your saved movies are stored for later viewing. |
| **`requirements.txt`** | The "Toolbox." Lists the external Python libraries (`requests`, `python-dotenv`) required to run the app. |
| **`venv/`** | The "Workshop." A virtual environment that keeps this project's dependencies separate from the rest of your computer. |

---

## 🛠️ Setup & Installation

1. **Clone/Download** this folder to your machine.
    * Upon opening for the first time (or restarting the session):
        * A. Open Terminal
            * Win: Ctrl + ~
            * Mac: Cmd + ~
        * B. Activate Virtual Environment (venv) by entering command below into Terminal
            * Win: .\venv\Scripts\activate
            * Mac/Linux: source venv/bin/activate
        * C. In the case you get an error when trying to activate venv, you'll need to bypass the terminal's security policy (temporarily) by entering the command below
            * Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
            * Then, re-enter the venv command again
2. **Install Dependencies** while inside your virtual environment:
   ```bash
   pip install -r requirements.txt
3. **Configure API Key** Create a .env file and add your TMDB Bearer Token:
    TMDB_TOKEN=your_token_here
    BASE_URL=[https://api.themoviedb.org/3](https://api.themoviedb.org/3)
4. Run the App
    python app.py

---

## 🧠 How to Use

1. Recommendations: Enter a movie you like (e.g., Interstellar) to get similar suggestions.
2. Discovery: Leave the "Base Movie" blank and enter a Genre (e.g., Sci-Fi) or a Keyword (e.g., Zombies) to explore the database.
3. Modes:
    Choose Mode 1 for a list of the top matches.
    Choose Mode 2 for a single random recommendation.
4. Interact: Follow the prompts to watch trailers or save movies to your watchlist.txt.