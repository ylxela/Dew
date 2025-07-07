import tkinter as tk
import random
import time

class DesktopPet:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("Desktop Pet")

        # Window configuration for transparency and always on top
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.wm_attributes('-transparentcolor', 'black')  # Make black transparent
        self.window.wm_attributes('-topmost', True)  # Keep on top

        # Pet position and movement variables
        self.x = 200
        self.y = 500
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 2

        # Get screen dimensions
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Load your PNG image (replace with your image path)
        try:
            self.pet_image = tk.PhotoImage(file="pet.png")  # Replace with your PNG file path
        except:
            # If no image found, create a simple colored rectangle as placeholder
            self.pet_image = tk.PhotoImage(width=50, height=50)
            self.pet_image.put("orange", to=(0, 0, 50, 50))

        # Create label to display the pet
        self.label = tk.Label(self.window, image=self.pet_image, bd=0, bg='black')
        self.label.pack()

        # Bind click event to make pet draggable
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.drag)

        # Variables for dragging
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Start the pet's behavior
        self.behavior_loop()

    def start_drag(self, event):
        """Start dragging the pet"""
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def drag(self, event):
        """Drag the pet around"""
        x = self.window.winfo_pointerx() - self.drag_start_x
        y = self.window.winfo_pointery() - self.drag_start_y
        self.window.geometry(f"+{x}+{y}")
        self.x = x
        self.y = y

    def move_pet(self):
        """Move the pet across the screen"""
        self.x += self.direction * self.speed

        # Bounce off screen edges
        if self.x <= 0:
            self.direction = 1  # Move right
        elif self.x >= self.screen_width - 100:
            self.direction = -1  # Move left

        # Keep pet on screen vertically
        if self.y < 0:
            self.y = 0
        elif self.y > self.screen_height - 100:
            self.y = self.screen_height - 100

        # Update window position
        self.window.geometry(f"+{self.x}+{self.y}")

    def random_behavior(self):
        """Add some random behaviors"""
        action = random.choice(['move', 'idle', 'jump', 'change_direction'])

        if action == 'move':
            self.move_pet()
        elif action == 'idle':
            pass  # Do nothing, just stay in place
        elif action == 'jump':
            # Simple jump animation
            original_y = self.y
            self.y -= 20
            self.window.geometry(f"+{self.x}+{self.y}")
            self.window.after(200, lambda: self.return_from_jump(original_y))
        elif action == 'change_direction':
            self.direction *= -1  # Reverse direction

    def return_from_jump(self, original_y):
        """Return from jump to original position"""
        self.y = original_y
        self.window.geometry(f"+{self.x}+{self.y}")

    def behavior_loop(self):
        """Main behavior loop"""
        self.random_behavior()
        # Schedule next behavior (every 500ms)
        self.window.after(500, self.behavior_loop)

    def run(self):
        """Start the pet"""
        self.window.mainloop()

# Instructions for use:
# 1. Save this code as 'desktop_pet.py'
# 2. Find a PNG image of your pet (cat, dog, etc.) and save it as 'pet.png' in the same folder
# 3. Run the script: python desktop_pet.py
#
# TO HIDE THE TERMINAL:
# Method 1: Save as .pyw file instead of .py (Windows only)
# Method 2: Use pythonw instead of python: pythonw desktop_pet.py
# Method 3: Create a batch file or shortcut (see below)
#
# Features:
# - Click and drag to move the pet
# - Pet will move around randomly
# - Pet bounces off screen edges
# - Transparent background
# - Always stays on top of other windows

pet = DesktopPet()
pet.run()