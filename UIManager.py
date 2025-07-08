import tkinter as tk
from tkinter import messagebox, ttk

class UIManager:
    """Manages UI windows and dialogs."""

    def __init__(self, pet_instance):
        self.pet = pet_instance

    def open_setup_window(self):
        """Open setup window to change daily goal and sip size."""
        win = tk.Toplevel(self.pet.window)
        win.title("Dew - Setup")
        win.attributes("-topmost", True)

        tk.Label(win, text="Daily Goal (ml)").grid(row=0, column=0, padx=10, pady=5)
        goal_var = tk.StringVar(value=str(self.pet.config.dailyGoal))
        tk.Entry(win, textvariable=goal_var, width=10).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(win, text="Sip Amount (ml)").grid(row=1, column=0, padx=10, pady=5)
        sip_var = tk.StringVar(value=str(self.pet.config.sipAmount))
        tk.Entry(win, textvariable=sip_var, width=10).grid(row=1, column=1, padx=10, pady=5)

        def save():
            try:
                self.pet.config.dailyGoal = int(goal_var.get())
                self.pet.config.sipAmount = int(sip_var.get())
                messagebox.showinfo("Saved", "Preferences updated.")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")

        ttk.Button(win, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

    def open_logging_window(self):
        """Open water logging window."""
        popup = tk.Toplevel(self.pet.window)
        popup.title("Log Water")
        popup.attributes("-topmost", True)
        popup.geometry(f"200x120+{self.pet.x+110}+{self.pet.y}")

        tk.Label(popup, text=f"Log {self.pet.config.sipAmount} ml water?").pack(pady=5)

        progress = ttk.Progressbar(popup, maximum=self.pet.config.dailyGoal,
                                  value=self.pet.config.currentIntake, length=160)
        progress.pack(pady=5)

        prog_label = tk.Label(popup, text=f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
        prog_label.pack()

        def log_water():
            self.pet.config.addIntake(self.pet.config.sipAmount)
            progress["value"] = self.pet.config.currentIntake
            prog_label.config(text=f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
            if self.pet.config.currentIntake >= self.pet.config.dailyGoal:
                messagebox.showinfo("Congrats!", "You've met today's hydration goal!")
            popup.destroy()

        ttk.Button(popup, text="Drink", command=log_water).pack(pady=5)