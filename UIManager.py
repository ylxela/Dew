import tkinter as tk
from tkinter import messagebox, ttk
import time
import threading

POPUP_INTERVAL = 1 * 5      # 1 hour in seconds
POPUP_DURATION = 1 * 3       # 2 minutes in seconds

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

        ttk.Button(popup, text="Drink", command=logWater).pack(pady=5)

    def runReminder(self):
        self.pet.window.after(POPUP_INTERVAL * 1000, self.show_popup)

    def show_popup(self):
        if self.popup_visible:
            return

        self.popup = tk.Toplevel(self.pet.window)
        self.popup.title("Hourly Reminder")
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.popup.configure(bg="lightyellow")

        label = tk.Label(self.popup, text="Time to drink water!", font=("Arial", 14), bg="lightyellow")
        label.pack(expand=True, fill="both")

        self.popup_visible = True
        self.updatePopUpPosition()

        self.pet.window.after(POPUP_DURATION * 1000, self.close_popup)

        self.pet.window.after(POPUP_INTERVAL * 1000, self.show_popup)

    def updatePopUpPosition(self):
        if not self.popup or not self.popup_visible:
            return

        popup_width = 300
        popup_height = 150

        pet_x = self.pet.x
        pet_y = self.pet.y
        pet_width = self.pet.petWidth

        popup_x = pet_x + (pet_width // 2) - (popup_width // 2)
        popup_y = pet_y - popup_height - 10

        self.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        # Keep tracking position
        self.pet.window.after(100, self.updatePopUpPosition)

    def close_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
            self.popup_visible = False
