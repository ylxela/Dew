class MouseHandler:
    """Handles mouse interactions for pet dragging and clicking."""

    def __init__(self, pet_instance):
        self.pet = pet_instance
        self.dragStartX = 0
        self.dragStartY = 0
        self.clickStartPos = (0, 0)
        self.potentialDrag = False

    def on_button_press(self, event):
        """Handle mouse button press - prepare for drag or click."""
        self.clickStartPos = (event.x_root, event.y_root)
        self.potentialDrag = True

    def on_mouse_move(self, event):
        """Handle mouse movement - initiate drag if movement threshold exceeded."""
        if self.potentialDrag:
            dx = abs(event.x_root - self.clickStartPos[0])
            dy = abs(event.y_root - self.clickStartPos[1])
            if dx > 5 or dy > 5:
                self.potentialDrag = False
                self.start_drag(event)

        if self.pet.behavior.isDragging:
            self.drag_pet(event)

    def on_button_release(self, event):
        """Handle mouse button release - stop drag or trigger click action."""
        if self.pet.behavior.isDragging:
            self.stop_drag(event)
        elif self.potentialDrag:
            self.pet.openLoggingWindow()
        self.potentialDrag = False

    def start_drag(self, event):
        """Start drag operation and record initial position."""
        self.pet.behavior.start_drag()
        self.dragStartX = event.x
        self.dragStartY = event.y

    def drag_pet(self, event):
        """Update pet position during drag operation."""
        if self.pet.behavior.isDragging:
            newX = self.pet.window.winfo_pointerx() - self.dragStartX
            newY = self.pet.window.winfo_pointery() - self.dragStartY

            self.pet.x = newX
            self.pet.y = newY

            self.pet.window.geometry(f'{self.pet.petWidth}x{self.pet.petHeight}+{newX}+{newY}')

    def stop_drag(self, event):
        """Stop drag operation."""
        self.pet.behavior.stop_drag()

    def start_hover(self, event):
        """Handle mouse enter event."""
        self.pet.behavior.start_hover()

    def stop_hover(self, event):
        """Handle mouse leave event."""
        self.pet.behavior.stop_hover()

    def open_setup(self, event):
        """Handle right-click to open setup window."""
        self.pet.openSetupWindow()