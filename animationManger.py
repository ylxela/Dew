import tkinter as tk

NUM_FRAMES_IDLE = 3
NUM_FRAMES_PANIC = 6
NUM_FRAMES_HOVER = 3
STATE_IDLE = 0
STATE_PANIC = 1
STATE_HOVER = 2
SPEED_IDLE = 400
SPEED_PANIC = 100
SPEED_HOVER = 150

class AnimationManager:
    def __init__(self):
        self.cycle = 0
        self.currentState = STATE_IDLE

        self.idleFrames = []
        self.panicFrames = []
        self.hoverFrames = []

    def load_animations(self):
        scale_factor = 2
        try:
            self.idleFrames = [tk.PhotoImage(file='idle.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                            for i in range(self.IDLE_FRAMES)]
            self.panicFrames = [tk.PhotoImage(file='panic.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                                for i in range(self.PANIC_FRAMES)]
            self.hoverFrames = [tk.PhotoImage(file='hover.gif', format='gif -index %i' % i).zoom(scale_factor, scale_factor)
                                for i in range(self.HOVER_FRAMES)]
        except Exception as e:
            raise FileNotFoundError(f"{e} not found")

    def getDimensions(self):
        return self.idleFrames[0].width(), self.idleFrames[0].height()

    def getCurrFrame(self):
        if self.currentState == STATE_IDLE:
            frame = self.idleFrames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.idleFrames)
        elif self.currentState == STATE_PANIC:
            frame = self.panicFrames[self.cycle]
            self.cycle = (self.cycle + 1)
            # get to frame 4, then repeat frames 3 to 4
            if self.cycle > 4:
                self.cycle = 3
        elif self.currentState == STATE_HOVER:
            frame = self.hoverFrames[self.cycle]
            self.cycle = (self.cycle + 1) % len(self.hoverFrames)
        else:
            # fallback to idle
            frame = self.idleFrames[0]
            self.currentState = STATE_IDLE
            self.cycle = 0

        return frame

    def setState(self, newState):
        if newState != self.currentState:
            self.currentState = newState
            self.cycle = 0

    def getAnimSpeed(self):
        speedMap = {
            STATE_IDLE: SPEED_IDLE,  # Idle - slower
            STATE_PANIC: SPEED_PANIC,  # Panic - faster
            STATE_HOVER: SPEED_HOVER   # Hover - medium
        }
        return speedMap.get(self.currentState, 400)