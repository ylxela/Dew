class MouseHandler:
    """Handles all mouse interactions including dragging and clicking."""

    def __init__(self, pet_instance):
        self.pet = pet_instance
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.click_start_pos = (0, 0)
        self.potential_drag = False

    def on_button_press(self, event):
        """Handle mouse button press."""
        self.click_start_pos = (event.x_root, event.y_root)
        self.potential_drag = True

    def on_mouse_move(self, event):
        """Handle mouse movement."""
        if self.potential_drag:
            dx = abs(event.x_root - self.click_start_pos[0])
            dy = abs(event.y_root - self.click_start_pos[1])
            if dx > 5 or dy > 5:
                self.potential_drag = False
                self.start_drag(event)

        if self.pet.behavior.is_dragging:
            self.drag_pet(event)

    def on_button_release(self, event):
        """Handle mouse button release."""
        if self.pet.behavior.is_dragging:
            self.stop_drag(event)
        elif self.potential_drag:
            # Treat as click - open logger
            self.pet.open_logging_window()
        self.potential_drag = False

    def start_drag(self, event):
        """Start drag operation."""
        self.pet.behavior.start_drag()
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def drag_pet(self, event):
        """Handle pet dragging."""
        if self.pet.behavior.is_dragging:
            # Calculate new position based on mouse movement
            new_x = self.pet.window.winfo_pointerx() - self.drag_start_x
            new_y = self.pet.window.winfo_pointery() - self.drag_start_y

            # Update pet position
            self.pet.x = new_x
            self.pet.y = new_y

            # Move the window
            self.pet.window.geometry(f'{self.pet.pet_width}x{self.pet.pet_height}+{new_x}+{new_y}')

    def stop_drag(self, event):
        """Stop drag operation."""
        self.pet.behavior.stop_drag()

    def start_hover(self, event):
        """Handle mouse enter."""
        self.pet.behavior.start_hover()

    def stop_hover(self, event):
        """Handle mouse leave."""
        self.pet.behavior.stop_hover()

    def open_setup(self, event):
        """Handle right-click to open setup."""
        self.pet.open_setup_window()