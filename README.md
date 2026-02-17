# Discovery Engine Suite

A Python-based desktop application suite for discovering movies (via TMDB) and anime (via AniList).

## Features
- **Draggable UI:** Resizable sidebars for long titles.
- **Smart Search:** Autocomplete suggestions as you type.
- **Save System:** Keep track of your favorites in a local watchlist.

## Setup
1. Clone this repo.
2. Create a `.env` file with your `TMDB_TOKEN`.
3. Install requirements: `pip install -r requirements.txt`.

### Project Structure

| File | Description |
| :--- | :--- |
| **`gui_app.py`** | The main Movie Discovery Engine (TMDB API) |
| **`anime_app.py`** | The Anime Discovery Engine (AniList GraphQL) |
| **`explorer.py`** | A CLI tool to browse TMDB genres and technical IDs |
| **`push.bat`** | Automation script for staging and pushing edits |
| **`.env.example`** | Template for API keys (rename to .env) |
| **`requirements.txt`** | List of Python libraries needed to run the apps |

## Deployment Guide: Movie Discovery Engine

This guide explains how to set up and run the Movie Discovery Engine on a new computer.

### 1. Prerequisites
Before starting, ensure the new machine has:
* **Python 3.10+** installed.
* The project files: `gui_app.py` and `requirements.txt`.
* A stable internet connection.

---

### 2. Step-by-Step Setup

#### **Step A: The Environment File**
1. Create a new file in the project folder named `.env`.
2. Open it with a text editor and add your TMDB token:
   ```text
   TMDB_TOKEN=your_api_token_here
    ```
#### **Step B: Create a Virtual Environment**
This keeps the project libraries isolated from the rest of the computer.
* Open a terminal/command prompt in the project folder.
* Run the following command:
    ```bash
    python -m venv venv
    ```
#### **Step C: Install Required Libraries**
Activate the environment and use the `requirements.txt` file to install everything at once.
    
    venv\Scripts\activate
    pip install -r requirements.txt
---

### 3. Creating a "One-Click" Launcher
Instead of typing commands every time, create a Windows Batch script to launch the app instantly.
* Open Notepad.
* Paste the following code:
    
    ```Code snippet
    @echo off
    title Movie Engine Launcher
    :: Ensure we are in the right folder
    cd /d "%~dp0"
    :: Activate the environment and run the app
    call venv\Scripts\activate
    python gui_app.py
    pause
    ```
Save the file as `run_app.bat` inside your project folder.

---

### 4. How to Use the App

| Feature | How it works |
| :--- | :--- |
| **`Recommendation Mode`** | Enter a "Base Movie." The engine finds similar movies but filters out sequels so you find new favorites. |
| **`Discovery Mode`** | Leave "Base Movie" empty and use Year/Genre to browse the top-rated hits of that category. |
| **`Why Recommended?`** | Click any movie in the list to see the "Shared DNA" (genres) between your input and the result. |
| **`Action Buttons`** | Use the detail panel to watch trailers on YouTube or save titles to your `watchlist.txt`. |

---

### Troubleshooting
* Empty Results? Check your spelling or try a more common movie title.
* No Images? Ensure you are connected to the internet.
* Encoding Errors? If requirements.txt looks like gibberish, ensure it was saved in UTF-8 or ASCII format, not UTF-16.