import tkinter as tk
from tkinter import ttk, messagebox  # ttk for progress bar
from UIManager import UIManager
from behaviourManager import BehaviorManager
from configManager import ConfigManager
from animationManger import AnimationManager
from mouseManager import MouseHandler

# Class Representing the DesktopPet
class DesktopPet:
    def __init__(self):
        # Position variables
        self.x = 100
        self.y = 150

        # Initialize components
        self.animation = AnimationManager()
        self.behavior = BehaviorManager()
        self.mouse_handler = MouseHandler(self)
        self.ui_manager = UIManager(self)

        # Window components
        self.window = None
        self.label = None
        self.pet_width = 0
        self.pet_height = 0
        self.config = None

        self.setup_window()

    def setup_window(self):
        """Initialize the main window and components."""
        # Create main window
        self.window = tk.Tk()

        self.animation.load_animations()

        # Get pet dimensions
        self.pet_width, self.pet_height = self.animation.get_frame_dimensions()

        # Configure window
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.wm_attributes('-topmost', True)

        # Create label
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.pack()

        # Bind mouse events
        self.bind_mouse_events()

        # Initialize config
        self.config = ConfigManager()

        # Set initial position
        self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

    def bind_mouse_events(self):
        """Bind all mouse events to handlers."""
        self.label.bind("<Button-1>", self.mouse_handler.on_button_press)
        self.label.bind("<B1-Motion>", self.mouse_handler.on_mouse_move)
        self.label.bind("<ButtonRelease-1>", self.mouse_handler.on_button_release)
        self.label.bind("<Enter>", self.mouse_handler.start_hover)
        self.label.bind("<Leave>", self.mouse_handler.stop_hover)
        self.label.bind("<Button-3>", self.mouse_handler.open_setup)

    def update_animation(self):
        """Main animation update loop."""
        # Update behavior state
        new_state = self.behavior.determine_behavior()
        self.animation.set_state(new_state)

        # Get current frame
        frame = self.animation.get_current_frame()

        # Update window position (unless dragging)
        if not self.behavior.is_dragging:
            self.window.geometry(f'{self.pet_width}x{self.pet_height}+{self.x}+{self.y}')

        # Update image
        self.label.configure(image=frame)

        # Schedule next update
        speed = self.animation.get_animation_speed()
        self.window.after(speed, self.update_animation)

    def open_setup_window(self):
        """Delegate to UI manager."""
        self.ui_manager.open_setup_window()

    def open_logging_window(self):
        """Delegate to UI manager."""
        self.ui_manager.open_logging_window()

    def run(self):
        """Start the desktop pet application."""
        # Auto-open setup on first launch
        if self.config.data.get("last_reset_date") is None:
            self.window.after(500, self.open_setup_window)

        # Start animation loop
        self.window.after(1, self.update_animation)

        # Start main GUI loop
        self.window.mainloop()


# Run the application
pet = DesktopPet()
pet.run()