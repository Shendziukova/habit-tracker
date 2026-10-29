import json, os, tkinter as tk
from tkinter import ttk

DATA = os.path.join(os.path.expanduser("~"), ".habit_tracker.json")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("460x700")
        self.minsize(400, 500)
        self.configure(bg="#0f172a")
        self.habits = self.load()

        header = tk.Label(self, text="Habit Tracker", font=("Segoe UI", 20, "bold"),
                          bg="#0f172a", fg="#e2e8f0")
        header.pack(pady=(20, 10))

        top = tk.Frame(self, bg="#0f172a")
        top.pack(fill="x", padx=20, pady=10)
        self.entry = tk.Entry(top, font=("Segoe UI", 13), bg="#1e293b", fg="#e2e8f0",
                              insertbackground="#e2e8f0", relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<Return>", lambda e: self.add())
        addbtn = tk.Button(top, text="Add", command=self.add, bg="#3b82f6", fg="white",
                           relief="flat", padx=16, pady=6, cursor="hand2")
        addbtn.pack(side="left", padx=(10, 0))

        self.canvas = tk.Canvas(self, bg="#0f172a", highlightthickness=0)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg="#0f172a")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20)
        self.scroll.pack(side="right", fill="y")

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

    def toggle(self, i):
        self.habits[i]["done"] = not self.habits[i]["done"]
        self.save()
        self.render()

    def delete(self, i):
        del self.habits[i]
        self.save()
        self.render()

    def render(self):
        for w in self.inner.winfo_children():
            w.destroy()
        for i, h in enumerate(self.habits):
            row = tk.Frame(self.inner, bg="#1e293b", pady=8)
            row.pack(fill="x", pady=4)
            var = tk.BooleanVar(value=h["done"])
            cb = tk.Checkbutton(row, variable=var, command=lambda i=i: self.toggle(i),
                                bg="#1e293b", fg="#e2e8f0", selectcolor="#1e293b",
                                activebackground="#1e293b")
            cb.pack(side="left", padx=8)
            lbl = tk.Label(row, text=h["name"], bg="#1e293b", fg="#e2e8f0",
                           font=("Segoe UI", 12), anchor="w")
            if h["done"]:
                lbl.config(fg="#64748b")
            lbl.pack(side="left", fill="x", expand=True, padx=4)
            tk.Button(row, text="x", command=lambda i=i: self.delete(i),
                      bg="#ef4444", fg="white", relief="flat", padx=10).pack(side="right", padx=8)

if __name__ == "__main__":
    App().mainloop()
