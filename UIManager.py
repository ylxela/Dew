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
        self.bg_canvas = None
        self.bg_image_id = None
        self.bg_animation_running = False

    def load_background_frames(self):
        """Load all frames of the background GIF"""
        try:
            self.bg_frames = []
            frame_index = 0
            
            while True:
                try:
                    frame = tk.PhotoImage(file='assets/water logger.gif', format='gif -index %i' % frame_index)
                    # Scale the frame to fit the window (1400x1060)
                    # Note: PhotoImage zoom might not give exact dimensions, but it will scale proportionally
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
        if not self.bg_animation_running or not self.bg_frames or not self.bg_canvas:
            return
            
        # Update the canvas with the current frame
        if self.bg_image_id:
            self.bg_canvas.delete(self.bg_image_id)
            
        current_frame = self.bg_frames[self.bg_current_frame]
        self.bg_image_id = self.bg_canvas.create_image(700, 530, image=current_frame)
        
        # Move to next frame
        self.bg_current_frame = (self.bg_current_frame + 1) % len(self.bg_frames)
        
        # Schedule next frame update (adjust timing as needed)
        if self.preferences_window:
            self.preferences_window.after(200, self.animate_background)

    def stop_background_animation(self):
        """Stop the background animation"""
        self.bg_animation_running = False
        self.bg_frames = []
        self.bg_current_frame = 0
        self.bg_canvas = None
        self.bg_image_id = None

    def openSetup(self):
        # Close existing window if it exists
        if self.preferences_window is not None:
            self.stop_background_animation()
            self.preferences_window.destroy()
            
        # Create fixed window with specified dimensions
        self.preferences_window = tk.Toplevel(self.pet.window)
        self.preferences_window.title("Dew - Preferences")
        self.preferences_window.geometry("1400x1060")
        self.preferences_window.resizable(False, False)
        self.preferences_window.attributes("-topmost", True)
        
        # Try to load background image with fallback
        try:
            # Check if background image exists and try to load animated frames
            if os.path.exists("assets/water logger.gif") and self.load_background_frames():
                # Create canvas for animated background
                self.bg_canvas = tk.Canvas(self.preferences_window, width=1400, height=1060, highlightthickness=0)
                self.bg_canvas.pack(fill=tk.BOTH, expand=True)
                
                # Start background animation
                self.bg_animation_running = True
                self.animate_background()
                
            else:
                # Use solid color background if image doesn't exist or loading fails
                self.bg_canvas = tk.Canvas(self.preferences_window, width=1400, height=1060, highlightthickness=0, bg='#4A90E2')
                self.bg_canvas.pack(fill=tk.BOTH, expand=True)
                print("Could not load animated background, using solid color")
            
            # Create main frame for preferences
            main_frame = tk.Frame(self.bg_canvas, bg='#E8D5B7', padx=40, pady=40, relief=tk.RAISED, borderwidth=2)
            main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Configure custom font with fallback
            try:
                custom_font = ("Press Start 2P", 16)
                label_font = ("Press Start 2P", 14)
                button_font = ("Press Start 2P", 12)
                title_font = ("Press Start 2P", 20)
                # Test if the font actually works
                test_label = tk.Label(main_frame, text="Test", font=custom_font)
                test_label.destroy()
            except:
                # Fallback fonts if Press Start 2P is not available
                custom_font = ("Courier", 16, "bold")
                label_font = ("Courier", 14, "bold")
                button_font = ("Courier", 12, "bold")
                title_font = ("Courier", 20, "bold")
            
            # Title
            title_label = tk.Label(main_frame, text="Preferences", font=title_font, 
                                 bg='#E8D5B7', fg='#2B2B2B')
            title_label.pack(pady=(0, 30))
            
            # Daily Goal Section
            goal_frame = tk.Frame(main_frame, bg='#E8D5B7')
            goal_frame.pack(fill=tk.X, pady=10)
            
            goal_label = tk.Label(goal_frame, text="Daily Goal", font=label_font, bg='#E8D5B7', fg='#2B2B2B')
            goal_label.pack(anchor=tk.W)
            
            # Goal value display
            goal_value_frame = tk.Frame(goal_frame, bg='#E8D5B7')
            goal_value_frame.pack(fill=tk.X, pady=5)
            
            self.goal_var = tk.IntVar(value=self.pet.config.dailyGoal)
            goal_value_label = tk.Label(goal_value_frame, textvariable=self.goal_var, font=custom_font, bg='#E8D5B7', fg='#2B2B2B')
            goal_value_label.pack(side=tk.LEFT)
            
            goal_unit_label = tk.Label(goal_value_frame, text="(mL)", font=label_font, bg='#E8D5B7', fg='#2B2B2B')
            goal_unit_label.pack(side=tk.LEFT, padx=(10, 0))
            
            # Goal slider
            goal_slider = tk.Scale(goal_frame, from_=0, to=4000, resolution=500, orient=tk.HORIZONTAL, 
                                 length=400, variable=self.goal_var, font=label_font, bg='#E8D5B7', 
                                 fg='#2B2B2B', highlightbackground='#E8D5B7', troughcolor='#D4B896')
            goal_slider.pack(fill=tk.X, pady=5)
            
            # Sip Amount Section
            sip_frame = tk.Frame(main_frame, bg='#E8D5B7')
            sip_frame.pack(fill=tk.X, pady=10)
            
            sip_label = tk.Label(sip_frame, text="Sip Amount", font=label_font, bg='#E8D5B7', fg='#2B2B2B')
            sip_label.pack(anchor=tk.W)
            
            # Sip value display
            sip_value_frame = tk.Frame(sip_frame, bg='#E8D5B7')
            sip_value_frame.pack(fill=tk.X, pady=5)
            
            self.sip_var = tk.IntVar(value=self.pet.config.sipAmount)
            sip_value_label = tk.Label(sip_value_frame, textvariable=self.sip_var, font=custom_font, bg='#E8D5B7', fg='#2B2B2B')
            sip_value_label.pack(side=tk.LEFT)
            
            sip_unit_label = tk.Label(sip_value_frame, text="(mL)", font=label_font, bg='#E8D5B7', fg='#2B2B2B')
            sip_unit_label.pack(side=tk.LEFT, padx=(10, 0))
            
            # Sip slider
            sip_slider = tk.Scale(sip_frame, from_=0, to=1000, resolution=500, orient=tk.HORIZONTAL, 
                                length=400, variable=self.sip_var, font=label_font, bg='#E8D5B7', 
                                fg='#2B2B2B', highlightbackground='#E8D5B7', troughcolor='#D4B896')
            sip_slider.pack(fill=tk.X, pady=5)
            
            # Save button
            def save():
                try:
                    self.pet.config.dailyGoal = self.goal_var.get()
                    self.pet.config.sipAmount = self.sip_var.get()
                    messagebox.showinfo("Saved", "Preferences updated.")
                    self.stop_background_animation()
                    self.preferences_window.destroy()
                    self.preferences_window = None
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save preferences: {str(e)}")
            
            save_button = tk.Button(main_frame, text="Save", command=save, font=button_font, 
                                  bg='#B85450', fg='white', padx=30, pady=10, relief=tk.FLAT)
            save_button.pack(pady=20)
            
            # Handle window close
            def on_closing():
                self.stop_background_animation()
                self.preferences_window.destroy()
                self.preferences_window = None
            
            self.preferences_window.protocol("WM_DELETE_WINDOW", on_closing)
            
        except Exception as e:
            # Fallback to simple window if anything fails
            messagebox.showerror("Error", f"Could not create preferences window: {str(e)}")
            self.stop_background_animation()
            if self.preferences_window:
                self.preferences_window.destroy()
            self.preferences_window = None
            self.openSetupFallback()

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
