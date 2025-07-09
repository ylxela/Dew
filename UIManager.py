import tkinter as tk
from tkinter import messagebox, ttk

# Manages UI windows and dialogs.
class UIManager:
    def __init__(self, pet):
        self.pet = pet

    def openSetup(self):
        win = tk.Toplevel(self.pet.window)
        win.title("Dew - Setup")
        win.attributes("-topmost", True)

        tk.Label(win, text = "Daily Goal (ml)").grid(row = 0, column = 0, padx = 10, pady = 5)
        goalVar = tk.StringVar(value = str(self.pet.config.dailyGoal))
        tk.Entry(win, textvariable = goalVar, width = 10).grid(row = 0, column = 1, padx = 10, pady = 5)

        tk.Label(win, text = "Sip Amount (ml)").grid(row = 1, column = 0, padx = 10, pady = 5)
        sipVar = tk.StringVar(value = str(self.pet.config.sipAmount))
        tk.Entry(win, textvariable = sipVar, width = 10).grid(row = 1, column = 1, padx = 10, pady = 5)

        def save():
            try:
                self.pet.config.dailyGoal = int(goalVar.get())
                self.pet.config.sipAmount = int(sipVar.get())
                messagebox.showinfo("Saved", "Preferences updated.")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        ttk.Button(win, text = "Save", command = save).grid(row = 2, column = 0, columnspan = 2, pady = 10)

    def openLog(self):
        popup = tk.Toplevel(self.pet.window)
        popup.title("Log Water")
        popup.attributes("-topmost", True)
        popup.geometry(f"200x120+{self.pet.x+110}+{self.pet.y}")

        tk.Label(popup, text = f"Log {self.pet.config.sipAmount} ml water?").pack(pady = 5)

        progress = ttk.Progressbar(popup, maximum = self.pet.config.dailyGoal,
                                  value = self.pet.config.currentIntake, length = 160)
        progress.pack(pady = 5)

        progLabel = tk.Label(popup, text = f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
        progLabel.pack()

        def logWater():
            self.pet.config.addIntake(self.pet.config.sipAmount)
            progress["value"] = self.pet.config.currentIntake
            progLabel.config(text = f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
            if self.pet.config.currentIntake >= self.pet.config.dailyGoal:
                messagebox.showinfo("Congrats!", "You've met today's hydration goal!")
            popup.destroy()

        ttk.Button(popup, text = "Drink", command = logWater).pack(pady = 5)