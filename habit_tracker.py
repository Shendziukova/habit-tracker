import json, os, tkinter as tk

DATA = os.path.join(os.path.expanduser("~"), ".habit_tracker.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("400x600")
        self.habits = self.load()

        tk.Label(self, text="Habit Tracker", font=("Helvetica", 18, "bold")).pack(pady=10)

        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)
        self.entry = tk.Entry(top, font=("Helvetica", 13))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.add())
        tk.Button(top, text="Add", command=self.add).pack(side="left", padx=5)

        self.listbox = tk.Listbox(self, font=("Helvetica", 12))
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        btnrow = tk.Frame(self)
        btnrow.pack(pady=10)
        tk.Button(btnrow, text="Toggle Done", command=self.toggle).pack(side="left", padx=5)
        tk.Button(btnrow, text="Delete", command=self.delete).pack(side="left", padx=5)

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
        if not v:
            return
        self.habits.append({"name": v, "done": False})
        self.entry.delete(0, "end")
        self.save()
        self.render()

    def toggle(self):
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        self.habits[i]["done"] = not self.habits[i]["done"]
        self.save(); self.render()

    def delete(self):
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        del self.habits[i]
        self.save(); self.render()

    def render(self):
        self.listbox.delete(0, "end")
        for h in self.habits:
            mark = "[x]" if h["done"] else "[ ]"
            self.listbox.insert("end", f"{mark} {h['name']}")

if __name__ == "__main__":
    App().mainloop()
