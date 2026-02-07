import requests
import os
from dotenv import load_dotenv

# ==========================================
# ⚙️ 1. INITIAL SETUP
# ==========================================
# Load the .env file from your local folder
load_dotenv()
API_TOKEN = os.getenv('TMDB_TOKEN')
BASE_URL = "https://api.themoviedb.org/3"

# Safety check for the token
if not API_TOKEN:
    print("❌ ERROR: TMDB_TOKEN not found in .env file!")
    exit()

headers = {
    "accept": "application/json", 
    "Authorization": f"Bearer {API_TOKEN}"
}

def explore_database():
    while True:
        print("\n" + "="*30)
        print("TMDB DATABASE EXPLORER")
        print("="*30)
        print("1. View All Official Movie Genres")
        print("2. View Popular Actors")
        print("3. View Titles Currently in Theaters")
        print("4. View Technical configurations (Sizes/Langs)")
        print("5. Exit Explorer")
        
        choice = input("\nEnter number (1-5): ")

        if choice == '1':
            url = f"{BASE_URL}/genre/movie/list"
            data = requests.get(url, headers=headers).json()
            print("\n📂 AVAILABLE MOVIE GENRES:")
            # Tip: Look for ID 12 (Adventure) here!
            for g in data.get('genres', []):
                print(f"ID: {g['id']:<5} | Name: {g['name']}")

        elif choice == '2':
            url = f"{BASE_URL}/person/popular"
            data = requests.get(url, headers=headers).json()
            print("\n🎭 TRENDING/POPULAR ACTORS:")
            for p in data.get('results', []):
                known_for = ", ".join([m.get('title', m.get('name', '')) for m in p.get('known_for', [])])
                print(f"Name: {p['name']:<20} | Known for: {known_for}")

        elif choice == '3':
            url = f"{BASE_URL}/movie/now_playing"
            data = requests.get(url, headers=headers).json()
            print("\n🍿 TITLES CURRENTLY IN THEATERS:")
            for m in data.get('results', []):
                print(f"Title: {m['title']:<30} | ID: {m['id']} (Released: {m['release_date']})")

        elif choice == '4':
            print("\n⚙️ FETCHING API CONFIGURATIONS...")
            # 1. Image Sizes
            config_url = f"{BASE_URL}/configuration"
            config_data = requests.get(config_url, headers=headers).json()
            print(f"\n🖼️ Poster Sizes: {config_data['images']['poster_sizes']}")

            # 2. Languages
            lang_url = f"{BASE_URL}/configuration/languages"
            lang_data = requests.get(lang_url, headers=headers).json()
            print(f"🌎 Total Languages in Database: {len(lang_data)}")

            # 3. Countries
            country_url = f"{BASE_URL}/configuration/countries"
            country_data = requests.get(country_url, headers=headers).json()
            print(f"📍 Total Countries in Database: {len(country_data)}")

        elif choice == '5':
            print("👋 Closing explorer. Happy hunting!")
            break
        
        else:
            print("⚠️ Invalid choice. Please pick 1-5.")

# --- RUN THE APP ---
if __name__ == "__main__":
    explore_database()