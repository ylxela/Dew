import tkinter as tk
from tkinter import messagebox, ttk
import time
import os

POPUP_INTERVAL = 1 * 5      # 1 hour in seconds
POPUP_DURATION = 1 * 3       # 2 minutes in seconds

# Manages UI windows and dialogs.
class UIManager:
    def __init__(self, pet):
        self.pet = pet
        self.popUpVisible = False
        self.popup = None
        self.preferences_window = None
        self.bg_frames = []
        self.bg_current_frame = 0
        self.bg_label = None
        self.bg_animation_running = False
        self.hamster_img = None

    def load_background_frames(self):
        """Load all frames of the background GIF"""
        try:
            self.bg_frames = []
            frame_index = 0
            
            while True:
                try:
                    frame = tk.PhotoImage(file='assets/water logger.gif', format='gif -index %i' % frame_index)
                    # Scale the frame to fit the window (1400x1060)
                    scaled_frame = frame.zoom(2, 2)  # Adjust scaling factor as needed
                    self.bg_frames.append(scaled_frame)
                    frame_index += 1
                except tk.TclError:
                    # No more frames
                    break
            
            return len(self.bg_frames) > 0
        except Exception as e:
            print(f"Error loading background frames: {e}")
            return False

    def animate_background(self):
        """Animate the background GIF"""
        if not self.bg_animation_running or not self.bg_frames or not self.bg_label:
            return
            
        # Update the label with the current frame
        current_frame = self.bg_frames[self.bg_current_frame]
        self.bg_label.configure(image=current_frame)
        
        # Move to next frame
        self.bg_current_frame = (self.bg_current_frame + 1) % len(self.bg_frames)
        
        # Schedule next frame update
        if self.preferences_window and self.preferences_window.winfo_exists():
            self.preferences_window.after(200, self.animate_background)

    def stop_background_animation(self):
        """Stop the background animation"""
        self.bg_animation_running = False
        self.bg_current_frame = 0
        self.bg_label = None

    def openSetup(self):
        """Popup window to change daily goal and sip size with revamped UI."""
        # Close existing window if it exists
        if self.preferences_window is not None:
            self.stop_background_animation()
            self.preferences_window.destroy()
            
        # Create top-level window
        self.preferences_window = tk.Toplevel(self.pet.window)
        self.preferences_window.title("Preferences")
        self.preferences_window.geometry("1400x1060")
        self.preferences_window.resizable(False, False)
        self.preferences_window.attributes("-topmost", True)
        # Ensure it always stays above pet
        self.preferences_window.lift(self.pet.window)

        # Load hamster image
        try:
            self.hamster_img = tk.PhotoImage(file="assets/water logging hamster.png")
        except Exception:
            self.hamster_img = None

        # Set up animated background
        if os.path.exists("assets/water logger.gif") and self.load_background_frames():
            # Display animated background using a label that updates
            self.bg_label = tk.Label(self.preferences_window)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Start background animation
            self.bg_animation_running = True
            self.animate_background()
        else:
            # Fallback background color
            self.preferences_window.configure(bg='#4A90E2')

        # Load font (Press Start 2P) if installed, else default
        try:
            import tkinter.font as tkfont
            press_start_font = tkfont.Font(family="Press Start 2P", size=12)
        except Exception:
            press_start_font = None

        # Central panel (semi-transparent)
        panel_width = 800
        panel_height = 600
        panel_x = (1400 - panel_width) // 2
        panel_y = (1060 - panel_height) // 2 + 80  # leave space for hamster
        # Create canvas to draw rounded rectangle panel
        canvas = tk.Canvas(self.preferences_window, width=panel_width, height=panel_height, highlightthickness=0)
        canvas.place(x=panel_x, y=panel_y)
        # Draw rectangle (rounded corners are limited in Tk)
        canvas.create_rectangle(0, 0, panel_width, panel_height, fill="#f3f3f3", outline="")

        # Frame to hold interactive widgets positioned at the center of panel
        content = tk.Frame(canvas, bg="#f3f3f3")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Hamster image floating above panel
        if self.hamster_img:
            hamster_x = (1400 - self.hamster_img.width()) // 2
            self.hamster_label = tk.Label(self.preferences_window, image=self.hamster_img, bd=0, bg="#f3f3f3")
            self.hamster_label.place(x=hamster_x, y=panel_y - self.hamster_img.height() - 10)
            self.hamster_label.lift()

        # Header text
        header = tk.Label(content, text="Preferences", bg="#f3f3f3", fg="#000000")
        if press_start_font:
            header.configure(font=("Press Start 2P", 20))
        else:
            header.configure(font=("Helvetica", 20, "bold"))
        header.pack(pady=(10, 30))

        # Utility to create labelled slider row
        def create_slider_row(parent, label_text, unit_text, range_from, range_to, step, default_val):
            row = tk.Frame(parent, bg="#f3f3f3")
            row.pack(fill="x", padx=40, pady=20)

            left_lbl = tk.Label(row, text=label_text, bg="#f3f3f3")
            right_lbl = tk.Label(row, text=unit_text, bg="#f3f3f3")
            font_def = ("Press Start 2P", 12) if press_start_font else ("Helvetica", 12, "bold")
            left_lbl.configure(font=font_def)
            right_lbl.configure(font=font_def)
            left_lbl.pack(side="left")
            right_lbl.pack(side="right")

            style_name = f"{label_text.replace(' ', '')}.Horizontal.TScale"
            style = ttk.Style()
            style.theme_use("default")
            style.configure(style_name, troughcolor="#eeeeee", background="#edb36a")

            var = tk.IntVar(value=default_val)
            scale = ttk.Scale(row, from_=range_from, to=range_to, orient="horizontal", style=style_name, variable=var, length=600)
            scale.pack(side="bottom", pady=10)

            # Snap to nearest discrete step
            def snap(event):
                val = round(var.get() / step) * step
                var.set(val)
            scale.bind("<ButtonRelease-1>", snap)

            # Tooltip showing value
            tooltip = tk.Label(row, text="", bg="#000000", fg="#FFFFFF", padx=4, pady=2)
            tooltip_font = ("Press Start 2P", 8) if press_start_font else ("Helvetica", 8)
            tooltip.configure(font=tooltip_font)

            def move_tooltip(event):
                tooltip.configure(text=f"{var.get()} mL")
                # Fix y so label stays at constant height above slider
                tooltip.place(x=event.x, y=event.y)
            def hide_tooltip(event):
                tooltip.place_forget()
            scale.bind("<Motion>", move_tooltip)
            scale.bind("<Leave>", hide_tooltip)
            return var

        goal_var = create_slider_row(content, "Daily Goal", "(mL)", 0, 4000, 500, self.pet.config.dailyGoal)
        sip_var = create_slider_row(content, "Sip Amount", "(mL)", 0, 1000, 250, self.pet.config.sipAmount)

        # Save button
        save_btn = tk.Button(content, text="Save", bg="#b41c27", fg="#FFFFFF", activebackground="#992026", padx=20, pady=10, bd=0)
        btn_font = ("Press Start 2P", 12) if press_start_font else ("Helvetica", 12, "bold")
        save_btn.configure(font=btn_font)
        save_btn.pack(pady=(40, 10))

        def save_preferences():
            self.pet.config.dailyGoal = int(goal_var.get())
            self.pet.config.sipAmount = int(sip_var.get())
            messagebox.showinfo("Saved", "Preferences updated.")
            self.stop_background_animation()
            self.preferences_window.destroy()
            self.preferences_window = None
        save_btn.configure(command=save_preferences)

        # Handle window close
        def on_closing():
            self.stop_background_animation()
            self.preferences_window.destroy()
            self.preferences_window = None
        
        self.preferences_window.protocol("WM_DELETE_WINDOW", on_closing)

    def openSetupFallback(self):
        """Fallback preferences window if main window fails"""
        self.preferences_window = tk.Toplevel(self.pet.window)
        self.preferences_window.title("Dew - Preferences")
        self.preferences_window.geometry("500x300")
        self.preferences_window.attributes("-topmost", True)

        tk.Label(self.preferences_window, text="Daily Goal (ml)").grid(row=0, column=0, padx=10, pady=5)
        goalVar = tk.StringVar(value=str(self.pet.config.dailyGoal))
        tk.Entry(self.preferences_window, textvariable=goalVar, width=10).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.preferences_window, text="Sip Amount (ml)").grid(row=1, column=0, padx=10, pady=5)
        sipVar = tk.StringVar(value=str(self.pet.config.sipAmount))
        tk.Entry(self.preferences_window, textvariable=sipVar, width=10).grid(row=1, column=1, padx=10, pady=5)

        def save():
            try:
                self.pet.config.dailyGoal = int(goalVar.get())
                self.pet.config.sipAmount = int(sipVar.get())
                messagebox.showinfo("Saved", "Preferences updated.")
                self.preferences_window.destroy()
                self.preferences_window = None
            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        ttk.Button(self.preferences_window, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

        def on_closing():
            self.preferences_window.destroy()
            self.preferences_window = None
        
        self.preferences_window.protocol("WM_DELETE_WINDOW", on_closing)

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

        photo = tk.PhotoImage(file="assets/thirsty.gif")
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
