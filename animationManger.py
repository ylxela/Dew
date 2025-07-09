import tkinter as tk

class AnimationManager:
    """Manages pet animations and frame cycling."""

    def __init__(self):
        self.cycle = 0
        self.currentState = 0  # 0=idle, 1=panic, 2=hover

        # Frame counts for each animation
        self.IDLE_FRAMES = 3
        self.PANIC_FRAMES = 6
        self.HOVER_FRAMES = 3

        # Animation frames
        self.idleFrames = []
        self.panicFrames = []
        self.hoverFrames = []

    def load_animations(self):
        """Load animation frames from GIF files."""
        scale_factor = 2
        try:
            self.idleFrames = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                            for i in range(self.IDLE_FRAMES)]
            self.panicFrames = [tk.PhotoImage(file='panic.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                                for i in range(self.PANIC_FRAMES)]
            self.hoverFrames = [tk.PhotoImage(file='hover.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                                for i in range(self.HOVER_FRAMES)]
        except Exception as e:
            raise FileNotFoundError(f"Error loading GIF files: {e}. Make sure the GIF files exist in the directory.")

    def get_frame_dimensions(self):
        """Return dimensions of animation frames."""
        return self.idleFrames[0].width(), self.idleFrames[0].height()

    def get_current_frame(self):
        """Get current animation frame based on state and cycle."""
        if self.currentState == 0:  # Idle
            frame = self.idleFrames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.idleFrames)
        elif self.currentState == 1:  # Panic
            frame = self.panicFrames[self.cycle]
            self.cycle = (self.cycle + 1)
            if self.cycle > 4:
                self.cycle = 3
        elif self.currentState == 2:  # Hover
            frame = self.hoverFrames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.hoverFrames)
        else:  # Fallback to idle
            frame = self.idleFrames[0]
            self.currentState = 0
            self.cycle = 0

        return frame

    def set_state(self, newState):
        """Change animation state and reset cycle if needed."""
        if newState != self.currentState:
            self.currentState = newState
            self.cycle = 0

    def get_animation_speed(self):
        """Return animation speed based on current state."""
        speedMap = {
            0: 400,  # Idle - slower
            1: 100,  # Panic - faster
            2: 150   # Hover - medium
        }
        return speedMap.get(self.currentState, 400)