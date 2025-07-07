import tkinter as tk
from PIL import Image, ImageTk

class Sprite:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # borderless
        root.wm_attributes('-transparentcolor', 'white') # white pixels = transparent
        self.root.wm_attributes("-topmost", True)  # keep on top
        self.root.config()

        # Load the GIF
        self.frames = []
        gif = Image.open("img.gif")
        try:
            while True:
                frame = gif.copy().resize((160, 160), Image.Resampling.LANCZOS)  # todo: resize to what we need
                frame = ImageTk.PhotoImage(frame)
                self.frames.append(frame)
                gif.seek(len(self.frames))
        except EOFError:
            pass


        self.label = tk.Label(root)
        self.label.pack()

        self.current_frame = 0
        self.update_frame()

    def update_frame(self):
        frame = self.frames[self.current_frame]
        self.label.config(image=frame)
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.root.after(100, self.update_frame)  # Adjust timing as needed

root = tk.Tk()
app = Sprite(root)
root.mainloop()