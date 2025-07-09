import tkinter as tk
from UIManager import UIManager
from behaviourManager import BehaviourManager
from configManager import ConfigManager
from animationManger import AnimationManager
from mouseManager import MouseHandler

FRAME_WIDTH = 100
FRAME_HEIGHT = 150
DELAY_SETUP_WINDOW = 500
DELAY_FRAME_STEP = 1

class DesktopPet:
    def __init__(self):
        # init components
        self.x = FRAME_WIDTH
        self.y = FRAME_HEIGHT
        self.animation = AnimationManager()
        self.behaviour = BehaviourManager()
        self.mouseHandler = MouseHandler(self)
        self.uiManager = UIManager(self)
        # init window
        self.window = None
        self.label = None
        self.petWidth = 0
        self.petHeight = 0
        self.config = None
        self.setupWindow()

    def setupWindow(self):
        self.window = tk.Tk()
        self.animation.loadAnimations()
        self.petWidth, self.petHeight = self.animation.getDimensions()

        self.window.config(highlightbackground = 'black')
        self.window.overrideredirect(True) # removes border
        self.window.wm_attributes('-transparentcolor', 'black') # todo: change transparent colour
        self.window.wm_attributes('-topmost', True)

        self.label = tk.Label(self.window, bd = 0, bg = 'black')
        self.label.pack()

        self.config = ConfigManager()
        self.bindMouseEvents()

        # modify this line to change the spawn position
        self.window.geometry(f'{self.petWidth}x{self.petHeight}+{self.x}+{self.y}')

    def bindMouseEvents(self):
        self.label.bind("<Button-1>", self.mouseHandler.pressLeft)
        self.label.bind("<B1-Motion>", self.mouseHandler.mouseMove)
        self.label.bind("<ButtonRelease-1>", self.mouseHandler.releaseLeft)
        self.label.bind("<Enter>", self.mouseHandler.startHover)
        self.label.bind("<Leave>", self.mouseHandler.endHover)
        self.label.bind("<Button-3>", self.mouseHandler.openSetup)

    def updateAnimation(self):
        newState = self.behaviour.getBehaviour()
        self.animation.setState(newState)

        frame = self.animation.getCurrFrame()

        if not self.behaviour.isDragging:
            # update window position
            self.window.geometry(f'{self.petWidth}x{self.petHeight}+{self.x}+{self.y}')

        self.label.configure(image = frame)
        speed = self.animation.getAnimSpeed()
        self.window.after(speed, self.updateAnimation)

    def openSetupWindow(self):
        self.uiManager.openSetup()

    def openLoggingWindow(self):
        self.uiManager.openLog()

    def run(self):
        if self.config.data.get("lastResetDate") is None:
            self.window.after(DELAY_SETUP_WINDOW, self.openSetupWindow)

        # start animation loop
        self.window.after(DELAY_FRAME_STEP, self.updateAnimation)
        # start main GUI loop
        self.window.mainloop()

pet = DesktopPet()
pet.run()

