STATE_IDLE = 0
STATE_PANIC = 1
STATE_HOVER = 2

#Handles mouse interactions for pet dragging and clicking.
class MouseHandler:
    def __init__(self, pet):
        self.pet = pet
        self.dragStartX = 0
        self.dragStartY = 0
        self.clickStartPos = (0, 0)
        self.potentialDrag = False

    def pressLeft(self, event):
        self.clickStartPos = (event.x_root, event.y_root)
        self.potentialDrag = True

    def mouseMove(self, event):
        if self.potentialDrag:
            dx = abs(event.x_root - self.clickStartPos[0])
            dy = abs(event.y_root - self.clickStartPos[1])
            if dx > 5 or dy > 5:
                self.potentialDrag = False
                self.startDrag(event)
        elif self.pet.behaviour.isDragging():
            self.dragPet(event)

    def releaseLeft(self, event):
        if self.pet.behaviour.isDragging():
            self.endDrag(event)
        elif self.potentialDrag:
            self.pet.openLoggingWindow()
        self.potentialDrag = False

    def startDrag(self, event):
        self.pet.behaviour.setBehaviour(STATE_PANIC)
        self.dragStartX = event.x
        self.dragStartY = event.y

    def dragPet(self, event):
        if self.pet.behaviour.isDragging():
            newX = self.pet.window.winfo_pointerx() - self.dragStartX
            newY = self.pet.window.winfo_pointery() - self.dragStartY

            self.pet.x = newX
            self.pet.y = newY

            self.pet.window.geometry(f'{self.pet.petWidth}x{self.pet.petHeight}+{newX}+{newY}')

    def endDrag(self, event):
        self.pet.behaviour.setBehaviour(STATE_IDLE)

    def startHover(self, event):
        if not self.pet.behaviour.isDragging():
            self.pet.behaviour.setBehaviour(STATE_HOVER)

    def endHover(self, event):
        if not self.pet.behaviour.isDragging():
            self.pet.behaviour.setBehaviour(STATE_IDLE)

    def openSetup(self, event):
        self.pet.openSetupWindow()