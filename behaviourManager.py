class BehaviorManager:
    """Manages pet behavior states and transitions."""

    def __init__(self):
        self.is_dragging = False
        self.is_hovering = False

    def determine_behavior(self):
        """Determine current behavior state based on interactions."""
        if self.is_dragging:
            return 1  # Panic state
        elif self.is_hovering:
            return 2  # Water state
        else:
            return 0  # Idle state

    def start_drag(self):
        """Start dragging behavior."""
        self.is_dragging = True
        print("Dragging started - panic mode!")

    def stop_drag(self):
        """Stop dragging behavior."""
        self.is_dragging = False
        print("Dragging stopped - returning to normal behavior")

    def start_hover(self):
        """Start hover behavior."""
        if not self.is_dragging:
            self.is_hovering = True
            print("Mouse hover started - water mode!")

    def stop_hover(self):
        """Stop hover behavior."""
        if not self.is_dragging:
            self.is_hovering = False
            print("Mouse hover stopped - idle mode!")