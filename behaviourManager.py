class BehaviorManager:
    """Manages pet behavior states and transitions."""

    def __init__(self):
        self.isDragging = False
        self.isHovering = False

    def determine_behavior(self):
        """Return current behavior state based on interactions."""
        if self.isDragging:
            return 1  # Panic state
        elif self.isHovering:
            return 2  # Hover state
        else:
            return 0  # Idle state

    def start_drag(self):
        """Start dragging behavior."""
        self.isDragging = True

    def stop_drag(self):
        """Stop dragging behavior."""
        self.isDragging = False

    def start_hover(self):
        """Start hover behavior."""
        if not self.isDragging:
            self.isHovering = True

    def stop_hover(self):
        """Stop hover behavior."""
        if not self.isDragging:
            self.isHovering = False