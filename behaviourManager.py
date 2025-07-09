STATE_IDLE = 0
STATE_PANIC = 1
STATE_HOVER = 2

class BehaviourManager:
    def __init__(self):
        self.state = STATE_IDLE

    def getBehaviour(self):
        return self.state
    
    def setBehaviour(self, state):
        self.state = state

    def isDragging(self):
        return (self.state == STATE_PANIC)