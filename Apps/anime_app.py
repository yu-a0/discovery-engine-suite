import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO

# ==========================================
# ⚙️ 1. ANILIST API CONFIG
# ==========================================
ANILIST_URL = 'https://graphql.anilist.co'

SEARCH_QUERY = '''
query ($search: String, $genre: String, $year: Int) {
  Page(perPage: 15) {
    media(search: $search, genre: $genre, seasonYear: $year, type: ANIME, sort: POPULARITY_DESC) {
      id
      title { romaji english }
      genres
      averageScore
      description
      coverImage { large }
      recommendations {
        nodes {
          mediaRecommendation {
            id
            title { romaji english }
            genres
            averageScore
            description
            coverImage { large }
          }
        }
      }
    }
  }
}
'''

class AnimeEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AniList Discovery Engine (Draggable Sidebar)")
        self.root.geometry("1200x850")
        self.root.configure(bg="#0b1622") 
        
        self.current_results = []
        self.base_genres = []

        # ==========================================
        # 🏗️ 2. THE PANED WINDOW (DRAGGABLE DIVIDER)
        # ==========================================
        # This creates the "split" container
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#0b1622", sashwidth=4, sashpad=2)
        self.paned_window.pack(fill="both", expand=True)

        # --- LEFT PANEL: SIDEBAR ---
        self.left_frame = tk.Frame(self.paned_window, bg="#151f2e", width=400)
        
        # --- RIGHT PANEL: DISPLAY ---
        self.right_frame = tk.Frame(self.paned_window, bg="#0b1622")

        # Add them to the PanedWindow
        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.right_frame)

        # ==========================================
        # ⬅️ 3. SIDEBAR CONTENT
        # ==========================================
        tk.Label(self.left_frame, text="ANIME FILTERS", 
                 font=("Arial", 14, "bold"), fg="#74b9df", bg="#151f2e").pack(pady=15)

        self.create_label_entry("Base Anime (for Recs):", "entry_anime")
        self.create_label_entry("Year:", "entry_year")
        self.create_label_entry("Genre:", "entry_genre")

        self.search_btn = tk.Button(self.left_frame, text="SEARCH ANILIST", 
                                   command=self.perform_search, 
                                   bg="#188cca", fg="white", 
                                   font=("Arial", 11, "bold"), height=2)
        self.search_btn.pack(fill="x", padx=20, pady=20)

        # Listbox with horizontal and vertical scroll
        self.list_container = tk.Frame(self.left_frame, bg="#0b1622")
        self.list_container.pack(fill="both", expand=True, padx=20, pady=5)

        self.x_scroll = tk.Scrollbar(self.list_container, orient="horizontal")
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll = tk.Scrollbar(self.list_container, orient="vertical")
        self.y_scroll.pack(side="right", fill="y")

        self.results_list = tk.Listbox(self.list_container, bg="#0b1622", fg="white", 
                                      font=("Arial", 11), borderwidth=0, highlightthickness=0,
                                      xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        
        self.x_scroll.config(command=self.results_list.xview)
        self.y_scroll.config(command=self.results_list.yview)
        self.results_list.pack(side="left", fill="both", expand=True)
        self.results_list.bind('<<ListboxSelect>>', self.on_select_anime)

        # ==========================================
        # ➡️ 4. DISPLAY WINDOW CONTENT
        # ==========================================
        self.poster_label = tk.Label(self.right_frame, bg="#0b1622")
        self.poster_label.pack(side="top", pady=10)

        self.action_frame = tk.Frame(self.right_frame, bg="#0b1622", height=100)
        self.action_frame.pack(side="bottom", fill="x", pady=20)

        self.detail_area = scrolledtext.ScrolledText(self.right_frame, bg="#0b1622", fg="#9fadbd", 
                                                    font=("Arial", 12), borderwidth=0, wrap=tk.WORD)
        self.detail_area.pack(side="top", fill="both", expand=True, padx=30)

        self.root.bind('<Return>', lambda event: self.perform_search())

    # --- THE REST OF THE FUNCTIONS (Same as before) ---

    def create_label_entry(self, label_text, var_name):
        tk.Label(self.left_frame, text=label_text, fg="#9fadbd", bg="#151f2e").pack(anchor="w", padx=20)
        if var_name == "entry_anime":
            self.anime_text_var = tk.StringVar()
            self.anime_text_var.trace_add("write", self.on_type_suggestion)
            entry = tk.Entry(self.left_frame, textvariable=self.anime_text_var, bg="#0b1622", fg="white", insertbackground="white", borderwidth=0)
            self.suggestion_menu = tk.Menu(self.root, tearoff=0, bg="#151f2e", fg="white", font=("Arial", 10))
        else:
            entry = tk.Entry(self.left_frame, bg="#0b1622", fg="white", insertbackground="white", borderwidth=0)
        entry.pack(fill="x", padx=20, pady=(0, 15), ipady=7)
        setattr(self, var_name, entry)

    def on_type_suggestion(self, *args):
        text = self.anime_text_var.get()
        if len(text) < 3:
            self.suggestion_menu.unpost()
            return
        query = 'query ($s: String) { Page(perPage: 5) { media(search: $s, type: ANIME) { title { english romaji } } } }'
        try:
            response = requests.post(ANILIST_URL, json={'query': query, 'variables': {'s': text}})
            results = response.json()['data']['Page']['media']
            if results:
                self.suggestion_menu.delete(0, tk.END)
                for item in results:
                    name = item['title']['english'] if item['title']['english'] else item['title']['romaji']
                    self.suggestion_menu.add_command(label=name, command=lambda n=name: self.select_suggestion(n))
                x = self.entry_anime.winfo_rootx()
                y = self.entry_anime.winfo_rooty() + self.entry_anime.winfo_height()
                self.suggestion_menu.post(x, y)
        except: pass

    def select_suggestion(self, name):
        self.anime_text_var.set(name)
        self.suggestion_menu.unpost()

    def perform_search(self):
        anime_name = self.entry_anime.get()
        year_val = self.entry_year.get()
        genre_val = self.entry_genre.get().capitalize()
        variables = {"search": anime_name if anime_name else None, "genre": genre_val if genre_val else None, 
                     "year": int(year_val) if year_val and year_val.isdigit() else None}
        try:
            response = requests.post(ANILIST_URL, json={'query': SEARCH_QUERY, 'variables': variables})
            data = response.json()['data']['Page']['media']
            if not data:
                messagebox.showwarning("No Results", "No anime found.")
                return
            if anime_name and data[0]['recommendations']['nodes']:
                base_anime = data[0]
                self.base_genres = base_anime['genres']
                raw_recs = [node['mediaRecommendation'] for node in base_anime['recommendations']['nodes'] if node['mediaRecommendation']]
                base_t = (base_anime['title']['english'] or base_anime['title']['romaji']).lower()
                self.current_results = [r for r in raw_recs if base_t not in (r['title']['english'] or "").lower()]
            else:
                self.current_results = data
                self.base_genres = []
            self.results_list.delete(0, tk.END)
            for anime in self.current_results:
                display_name = anime['title']['english'] if anime['title']['english'] else anime['title']['romaji']
                self.results_list.insert(tk.END, f" {display_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def on_select_anime(self, event):
        if not self.results_list.curselection(): return
        index = self.results_list.curselection()[0]
        anime = self.current_results[index]

        self.detail_area.delete('1.0', tk.END)
        for widget in self.action_frame.winfo_children(): widget.destroy()

        if anime.get('coverImage'):
            resp = requests.get(anime['coverImage']['large'])
            img_data = Image.open(BytesIO(resp.content))
            photo = ImageTk.PhotoImage(img_data)
            self.poster_label.config(image=photo)
            self.poster_label.image = photo

        matched = [g for g in anime['genres'] if g in self.base_genres]
        reason_text = f"💡 REASON: Both are {', '.join(matched)}\n\n" if matched else ""
        
        eng, rom = anime['title']['english'], anime['title']['romaji']
        full_title = f"{eng}\n({rom})" if eng and rom and eng.lower() != rom.lower() else (eng if eng else rom)
        desc = anime.get('description', '').replace('<br>', '\n').replace('<i>', '').replace('</i>', '')

        self.detail_area.insert(tk.END, f"{full_title.upper()}\n", "title")
        self.detail_area.insert(tk.END, reason_text, "reason")
        self.detail_area.insert(tk.END, f"⭐ Rating: {anime.get('averageScore', '??')}/100\n\n")
        self.detail_area.insert(tk.END, desc)
        
        self.detail_area.tag_config("title", font=("Arial", 20, "bold"), foreground="#3db4f2")
        self.detail_area.tag_config("reason", font=("Arial", 11, "italic"), foreground="#FFD700")

        tk.Button(self.action_frame, text="VIEW ON ANILIST", bg="#189ae0", fg="white", font=("Arial", 10, "bold"),
                  command=lambda: webbrowser.open(f"https://anilist.co/anime/{anime['id']}")).pack(side="left", padx=10, expand=True)
        
        tk.Button(self.action_frame, text="SAVE TO MY LIST", bg="#FFD700", fg="#0b1622", font=("Arial", 10, "bold"),
                  command=lambda: self.save_to_file(anime)).pack(side="left", padx=10, expand=True)

    def save_to_file(self, anime):
        name = anime['title']['english'] if anime['title']['english'] else anime['title']['romaji']
        with open("anime_watchlist.txt", "a", encoding="utf-8") as f:
            f.write(f"{name}\n")
        messagebox.showinfo("Saved!", f"'{name}' added!")

def main():
    root = tk.Tk()
    app = AnimeEngineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    import hupper
    reloader = hupper.start_reloader('anime_app.main') 
    main()