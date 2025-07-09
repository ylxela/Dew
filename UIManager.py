import tkinter as tk
from tkinter import messagebox, ttk
import time

POPUP_INTERVAL = 1 * 5      # 1 hour in seconds
POPUP_DURATION = 1 * 3       # 2 minutes in seconds

# Manages UI windows and dialogs.
class UIManager:
    def __init__(self, pet):
        self.pet = pet
        self.popUpVisible = False
        self.popup = None

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
            self.pet.config.lastIntakeTime = time.time()
            progress["value"] = self.pet.config.currentIntake
            progLabel.config(text = f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
            if self.pet.config.currentIntake >= self.pet.config.dailyGoal:
                messagebox.showinfo("Congrats!", "You've met today's hydration goal!")
            popup.destroy()

        ttk.Button(popup, text="Drink", command=logWater).pack(pady=5)

    def runReminder(self):
        self.pet.window.after(POPUP_INTERVAL * 1000, self.showPopUp)

    def showPopUp(self):
        self.pet.behaviour.setBehaviour(2)
        if self.popUpVisible:
            return

        last_time = self.pet.config.lastIntakeTime or 0  # handle None
        time_since_last_intake = time.time() - last_time

        if time_since_last_intake < POPUP_INTERVAL:
            self.pet.window.after(1000, self.runReminder)
            return

        self.popup = tk.Toplevel(self.pet.window)
        self.popup.title("Hourly Reminder")
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        transparent_color = "magenta"
        self.popup.configure(bg=transparent_color)
        self.popup.attributes("-transparentcolor", transparent_color)

        photo = tk.PhotoImage(file="thirsty.gif")
        self.photo = photo.subsample(5, 5)

        image_label = tk.Label(self.popup, image=self.photo, bg=transparent_color)
        image_label.pack()

        self.popUpVisible = True
        self.updatePopUpPosition()

        self.pet.window.after(POPUP_DURATION * 1000, self.close_popup)
        self.pet.window.after(POPUP_INTERVAL * 1000, self.showPopUp)


    def updatePopUpPosition(self):
        if not self.popup or not self.popUpVisible:
            return

        popup_width = 200
        popup_height = 100

        pet_x = self.pet.x
        pet_y = self.pet.y
        pet_width = self.pet.petWidth

        popup_x = pet_x + (pet_width // 2) - (popup_width // 2)
        popup_y = pet_y - popup_height + 50

        self.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        # Keep tracking position
        self.pet.window.after(100, self.updatePopUpPosition)

    def close_popup(self):
        if self.popup:
            self.pet.behaviour.setBehaviour(0)
            self.popup.destroy()
            self.popup = None
            self.popUpVisible = False
