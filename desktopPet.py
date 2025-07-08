import tkinter as tk
from tkinter import ttk, messagebox  # ttk for progress bar
from UIManager import UIManager
from behaviourManager import BehaviorManager
from configManager import ConfigManager
from animationManger import AnimationManager
from mouseManager import MouseHandler

class DesktopPet:
    """Main desktop pet application class."""
    
    def __init__(self):
        # Position variables
        self.x = 100
        self.y = 150

        # Initialize components
        self.animation = AnimationManager()
        self.behavior = BehaviorManager()
        self.mouseHandler = MouseHandler(self)
        self.uiManager = UIManager(self)

        # Window components
        self.window = None
        self.label = None
        self.petWidth = 0
        self.petHeight = 0
        self.config = None

        self.setupWindow()

    def setupWindow(self):
        """Initialize the main window and components."""
        # Create main window
        self.window = tk.Tk()

        self.animation.load_animations()

        # Get pet dimensions
        self.petWidth, self.petHeight = self.animation.get_frame_dimensions()

        # Configure window
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.window.wm_attributes('-topmost', True)

        # Create label
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.pack()

        # Bind mouse events
        self.bindMouseEvents()

        # Initialize config
        self.config = ConfigManager()

        # Set initial position
        self.window.geometry(f'{self.petWidth}x{self.petHeight}+{self.x}+{self.y}')

    def bindMouseEvents(self):
        """Bind all mouse events to handlers."""
        self.label.bind("<Button-1>", self.mouseHandler.on_button_press)
        self.label.bind("<B1-Motion>", self.mouseHandler.on_mouse_move)
        self.label.bind("<ButtonRelease-1>", self.mouseHandler.on_button_release)
        self.label.bind("<Enter>", self.mouseHandler.start_hover)
        self.label.bind("<Leave>", self.mouseHandler.stop_hover)
        self.label.bind("<Button-3>", self.mouseHandler.open_setup)

    def updateAnimation(self):
        """Main animation update loop."""
        # Update behavior state
        newState = self.behavior.determine_behavior()
        self.animation.set_state(newState)

        # Get current frame
        frame = self.animation.get_current_frame()

        # Update window position (unless dragging)
        if not self.behavior.isDragging:
            self.window.geometry(f'{self.petWidth}x{self.petHeight}+{self.x}+{self.y}')

        # Update image
        self.label.configure(image=frame)

        # Schedule next update
        speed = self.animation.get_animation_speed()
        self.window.after(speed, self.updateAnimation)

    def openSetupWindow(self):
        """Delegate to UI manager."""
        self.uiManager.open_setup_window()

    def openLoggingWindow(self):
        """Delegate to UI manager."""
        self.uiManager.open_logging_window()

    def run(self):
        """Start the desktop pet application."""
        # Auto-open setup on first launch
        if self.config.data.get("lastResetDate") is None:
            self.window.after(500, self.openSetupWindow)

        # Start animation loop
        self.window.after(1, self.updateAnimation)

        # Start main GUI loop
        self.window.mainloop()


# Run the application
pet = DesktopPet()
pet.run()