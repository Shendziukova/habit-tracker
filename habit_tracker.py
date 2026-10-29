import json, os, tkinter as tk

DATA = os.path.join(os.path.expanduser("~"), ".habit_tracker.json")
BG = "#0b1220"; CARD = "#151f32"; ACCENT = "#6366f1"; TEXT = "#e5e7eb"; MUTED = "#94a3b8"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("440x720")
        self.minsize(380, 500)
        self.configure(bg=BG)
        self.habits = self.load()

        tk.Label(self, text="Habit Tracker", font=("Helvetica", 22, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(24, 4))
        self.subtitle = tk.Label(self, text="", font=("Helvetica", 11), bg=BG, fg=MUTED)
        self.subtitle.pack(pady=(0, 16))

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=22, pady=(0, 14))
        self.entry = tk.Entry(top, font=("Helvetica", 13), bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat", bd=0)
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, ipadx=12)
        self.entry.bind("<Return>", lambda e: self.add())
        self.entry.focus_set()
        _btn = tk.Button(top, text="+ Add", command=self.add, bg=ACCENT, fg="white",
                  relief="flat", font=("Helvetica", 12, "bold"), padx=18, pady=8,
                  cursor="hand2", activebackground="#4f46e5", activeforeground="white"
                  )
        _btn.pack(side="left", padx=(12, 0))
        _btn.bind("<Button-1>", lambda e: self.add())

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw", width=400)
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=22)
        sb.pack(side="right", fill="y", padx=(0, 8))

        self.render()

    def load(self):
        try:
            with open(DATA) as f: return json.load(f)
        except Exception:
            return []

    def save(self):
        with open(DATA, "w") as f: json.dump(self.habits, f)

    def add(self):
        v = self.entry.get().strip()
        if not v: return
        self.habits.append({"name": v, "done": False})
        self.entry.delete(0, "end")
        self.save(); self.render()

    def toggle(self, i):
        self.habits[i]["done"] = not self.habits[i]["done"]
        self.save(); self.render()

    def delete(self, i):
        del self.habits[i]
        self.save(); self.render()

    def render(self):
        for w in self.inner.winfo_children(): w.destroy()
        done = sum(1 for h in self.habits if h["done"])
        total = len(self.habits)
        self.subtitle.config(text=f"{done} of {total} done today" if total else "Add your first habit")
        if not self.habits:
            tk.Label(self.inner, text="No habits yet", font=("Helvetica", 12),
                     bg=BG, fg=MUTED).pack(pady=40)
            return
        for i, h in enumerate(self.habits):
            card = tk.Frame(self.inner, bg=CARD)
            card.pack(fill="x", pady=6, ipady=4)
            var = tk.BooleanVar(value=h["done"])
            cb = tk.Checkbutton(card, variable=var, command=lambda i=i: self.toggle(i),
                                bg=CARD, fg=TEXT, selectcolor=CARD, activebackground=CARD,
                                font=("Helvetica", 13))
            cb.pack(side="left", padx=(12, 6))
            name = tk.Label(card, text=h["name"], font=("Helvetica", 13), bg=CARD,
                            fg=TEXT if not h["done"] else MUTED, anchor="w")
            if h["done"]:
                name.config(font=("Helvetica", 13, "overstrike"))
            name.pack(side="left", fill="x", expand=True, pady=8)
            tk.Button(card, text="✕", command=lambda i=i: self.delete(i),
                      bg=CARD, fg=MUTED, relief="flat", font=("Helvetica", 12),
                      activebackground=CARD, activeforeground="#ef4444", cursor="hand2"
                      ).pack(side="right", padx=12)

if __name__ == "__main__":
    App().mainloop()
