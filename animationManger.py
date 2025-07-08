import tkinter as tk

class AnimationManager:

    def __init__(self):
        self.cycle = 0
        self.current_state = 0  # 0=idle, 1=panic, 2=water

        # Frame counts for each animation
        self.IDLE_FRAMES = 3
        self.PANIC_FRAMES = 6
        self.HOVER_FRAMES = 3

        # Animation frames
        self.idle_frames = []
        self.panic_frames = []
        self.water_frames = []

    def load_animations(self):
        try:
            self.idle_frames = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i)
                               for i in range(self.IDLE_FRAMES)]
            self.panic_frames = [tk.PhotoImage(file='panic.gif', format='gif -index %i' % i)
                                for i in range(self.PANIC_FRAMES)]
            self.water_frames = [tk.PhotoImage(file='water.gif', format='gif -index %i' % i)
                                for i in range(self.HOVER_FRAMES)]
            print("GIF files loaded successfully!")
        except Exception as e:
            print(f"Error loading GIF files: {e}")
            print("Make sure the GIF files exist in the specified directory.")
            exit()

    def get_frame_dimensions(self):
        return self.idle_frames[0].width(), self.idle_frames[0].height()

    def get_current_frame(self):
        if self.current_state == 0:  # Idle
            frame = self.idle_frames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.idle_frames)
        elif self.current_state == 1:  # Panic
            frame = self.panic_frames[self.cycle]
            self.cycle = (self.cycle + 1)
            if self.cycle > 4:
                self.cycle = 3
        elif self.current_state == 2:  # Water
            frame = self.water_frames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.water_frames)
        else:  # Fallback
            frame = self.idle_frames[0]
            self.current_state = 0
            self.cycle = 0

        return frame

    def set_state(self, new_state):
        """Change animation state and reset cycle if needed."""
        if new_state != self.current_state:
            self.current_state = new_state
            self.cycle = 0

    def get_animation_speed(self):
        """Get animation speed based on current state."""
        speed_map = {
            0: 400,  # Idle - slower
            1: 100,  # Panic - faster
            2: 150   # Water - medium
        }
        return speed_map.get(self.current_state, 400)