#!/usr/bin/env python3
import tkinter as tk
import os

class TestAnimatedBackground:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Animated Background")
        self.root.geometry("800x600")
        
        self.bg_frames = []
        self.bg_current_frame = 0
        self.bg_canvas = None
        self.bg_image_id = None
        self.bg_animation_running = False
        
        self.load_background_frames()
        self.create_ui()
        
    def load_background_frames(self):
        """Load all frames of the background GIF"""
        try:
            self.bg_frames = []
            frame_index = 0
            
            while True:
                try:
                    frame = tk.PhotoImage(file='assets/water logger.gif', format='gif -index %i' % frame_index)
                    # Scale the frame to fit the window
                    scaled_frame = frame.zoom(1, 1)  # Adjust scaling factor as needed
                    self.bg_frames.append(scaled_frame)
                    frame_index += 1
                except tk.TclError:
                    # No more frames
                    break
            
            print(f"Loaded {len(self.bg_frames)} frames")
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
        self.bg_image_id = self.bg_canvas.create_image(400, 300, image=current_frame)
        
        # Move to next frame
        self.bg_current_frame = (self.bg_current_frame + 1) % len(self.bg_frames)
        
        # Schedule next frame update
        self.root.after(200, self.animate_background)

    def create_ui(self):
        if len(self.bg_frames) > 0:
            # Create canvas for animated background
            self.bg_canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
            self.bg_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Start background animation
            self.bg_animation_running = True
            self.animate_background()
            
            # Add a test button on top
            button = tk.Button(self.root, text="Animation Running!", font=("Arial", 16), 
                             bg='white', fg='black', padx=20, pady=10)
            button.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            
        else:
            # Fallback if no frames loaded
            label = tk.Label(self.root, text="Could not load animated background", 
                           font=("Arial", 16), bg='red', fg='white')
            label.pack(expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    test = TestAnimatedBackground()
    test.run() 