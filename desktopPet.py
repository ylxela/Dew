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


# --------------------------------------------------------------
# Helper GUI WINDOWS
# --------------------------------------------------------------

    def open_setup_window(self):
        """Popup window to change daily goal and sip size."""
        win = tk.Toplevel(self.window)
        win.title("Dew - Setup")
        win.attributes("-topmost", True)

        tk.Label(win, text="Daily Goal (ml)").grid(row=0, column=0, padx=10, pady=5)
        goal_var = tk.StringVar(value=str(self.config.dailyGoal))
        tk.Entry(win, textvariable=goal_var, width=10).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(win, text="Sip Amount (ml)").grid(row=1, column=0, padx=10, pady=5)
        sip_var = tk.StringVar(value=str(self.config.sipAmount))
        tk.Entry(win, textvariable=sip_var, width=10).grid(row=1, column=1, padx=10, pady=5)

        def save():
            try:
                self.config.dailyGoal = int(goal_var.get())
                self.config.sipAmount = int(sip_var.get())
                messagebox.showinfo("Saved", "Preferences updated.")
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")

        ttk.Button(win, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

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