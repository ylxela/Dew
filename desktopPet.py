import tkinter as tk
from tkinter import ttk, messagebox  # ttk for progress bar
from configManager import ConfigManager

class DesktopPet:

    # Configuration and Initial Setup
    def __init__(self):
        # Pet position and animation variables
        self.x = 100
        self.y = 150
        self.cycle = 0
        self.check = 0

        # Interaction state variables
        self.is_dragging = False
        self.is_hovering = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Frames Size for each Gif
        self.IDLE_FRAMES = 3
        self.PANIC_FRAMES = 6
        self.HOVER_FRAMES = 3

        # Mouse interaction variables
        self.click_start_pos = (0, 0)
        self.potential_drag = False

        # Initialize window and components
        self.window = None
        self.label = None
        self.idle = None
        self.panic = None
        self.water = None
        self.pet_width = 0
        self.pet_height = 0
        self.config = None

        self.setup_window()

    def setup_window(self):
        """Initialize the main window and load resources."""
        # Create main window
        self.window = tk.Tk()

        try:
            # Load all GIF animations by extracting individual frames
            self.idle = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % (i)) for i in range(self.IDLE_FRAMES)]
            self.panic = [tk.PhotoImage(file= 'panic.gif', format='gif -index %i' % (i)) for i in range(self.PANIC_FRAMES)]
            self.water = [tk.PhotoImage(file='water.gif', format='gif -index %i' % (i)) for i in range(self.HOVER_FRAMES)]
            self.pet_width = self.idle[0].width()
            self.pet_height = self.idle[0].height()
            print("GIF files loaded successfully!")
        except Exception as e:
            print(f"Error loading GIF files: {e}")
            print("Make sure the GIF files exist in the specified directory.")
            exit()

        # Configure window appearance
        self.window.config(highlightbackground='black')  # Set background color
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.wm_attributes('-transparentcolor', 'black')  # Make black pixels transparent

        # FIXED: Make window always stay on top of other applications
        self.window.wm_attributes('-topmost', True)

        # Create label to display the pet animations
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.pack()

        # Bind mouse events for drag and drop functionality
        self.label.bind("<Button-1>", self.on_button_press)        # Left mouse button press
        self.label.bind("<B1-Motion>", self.on_mouse_move)         # Mouse movement while button held
        self.label.bind("<ButtonRelease-1>", self.on_button_release)  # Left mouse button release

        # Bind mouse events for hover functionality
        self.label.bind("<Enter>", self.start_hover)          # Mouse enters pet area
        self.label.bind("<Leave>", self.stop_hover)           # Mouse leaves pet area
        # Right-click to open settings
        self.label.bind("<Button-3>", lambda e: self.open_setup_window())

        # Initialize config manager (assuming it exists)
        self.config = ConfigManager()

        # Set initial window position
        self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

    # Mouse Functions
    # Initial Drag Operation
    def start_drag(self, event):
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y

        # Switch to panic state when dragging starts
        self.check = 1  # Panic state
        self.cycle = 0  # Reset animation cycle
        print("Dragging started - panic mode!")


    def drag_pet(self, event):
        """
        Handles pet movement during drag operation.

        Args:
            event: Tkinter event object containing mouse coordinates
        """
        if self.is_dragging:
            # Calculate new position based on mouse movement
            new_x = self.window.winfo_pointerx() - self.drag_start_x
            new_y = self.window.winfo_pointery() - self.drag_start_y

            # Update pet position variables - THIS IS THE KEY FIX
            self.x = new_x
            self.y = new_y

            # Move the window to new position
            self.window.geometry(f'{self.pet_width}x{self.pet_height}+{new_x}+{new_y}')


    def stop_drag(self, event):
        """
        Ends drag operation when mouse button is released.

        Args:
            event: Tkinter event object
        """
        if self.is_dragging:
            self.is_dragging = False
            print("Dragging stopped - returning to normal behavior")

            # Reset animation cycle
            self.cycle = 0


    def start_hover(self, event):
        """
        Called when mouse enters the pet area.

        Args:
            event: Tkinter event object
        """
        if not self.is_dragging:  # Only switch to hover if not dragging
            self.is_hovering = True
            self.check = 2  # Water state
            self.cycle = 0  # Reset animation cycle
            print("Mouse hover started - water mode!")

    def stop_hover(self, event):
        """
        Called when mouse leaves the pet area.

        Args:
            event: Tkinter event object
        """
        if not self.is_dragging:  # Only switch to idle if not dragging
            self.is_hovering = False
            self.check = 0  # Idle state
            self.cycle = 0  # Reset animation cycle
            print("Mouse hover stopped - idle mode!")


# ==============================================================================
# BEHAVIOR CONTROL FUNCTIONS
# ==============================================================================

    def determine_behavior(self):
        """
        Determines the pet's behavior based on current interaction state.

        Returns:
            int: Behavior state (0=idle, 1=panic, 2=water)
        """
        if self.is_dragging:
            return 1  # Panic state
        elif self.is_hovering:
            return 2  # Water state
        else:
            return 0  # Idle state

    def update_animation(self):
        """
        Main update function that handles animation frame updates and pet behavior.
        """
        # Determine current behavior based on interaction state
        new_check = self.determine_behavior()

        # If behavior changed, reset animation cycle
        if new_check != self.check:
            self.cycle = 0
            self.check = new_check

        # Select appropriate animation frame and advance cycle
        if self.check == 0:  # Idle state
            frame = self.idle[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.idle)

        elif self.check == 1:  # Panic state
            frame = self.panic[self.cycle]
            self.cycle = (self.cycle + 1)
            if (self.cycle > 4): self.cycle = 3

        elif self.check == 2:  # Water state
            frame = self.water[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.water)

        else:  # Fallback to idle
            frame = self.idle[0]
            self.check = 0
            self.cycle = 0

        # Update window position using global coordinates (dragging updates this)
        if not self.is_dragging:
            self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

        # Always update the image
        self.label.configure(image=frame)

        # Schedule next update - different speeds for different animations
        if self.check == 0:  # Idle - slower animation
            self.window.after(400, self.update_animation)
        elif self.check == 1:  # Panic - faster animation
            self.window.after(100, self.update_animation)
        elif self.check == 2:  # Water - medium speed animation
            self.window.after(150, self.update_animation)
        else:
            self.window.after(400, self.update_animation)  # Default fallback

# Helper GUI WINDOWS
# --------------------------------------------------------------

    def open_setup_window(self):
        """Popup window to change daily goal and sip size with revamped UI."""
        # Create top-level window
        win = tk.Toplevel(self.window)
        win.title("Preferences")
        win.geometry("1400x1060")
        win.resizable(False, False)
        win.attributes("-topmost", True)
        # Ensure it always stays above pet
        win.lift(self.window)

        # --------------------------------------------------
        # Load resources (background GIF + hamster PNG)
        # --------------------------------------------------
        try:
            self.bg_gif_frames = [tk.PhotoImage(file="water logger.gif", format=f"gif -index {i}") for i in range(100)]
        except Exception:
            # fallback: single frame
            self.bg_gif_frames = [tk.PhotoImage(file="water logger.gif")]
        try:
            self.hamster_img = tk.PhotoImage(file="water logging hamster.png")
        except Exception:
            self.hamster_img = None

        # Display animated background using a label that updates every 100 ms
        bg_label = tk.Label(win)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        def animate_bg(frame=0):
            if not win.winfo_exists():
                return
            frame = (frame + 1) % len(self.bg_gif_frames)
            bg_label.configure(image=self.bg_gif_frames[frame])
            win.after(100, animate_bg, frame)
        bg_label.configure(image=self.bg_gif_frames[0])
        animate_bg()

        # --------------------------------------------------
        # Load font (Press Start 2P) if installed, else default
        # --------------------------------------------------
        try:
            import tkinter.font as tkfont
            press_start_font = tkfont.Font(family="Press Start 2P", size=12)
        except Exception:
            press_start_font = None

        # --------------------------------------------------
        # Central panel (semi-transparent)
        # --------------------------------------------------
        panel_width = 800
        panel_height = 600
        panel_x = (1400 - panel_width) // 2
        panel_y = (1060 - panel_height) // 2 + 80  # leave space for hamster
        # Create canvas to draw rounded rectangle panel
        canvas = tk.Canvas(win, width=panel_width, height=panel_height, highlightthickness=0)
        canvas.place(x=panel_x, y=panel_y)
        # Draw rectangle (rounded corners are limited in Tk)
        canvas.create_rectangle(0, 0, panel_width, panel_height, fill="#f3f3f3", outline="")

        # Frame to hold interactive widgets positioned at the center of panel
        content = tk.Frame(canvas, bg="#f3f3f3")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Hamster image floating above panel
        if self.hamster_img:
            hamster_x = (1400 - self.hamster_img.width()) // 2
            self.hamster_label = tk.Label(win, image=self.hamster_img, bd=0, bg="#f3f3f3")  # transparent bg
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

        goal_var = create_slider_row(content, "Daily Goal", "(mL)", 0, 4000, 500, self.config.dailyGoal)
        sip_var = create_slider_row(content, "Sip Amount", "(mL)", 0, 1000, 250, self.config.sipAmount)

        # Save button
        save_btn = tk.Button(content, text="Save", bg="#b41c27", fg="#FFFFFF", activebackground="#992026", padx=20, pady=10, bd=0)
        btn_font = ("Press Start 2P", 12) if press_start_font else ("Helvetica", 12, "bold")
        save_btn.configure(font=btn_font)
        save_btn.pack(pady=(40, 10))

        def save_preferences():
            self.config.dailyGoal = int(goal_var.get())
            self.config.sipAmount = int(sip_var.get())
            messagebox.showinfo("Saved", "Preferences updated.")
            win.destroy()
        save_btn.configure(command=save_preferences)




    def open_logging_window(self):
        """Popup near Dewey to log water intake and show progress."""
        # Determine popup position relative to pet
        popup = tk.Toplevel(self.window)
        popup.title("Log Water")
        popup.attributes("-topmost", True)
        popup.geometry(f"200x120+{self.x+110}+{self.y}")
        tk.Label(popup, text=f"Log {self.config.sipAmount} ml water?").pack(pady=5)

        progress = ttk.Progressbar(popup, maximum=self.config.dailyGoal, value=self.config.currentIntake, length=160)
        progress.pack(pady=5)

        prog_label = tk.Label(popup, text=f"{self.config.currentIntake}/{self.config.dailyGoal} ml")
        prog_label.pack()

        def log_water():
            self.config.addIntake(self.config.sipAmount)
            progress["value"] = self.config.currentIntake
            prog_label.config(text=f"{self.config.currentIntake}/{self.config.dailyGoal} ml")
            if self.config.currentIntake >= self.config.dailyGoal:
                messagebox.showinfo("Congrats!", "You've met today's hydration goal!")
            popup.destroy()

        ttk.Button(popup, text="Drink", command=log_water).pack(pady=5)


# --------------------------------------------------------------
# MOUSE INTERACTION (CLICK VS DRAG)
# --------------------------------------------------------------


    def on_button_press(self, event):
        self.click_start_pos = (event.x_root, event.y_root)
        self.potential_drag = True

    def on_mouse_move(self, event):
        if self.potential_drag:
            dx = abs(event.x_root - self.click_start_pos[0])
            dy = abs(event.y_root - self.click_start_pos[1])
            if dx > 5 or dy > 5:
                self.potential_drag = False
                self.start_drag(event)
        if self.is_dragging:
            self.drag_pet(event)

    def on_button_release(self, event):
        if self.is_dragging:
            self.stop_drag(event)
        elif self.potential_drag:
            # Treat as click — open logger
            self.open_logging_window()
        self.potential_drag = False

    def run(self):
        """Start the desktop pet application."""
        # Auto-open setup on first launch
        if self.config.data.get("last_reset_date") is None:
            self.window.after(500, self.open_setup_window)

        # Start the animation loop
        self.window.after(1, self.update_animation)

        # Start the main GUI loop
        self.window.mainloop()

pet = DesktopPet()
pet.run()