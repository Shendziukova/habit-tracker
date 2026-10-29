import json, os, tkinter as tk
from tkinter import ttk

DATA = os.path.join(os.path.expanduser("~"), ".habit_tracker.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("420x640")
        self.configure(bg="#0f172a")
        self.habits = self.load()
        top = tk.Frame(self, bg="#0f172a"); top.pack(fill="x", padx=20, pady=20)
        self.entry = tk.Entry(top, font=("Segoe UI", 12)); self.entry.pack(side="left", fill="x", expand=True)
        tk.Button(top, text="Add", command=self.add, bg="#3b82f6", fg="white").pack(side="left", padx=8)
        self.listbox = tk.Frame(self, bg="#0f172a"); self.listbox.pack(fill="both", expand=True, padx=20)
        self.render()

    def load(self):
        try:
            with open(DATA) as f: return json.load(f)
        except: return []

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
        for w in self.listbox.winfo_children(): w.destroy()
        for i, h in enumerate(self.habits):
            row = tk.Frame(self.listbox, bg="#1e293b", pady=8); row.pack(fill="x", pady=4)
            var = tk.BooleanVar(value=h["done"])
            cb = tk.Checkbutton(row, variable=var, command=lambda i=i: self.toggle(i), bg="#1e293b", fg="#e2e8f0", selectcolor="#1e293b")
            cb.pack(side="left", padx=8)
            lbl = tk.Label(row, text=h["name"], bg="#1e293b", fg="#e2e8f0", font=("Segoe UI", 12))
            if h["done"]: lbl.config(fg="#64748b")
            lbl.pack(side="left", fill="x", expand=True)
            tk.Button(row, text="x", command=lambda i=i: self.delete(i), bg="#ef4444", fg="white").pack(side="right", padx=8)

if __name__ == "__main__":
    App().mainloop()
