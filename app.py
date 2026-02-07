import os
import json
import requests
import textwrap
import random
import webbrowser
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
load_dotenv()
API_TOKEN = os.getenv('TMDB_TOKEN')
BASE_URL = os.getenv('BASE_URL')
headers = {"accept": "application/json", "Authorization": f"Bearer {API_TOKEN}"}
CACHE_FILE = "tmdb_pantry.json"

# --- THE MISSING VARIABLE ---
GENRES = {
    "action": 28, "thriller": 53, "comedy": 35, "horror": 27, 
    "sci-fi": 878, "drama": 18, "mystery": 9648, "animation": 16, 
    "fantasy": 14, "romance": 10749, "documentary": 99
}

# Create a dictionary that turns 28 -> "Action", etc.
GENRE_NAMES = {v: k.capitalize() for k, v in GENRES.items()}

# 2. CACHING ENGINE
def get_recommendations_with_cache(movie_id):
    pantry = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            pantry = json.load(f)
            if str(movie_id) in pantry:
                return pantry[str(movie_id)]
    
    rec_url = f"{BASE_URL}/movie/{movie_id}/recommendations"
    response = requests.get(rec_url, headers=headers)
    data = response.json().get('results', [])
    
    pantry[str(movie_id)] = data
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(pantry, f)
    return data

def add_to_watchlist(movie_details):
    with open("watchlist.txt", "a", encoding="utf-8") as f:
        f.write(f"{movie_details}\n")
    print("\n✅ Saved to watchlist.txt!")

# 3. MAIN INTERFACE
def main():
    print("\n🎬 WELCOME TO THE MOVIE DISCOVERY ENGINE")
    print("-" * 40)
    fav_movie = input("Base Movie (leave blank for discovery): ")
    year_filter = input("Year (optional): ")
    theme_input = input("Genre or Keyword (e.g. 'Space' or 'Thriller'): ").lower()
    actor_name = input("Actor/Actress (optional): ")
    
    mode = input("\nChoose Mode: [1] List Top 5 | [2] Surprise Me (Random): ")

# --- ID SCOUTING ---
    target_actor_id = None
    target_genre_id = GENRES.get(theme_input)
    target_keyword_id = None

    if actor_name:
        p_res = requests.get(f"{BASE_URL}/search/person", headers=headers, params={"query": actor_name}).json()
        if p_res.get('results'): 
            target_actor_id = p_res['results'][0]['id']

    if theme_input and not target_genre_id:
        k_res = requests.get(f"{BASE_URL}/search/keyword", headers=headers, params={"query": theme_input}).json()
        if k_res.get('results'): 
            target_keyword_id = k_res['results'][0]['id']

# --- CORE SEARCH (All Improvements Combined) ---
    movies_to_show = []
    base_genre_ids = [] # Used to explain the "Why" later
    
    if fav_movie:
        s_res = requests.get(f"{BASE_URL}/search/movie", headers=headers, params={"query": fav_movie}).json()
        if s_res.get('results'):
            base_movie = s_res['results'][0]
            base_id = base_movie['id']
            base_title = base_movie['title'].lower()
            base_genre_ids = base_movie.get('genre_ids', []) # Save the DNA
            
            recommendations = get_recommendations_with_cache(base_id)
            
            # IMPROVEMENT 1: Filter out sequels immediately
            unique_recs = [m for m in recommendations if base_title not in m['title'].lower()]
            
            # IMPROVEMENT 2: Tiered Fallback Logic (Perfect -> Close -> Broad)
            # Tier 1: Matches Year AND Genre
            tier_1 = [m for m in unique_recs if 
                     (not year_filter or (m.get('release_date') and year_filter in m['release_date'])) and
                     (not target_genre_id or target_genre_id in m.get('genre_ids', []))]
            
            # Tier 2: Matches Genre only
            tier_2 = [m for m in unique_recs if (not target_genre_id or target_genre_id in m.get('genre_ids', []))]

            if tier_1:
                movies_to_show = tier_1
                print("\n✨ Found perfect matches!")
            elif tier_2 and (year_filter or target_genre_id):
                movies_to_show = tier_2
                print(f"\n⚠️ No {year_filter} matches. Showing {theme_input or 'relevant'} recommendations...")
            else:
                movies_to_show = unique_recs
                print("\nℹ️ No matches for those filters. Showing all top recommendations...")
    else:
        # Standard Discovery Path
        params = {"primary_release_year": year_filter, "with_cast": target_actor_id, 
                  "with_genres": target_genre_id, "with_keywords": target_keyword_id, "sort_by": "popularity.desc"}
        res = requests.get(f"{BASE_URL}/discover/movie", headers=headers, params=params).json()
        movies_to_show = res.get('results', [])

# --- RANDOMIZER LOGIC ---
    if mode == '2':
        movies_to_show = [random.choice(movies_to_show)]
        print(f"\n🎲 RANDOM PICK BASED ON YOUR FILTERS:")
    else:
# Change the number in [:5] to increase/decrease the about of titles listed
        movies_to_show = movies_to_show[:5]
        print(f"\n{'='*70}\nTOP RECOMMENDATIONS\n{'='*70}")

# --- 1. DISPLAY THE LIST ---
    if not movies_to_show:
        print("\n❌ No matches found.")
        return

    print(f"\n{'='*75}\n{'ID':<4} {'MOVIE TITLE':<40} {'YEAR':<6} {'RATING':<8}\n{'='*75}")
    
    # We store the objects in a list so we can access them by index later
    session_movies = movies_to_show[:5] if mode != '2' else [movies_to_show[0]]

    for i, movie in enumerate(session_movies, 1):
        title = movie['title']
        year = movie.get('release_date', '????')[:4]
        rating = f"{movie['vote_average']}/10"
        print(f"[{i}]  {title[:38]:<40} {year:<6} {rating:<8}")

    # --- INTERACTION MENU (Now with REASON logic) ---
    while True:
        choice = input("\n👉 Enter a movie number for details/options (or Enter to quit): ")
        
        if not choice:
            break
        
        if choice.isdigit() and 1 <= int(choice) <= len(session_movies):
            selected = session_movies[int(choice)-1]
            
            print(f"\n--- LOADING DETAILS FOR: {selected['title']} ---")
            
            # 1. Fetch Cast & Trailer (Same as before)
            c_res = requests.get(f"{BASE_URL}/movie/{selected['id']}/credits", headers=headers).json()
            cast = ", ".join([p['name'] for p in c_res.get('cast', [])[:3]])
            v_res = requests.get(f"{BASE_URL}/movie/{selected['id']}/videos", headers=headers).json()
            trailer_key = next((v['key'] for v in v_res.get('results', []) if v['type'] == 'Trailer'), None)

            # 2. GENERATE THE REASON (The "Why")
            # We look for overlapping Genre IDs between the Base Movie and the Recommendation
            matched_genres = [GENRE_NAMES[g_id] for g_id in selected.get('genre_ids', []) if g_id in base_genre_ids]

            # 3. Detailed Display
            print(f"\n🎬 {selected['title'].upper()} ({selected.get('release_date', '????')[:4]})")
            
            if fav_movie and matched_genres:
                # This only shows if you started with a "Base Movie"
                print(f"💡 REASON: Both movies are {', '.join(matched_genres)}")
            elif not fav_movie:
                print(f"💡 REASON: Matches your {theme_input} filters")
            
            print(f"🎭 Cast: {cast}")
            print(f"📝 Overview: {textwrap.fill(selected.get('overview', 'No description.'), width=70)}")
            
            # 4. Interactive Options
            if trailer_key:
                if input("\n▶️ Watch trailer? (y/n): ").lower() == 'y':
                    webbrowser.open(f"https://www.youtube.com/watch?v={trailer_key}")
            
            if input("💾 Add to watchlist? (y/n): ").lower() == 'y':
                add_to_watchlist(f"{selected['title']} ({selected.get('release_date')[:4]})")
            
            print("\n" + "-"*40)
            print("Returning to list...")
        else:
            print("Invalid selection. Try again.")

# Keep this at the very bottom
if __name__ == "__main__":
    main()