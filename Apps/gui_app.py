import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import os
import webbrowser
from dotenv import load_dotenv
from PIL import Image, ImageTk
from io import BytesIO

# ==========================================
# ⚙️ 1. INITIAL SETUP & API CONFIG
# ==========================================
load_dotenv()
API_TOKEN = os.getenv('TMDB_TOKEN')
BASE_URL = "https://api.themoviedb.org/3"
headers = {"accept": "application/json", "Authorization": f"Bearer {API_TOKEN}"}

GENRES = {
    "action": 28, "adventure": 12, "animation": 16, "comedy": 35, 
    "crime": 80, "documentary": 99, "drama": 18, "family": 10751, 
    "fantasy": 14, "history": 36, "horror": 27, "music": 10402, 
    "mystery": 9648, "romance": 10749, "sci-fi": 878, "tv movie": 10770, 
    "thriller": 53, "war": 10752, "western": 37
}
GENRE_NAMES = {v: k.capitalize() for k, v in GENRES.items()}

class MovieEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Discovery Engine Pro")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1a1a1a") 
        
        self.current_results = []
        self.base_genre_ids = []

        # ==========================================
        # 🏗️ 2. DRAGGABLE PANED WINDOW
        # ==========================================
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#1a1a1a", sashwidth=4)
        self.paned_window.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.paned_window, bg="#2d2d2d", width=400)
        self.right_frame = tk.Frame(self.paned_window, bg="#1a1a1a")

        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.right_frame)

        # ==========================================
        # ⬅️ 3. LEFT PANEL: CONTROLS & SIDEBAR
        # ==========================================
        tk.Label(self.left_frame, text="SEARCH FILTERS", 
                 font=("Arial", 14, "bold"), fg="#7FA2EC", bg="#2d2d2d").pack(pady=15)

        # Input Fields
        self.create_label_entry("Base Movie Title:", "entry_movie")
        self.create_label_entry("Year (Optional):", "entry_year")
        self.create_label_entry("Genre/Keyword:", "entry_theme")

        self.search_btn = tk.Button(self.left_frame, text="FIND MOVIES", 
                                   command=self.perform_search, 
                                   bg="#022C86", fg="white", 
                                   font=("Arial", 11, "bold"), height=2)
        self.search_btn.pack(fill="x", padx=20, pady=20)

        # Results Listbox with Scrollbars
        self.list_container = tk.Frame(self.left_frame, bg="#1e1e1e")
        self.list_container.pack(fill="both", expand=True, padx=20, pady=5)

        self.x_scroll = tk.Scrollbar(self.list_container, orient="horizontal")
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll = tk.Scrollbar(self.list_container, orient="vertical")
        self.y_scroll.pack(side="right", fill="y")

        self.results_list = tk.Listbox(self.list_container, bg="#1e1e1e", fg="white", 
                                      font=("Arial", 11), borderwidth=0, highlightthickness=0,
                                      xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        
        self.x_scroll.config(command=self.results_list.xview)
        self.y_scroll.config(command=self.results_list.yview)
        self.results_list.pack(side="left", fill="both", expand=True)
        self.results_list.bind('<<ListboxSelect>>', self.on_select_movie)

        # ==========================================
        # ➡️ 4. RIGHT PANEL: ELASTIC DISPLAY
        # ==========================================
        # Poster Image (Fixed at Top)
        self.poster_label = tk.Label(self.right_frame, bg="#1a1a1a")
        self.poster_label.pack(side="top", pady=10)

        # Action Buttons (Locked to Bottom)
        self.action_frame = tk.Frame(self.right_frame, bg="#1a1a1a")
        self.action_frame.pack(side="bottom", fill="x", pady=20)

        # Description (Elastic Middle)
        self.detail_area = scrolledtext.ScrolledText(self.right_frame, bg="#1a1a1a", fg="white", 
                                                    font=("Arial", 12), borderwidth=0, wrap=tk.WORD)
        self.detail_area.pack(side="top", fill="both", expand=True, padx=30)

        # Global key binding for Enter
        self.root.bind('<Return>', lambda event: self.perform_search())

    # ==========================================
    # 🧠 5. HELPER & AUTOCOMPLETE LOGIC
    # ==========================================
    def create_label_entry(self, label_text, var_name):
        tk.Label(self.left_frame, text=label_text, fg="#bbb", bg="#2d2d2d").pack(anchor="w", padx=20)
        
        if var_name == "entry_movie":
            self.movie_text_var = tk.StringVar()
            self.movie_text_var.trace_add("write", self.on_type_suggestion)
            entry = tk.Entry(self.left_frame, textvariable=self.movie_text_var, bg="#3d3d3d", fg="white", insertbackground="white", borderwidth=0)
            self.suggestion_menu = tk.Menu(self.root, tearoff=0, bg="#2d2d2d", fg="white")
        else:
            entry = tk.Entry(self.left_frame, bg="#3d3d3d", fg="white", insertbackground="white", borderwidth=0)
            
        entry.pack(fill="x", padx=20, pady=(0, 10), ipady=5)
        setattr(self, var_name, entry)

    def on_type_suggestion(self, *args):
        text = self.movie_text_var.get()
        if len(text) < 3:
            self.suggestion_menu.unpost()
            return
        
        try:
            params = {"query": text}
            resp = requests.get(f"{BASE_URL}/search/movie", headers=headers, params=params).json()
            results = resp.get('results', [])[:5]
            if results:
                self.suggestion_menu.delete(0, tk.END)
                for movie in results:
                    name = movie['title']
                    self.suggestion_menu.add_command(label=name, command=lambda n=name: self.select_suggestion(n))
                
                x = self.entry_movie.winfo_rootx()
                y = self.entry_movie.winfo_rooty() + self.entry_movie.winfo_height()
                self.suggestion_menu.post(x, y)
        except: pass

    def select_suggestion(self, name):
        self.movie_text_var.set(name)
        self.suggestion_menu.unpost()

    # ==========================================
    # 🔎 6. SEARCH & SELECTION LOGIC
    # ==========================================
    def perform_search(self):
        fav_movie = self.entry_movie.get()
        year_filter = self.entry_year.get()
        theme_input = self.entry_theme.get().lower()
        target_genre_id = GENRES.get(theme_input)

        try:
            if fav_movie:
                s_res = requests.get(f"{BASE_URL}/search/movie", headers=headers, params={"query": fav_movie}).json()
                if not s_res.get('results'): return
                base_movie = s_res['results'][0]
                self.base_genre_ids = base_movie.get('genre_ids', [])
                recs = requests.get(f"{BASE_URL}/movie/{base_movie['id']}/recommendations", headers=headers).json().get('results', [])
                
                self.current_results = [m for m in recs if base_movie['title'].lower() not in m['title'].lower()]
                if not self.current_results: self.current_results = recs
            else:
                params = {"primary_release_year": year_filter, "with_genres": target_genre_id, "sort_by": "popularity.desc"}
                res = requests.get(f"{BASE_URL}/discover/movie", headers=headers, params=params).json()
                self.current_results = res.get('results', [])

            self.results_list.delete(0, tk.END)
            for m in self.current_results[:15]:
                self.results_list.insert(tk.END, f" {m['title']} ({m.get('release_date', '????')[:4]})")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select_movie(self, event):
        if not self.results_list.curselection(): return
        index = self.results_list.curselection()[0]
        movie = self.current_results[index]

        self.detail_area.delete('1.0', tk.END)
        for widget in self.action_frame.winfo_children(): widget.destroy()

        # Fetch Trailer
        v_res = requests.get(f"{BASE_URL}/movie/{movie['id']}/videos", headers=headers).json()
        trailer_key = next((v['key'] for v in v_res.get('results', []) if v['type'] == 'Trailer'), None)
        
        # Poster Image
        if movie.get('poster_path'):
            img_url = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
            response = requests.get(img_url)
            img_data = Image.open(BytesIO(response.content))
            photo = ImageTk.PhotoImage(img_data)
            self.poster_label.config(image=photo)
            self.poster_label.image = photo 

        # Reasons
        matched = [GENRE_NAMES[g_id] for g_id in movie.get('genre_ids', []) if g_id in self.base_genre_ids]
        reason_text = f"💡 REASON: Shared Genres ({', '.join(matched)})\n\n" if matched else ""

        # Render Content
        self.detail_area.insert(tk.END, f"{movie['title'].upper()}\n", "title")
        self.detail_area.insert(tk.END, reason_text, "reason")
        self.detail_area.insert(tk.END, f"Rating: {movie['vote_average']}/10\n\n")
        self.detail_area.insert(tk.END, movie.get('overview', 'No description.'))
        
        self.detail_area.tag_config("title", font=("Arial", 20, "bold"), foreground="#7FA2EC")
        self.detail_area.tag_config("reason", font=("Arial", 11, "italic"), foreground="#bbb")

        # Buttons
        if trailer_key:
            tk.Button(self.action_frame, text="WATCH TRAILER", bg="#DA1C1C", fg="white", font=("Arial", 10, "bold"),
                      command=lambda: webbrowser.open(f"https://www.youtube.com/watch?v={trailer_key}")).pack(side="left", padx=10, expand=True)
        
        tk.Button(self.action_frame, text="SAVE TO WATCHLIST", bg="#FFD700", fg="#1a1a1a", font=("Arial", 10, "bold"),
                  command=lambda: self.save_to_file(movie)).pack(side="left", padx=10, expand=True)

    def save_to_file(self, movie):
        with open("watchlist.txt", "a", encoding="utf-8") as f:
            f.write(f"{movie['title']} ({movie.get('release_date', '????')[:4]})\n")
        messagebox.showinfo("Saved", f"'{movie['title']}' added to watchlist!")

# ==========================================
# 🚀 7. BOOTSTRAP
# ==========================================
def main():
    root = tk.Tk()
    app = MovieEngineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    import hupper
    reloader = hupper.start_reloader('gui_app.main') 
    main()