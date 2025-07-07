import tkinter as tk
from PIL import Image, ImageTk

class Sprite:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # borderless
        root.wm_attributes('-transparentcolor', 'white') # white pixels = transparent
        self.root.wm_attributes("-topmost", True)  # keep on top
        self.root.config()
        self.animations = {
            "idle": self.load_img("idle.gif"),
            "drag": self.load_img("drag.gif"),
        }
        self.curr_state = "idle"

        self.label = tk.Label(root)
        self.label.pack()

        self.curr_frame = 0
        self.update_frame()

    # Load the GIF
    def load_img(self, path):
        frames = []
        gif = Image.open(path)
        try:
            while True:
                frame = gif.copy().resize((160, 160), Image.Resampling.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(frames))
        except EOFError:
            pass
        return frames


    def update_frame(self):
        frames = self.animations[self.curr_state]
        frame = frames[self.curr_frame]
        self.label.config(image=frame)
        self.curr_frame = (self.curr_frame + 1) % len(frames)
        self.root.after(100, self.update_frame)

    
    def toggle_visibility(self, event):
        if root.state() == 'normal':
            root.withdraw()
        else:
            root.deiconify()
    
    def drag(self, event):
        self.curr_state = "drag"
        self.curr_frame = 0

    def idle(self, event):
        self.curr_state = "idle"
        self.curr_frame = 0



root = tk.Tk()
root.focus_force()
app = Sprite(root)
root.bind('<space>', app.toggle_visibility)
root.bind('i', app.idle)
root.bind('d', app.drag)
root.mainloop()