import requests
import json

# AniList does NOT require a token for general browsing (public data),
# which makes this explorer very easy for others to test!
BASE_URL = "https://graphql.anilist.co"

def run_query(query, variables=None):
    """Helper function to send GraphQL requests"""
    response = requests.post(BASE_URL, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Query failed with code {response.status_code}")
        return None

def explore_anilist():
    while True:
        print("\n" + "="*35)
        print("🌸 ANILIST DATABASE EXPLORER (GraphQL)")
        print("="*35)
        print("1. View Official Anime Genres & Tags")
        print("2. View Trending Anime This Season")
        print("3. View Top Voice Actors (Seiyuu)")
        print("4. View Top Animation Studios")
        print("5. Exit Explorer")
        
        choice = input("\nEnter number (1-5): ")

        if choice == '1':
            # Queries the GenreCollection and MediaTagCollection
            query = """
            query {
              GenreCollection
              MediaTagCollection { name }
            }
            """
            data = run_query(query)
            if data:
                print("\n📂 OFFICIAL GENRES:")
                print(", ".join(data['data']['GenreCollection']))
                print(f"\n🏷️ TOTAL TAGS AVAILABLE: {len(data['data']['MediaTagCollection'])}")

        elif choice == '2':
            # Queries for the top 10 trending shows right now
            query = """
            query {
              Page(perPage: 10) {
                media(sort: TRENDING_DESC, type: ANIME) {
                  title { english romaji }
                  averageScore
                  format
                }
              }
            }
            """
            data = run_query(query)
            if data:
                print("\n📈 CURRENTLY TRENDING ANIME:")
                for anime in data['data']['Page']['media']:
                    title = anime['title']['english'] or anime['title']['romaji']
                    score = anime['averageScore'] or "N/A"
                    print(f"[{score}%] {title[:40]:<40} | Format: {anime['format']}")

        elif choice == '3':
            # Queries for popular Voice Actors
            query = """
            query {
              Page(perPage: 10) {
                staff(sort: FAVOURITES_DESC) {
                  name { full }
                  primaryOccupations
                }
              }
            }
            """
            data = run_query(query)
            if data:
                print("\n🎙️ MOST FAVORITED VOICE ACTORS/STAFF:")
                for person in data['data']['Page']['staff']:
                    occ = person['primaryOccupations'][0] if person['primaryOccupations'] else "Staff"
                    print(f"Name: {person['name']['full']:<25} | Primary Role: {occ}")

        elif choice == '4':
            # Queries for top Animation Studios
            query = """
            query {
              Page(perPage: 10) {
                studios(sort: FAVOURITES_DESC) {
                  name
                  favourites
                }
              }
            }
            """
            data = run_query(query)
            if data:
                print("\n🎨 TOP ANIMATION STUDIOS:")
                for studio in data['data']['Page']['studios']:
                    print(f"Studio: {studio['name']:<25} | Fans: {studio['favourites']}")

        elif choice == '5':
            print("👋 Closing AniList explorer. Sayonara!")
            break
        
        else:
            print("⚠️ Invalid choice. Please pick 1-5.")

if __name__ == "__main__":
    explore_anilist()