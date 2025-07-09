import tkinter as tk
from tkinter import messagebox, ttk
import time
import os

POPUP_INTERVAL = 60 * 60      # 1 hour in seconds
POPUP_DURATION = 2 * 60       # 2 minutes in seconds

# Manages UI windows and dialogs.
class UIManager:
    def __init__(self, pet):
        self.pet = pet
        self.popUpVisible = False
        self.popup = None
        self.preferencesWindow = None
        self.bgFrame = []
        self.bgCurrentFrame = 0
        self.bgLabel = None
        self.bgAnimationRunning = False
        self.hamsterImg = None

    def loadBackgroundFrames(self):
        try:
            self.bgFrame = []
            frameIndex = 0

            while True:
                try:
                    frame = tk.PhotoImage(file='assets/water logger.gif', format='gif -index %i' % frameIndex)
                    scaled_frame = frame.zoom(2, 2)
                    self.bgFrame.append(scaled_frame)
                    frameIndex += 1
                except tk.TclError:
                    break

            return len(self.bgFrame) > 0
        except Exception as e:
            print(f"Error loading background frames: {e}")
            return False

    def animateBackground(self):
        if not self.bgAnimationRunning or not self.bgFrame or not self.bgLabel:
            return

        current_frame = self.bgFrame[self.bgCurrentFrame]
        self.bgLabel.configure(image=current_frame)

        self.bgCurrentFrame = (self.bgCurrentFrame + 1) % len(self.bgFrame)

        if self.preferencesWindow and self.preferencesWindow.winfo_exists():
            self.preferencesWindow.after(200, self.animateBackground)

    def stopBackgroundAnimation(self):
        self.bgAnimationRunning = False
        self.bgCurrentFrame = 0
        self.bgLabel = None

    def openSetup(self):
        if self.preferencesWindow is not None:
            self.stopBackgroundAnimation()
            self.preferencesWindow.destroy()

        self.preferencesWindow = tk.Toplevel(self.pet.window)
        self.preferencesWindow.title("Preferences")
        self.preferencesWindow.geometry("1400x1060")
        self.preferencesWindow.resizable(False, False)
        self.preferencesWindow.attributes("-topmost", True)
        self.preferencesWindow.lift(self.pet.window)

        try:
            self.hamsterImg = tk.PhotoImage(file="assets/water logging hamster.png")
        except Exception:
            self.hamsterImg = None

        if os.path.exists("assets/water logger.gif") and self.loadBackgroundFrames():
            self.bgLabel = tk.Label(self.preferencesWindow)
            self.bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

            self.bgAnimationRunning = True
            self.animateBackground()
        else:
            self.preferencesWindow.configure(bg='#4A90E2')

        try:
            import tkinter.font as tkfont
            pressStartFont = tkfont.Font(family="Press Start 2P", size=12)
        except Exception:
            pressStartFont = None

        panelWidth = 800
        panelHeight = 600
        panelX = (1400 - panelWidth) // 2
        panelY = (1060 - panelHeight) // 2 + 80
        canvas = tk.Canvas(self.preferencesWindow, width=panelWidth, height=panelHeight, highlightthickness=0)
        canvas.place(x=panelX, y=panelY)
        canvas.create_rectangle(0, 0, panelWidth, panelHeight, fill="#f3f3f3", outline="")

        content = tk.Frame(canvas, bg="#f3f3f3")
        content.place(relx=0.5, rely=0.5, anchor="center")

        if self.hamsterImg:
            hamster_x = (1400 - self.hamsterImg.width()) // 2
            self.hamster_label = tk.Label(self.preferencesWindow, image=self.hamsterImg, bd=0, bg="#f3f3f3")
            self.hamster_label.place(x=hamster_x, y=panelY - self.hamsterImg.height() - 10)
            self.hamster_label.lift()

        header = tk.Label(content, text="Preferences", bg="#f3f3f3", fg="#000000")
        if pressStartFont:
            header.configure(font=("Press Start 2P", 20))
        else:
            header.configure(font=("Helvetica", 20, "bold"))
        header.pack(pady=(10, 30))

        def createSliderRow(parent, labelText, unitText, rangeFrom, rangeTo, step, defaultVal):
            row = tk.Frame(parent, bg="#f3f3f3")
            row.pack(fill="x", padx=40, pady=20)

            left_lbl = tk.Label(row, text=labelText, bg="#f3f3f3")
            right_lbl = tk.Label(row, text=unitText, bg="#f3f3f3")
            font_def = ("Press Start 2P", 12) if pressStartFont else ("Helvetica", 12, "bold")
            left_lbl.configure(font=font_def)
            right_lbl.configure(font=font_def)
            left_lbl.pack(side="left")
            right_lbl.pack(side="right")

            style_name = f"{labelText.replace(' ', '')}.Horizontal.TScale"
            style = ttk.Style()
            style.theme_use("default")
            style.configure(style_name, troughcolor="#eeeeee", background="#edb36a")

            var = tk.IntVar(value=defaultVal)
            scale = ttk.Scale(row, from_=rangeFrom, to=rangeTo, orient="horizontal", style=style_name, variable=var, length=600)
            scale.pack(side="bottom", pady=10)

            def snap(event):
                val = round(var.get() / step) * step
                var.set(val)
            scale.bind("<ButtonRelease-1>", snap)

            tooltip = tk.Label(row, text="", bg="#000000", fg="#FFFFFF", padx=4, pady=2)
            tooltip_font = ("Press Start 2P", 8) if pressStartFont else ("Helvetica", 8)
            tooltip.configure(font=tooltip_font)

            def move_tooltip(event):
                tooltip.configure(text=f"{var.get()} mL")
                tooltip.place(x=event.x, y=event.y)
            def hide_tooltip(event):
                tooltip.place_forget()
            scale.bind("<Motion>", move_tooltip)
            scale.bind("<Leave>", hide_tooltip)
            return var

        goalVar = createSliderRow(content, "Daily Goal", "(mL)", 0, 4000, 500, self.pet.config.dailyGoal)
        sipVar = createSliderRow(content, "Sip Amount", "(mL)", 0, 1000, 250, self.pet.config.sipAmount)

        # Save button
        saveBtn = tk.Button(content, text="Save", bg="#b41c27", fg="#FFFFFF", activebackground="#992026", padx=20, pady=10, bd=0)
        btnFont = ("Press Start 2P", 12) if pressStartFont else ("Helvetica", 12, "bold")
        saveBtn.configure(font=btnFont)
        saveBtn.pack(pady=(40, 10))

        def save_preferences():
            self.pet.config.dailyGoal = int(goalVar.get())
            self.pet.config.sipAmount = int(sipVar.get())
            messagebox.showinfo("Saved", "Preferences updated.")
            self.stopBackgroundAnimation()
            self.preferencesWindow.destroy()
            self.preferencesWindow = None
        saveBtn.configure(command=save_preferences)

        def onClosing():
            self.stopBackgroundAnimation()
            self.preferencesWindow.destroy()
            self.preferencesWindow = None

        self.preferencesWindow.protocol("WM_DELETE_WINDOW", onClosing)

    def openSetupFallback(self):
        self.preferencesWindow = tk.Toplevel(self.pet.window)
        self.preferencesWindow.title("Dew - Preferences")
        self.preferencesWindow.geometry("500x300")
        self.preferencesWindow.attributes("-topmost", True)

        tk.Label(self.preferencesWindow, text="Daily Goal (ml)").grid(row=0, column=0, padx=10, pady=5)
        goalVar = tk.StringVar(value=str(self.pet.config.dailyGoal))
        tk.Entry(self.preferencesWindow, textvariable=goalVar, width=10).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.preferencesWindow, text="Sip Amount (ml)").grid(row=1, column=0, padx=10, pady=5)
        sipVar = tk.StringVar(value=str(self.pet.config.sipAmount))
        tk.Entry(self.preferencesWindow, textvariable=sipVar, width=10).grid(row=1, column=1, padx=10, pady=5)

        def save():
            try:
                self.pet.config.dailyGoal = int(goalVar.get())
                self.pet.config.sipAmount = int(sipVar.get())
                messagebox.showinfo("Saved", "Preferences updated.")
                self.preferencesWindow.destroy()
                self.preferencesWindow = None
            except ValueError:
                messagebox.showerror("Error", "Invalid input")

        ttk.Button(self.preferencesWindow, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=10)

        def onClosing():
            self.preferencesWindow.destroy()
            self.preferencesWindow = None

        self.preferencesWindow.protocol("WM_DELETE_WINDOW", onClosing)

    def openLog(self):
        popup = tk.Toplevel(self.pet.window)
        popup.title("Log Water")
        popup.attributes("-topmost", True)
        popup.geometry(f"200x120+{self.pet.x+110}+{self.pet.y}")

        tk.Label(popup, text = f"Log {self.pet.config.sipAmount} ml water?").pack(pady = 5)

        progress = ttk.Progressbar(popup, maximum = self.pet.config.dailyGoal,
                                  value = self.pet.config.currentIntake, length = 160)
        progress.pack(pady = 5)

        progLabel = tk.Label(popup, text = f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
        progLabel.pack()

        def logWater():
            self.pet.config.addIntake(self.pet.config.sipAmount)
            self.pet.config.lastIntakeTime = time.time()
            progress["value"] = self.pet.config.currentIntake
            progLabel.config(text = f"{self.pet.config.currentIntake}/{self.pet.config.dailyGoal} ml")
            if self.pet.config.currentIntake >= self.pet.config.dailyGoal:
                messagebox.showinfo("Congrats!", "You've met today's hydration goal!")
            popup.destroy()

        ttk.Button(popup, text="Drink", command=logWater).pack(pady=5)

    def runReminder(self):
        self.pet.window.after(POPUP_INTERVAL * 1000, self.showPopUp)

    def showPopUp(self):
        self.pet.behaviour.setBehaviour(2)
        if self.popUpVisible:
            return

        lastTime = self.pet.config.lastIntakeTime or 0
        timeSinceLastIntake = time.time() - lastTime

        if timeSinceLastIntake < POPUP_INTERVAL:
            self.pet.window.after(1000, self.runReminder)
            return

        self.popup = tk.Toplevel(self.pet.window)
        self.popup.title("Hourly Reminder")
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        transparentColour = "magenta"
        self.popup.configure(bg=transparentColour)
        self.popup.attributes("-transparentcolor", transparentColour)

        photo = tk.PhotoImage(file="assets/thirsty.gif")
        self.photo = photo.subsample(5, 5)

        image_label = tk.Label(self.popup, image=self.photo, bg=transparentColour)
        image_label.pack()

        self.popUpVisible = True
        self.updatePopUpPosition()

        self.pet.window.after(POPUP_DURATION * 1000, self.close_popup)
        self.pet.window.after(POPUP_INTERVAL * 1000, self.showPopUp)

    def updatePopUpPosition(self):
        if not self.popup or not self.popUpVisible:
            return

        popupWidth = 200
        popupHeight = 100

        petX = self.pet.x
        petY = self.pet.y
        pet_width = self.pet.petWidth

        popupX = petX + (pet_width // 2) - (popupWidth // 2)
        popupY = petY - popupHeight + 50

        self.popup.geometry(f"{popupWidth}x{popupHeight}+{popupX}+{popupY}")

        self.pet.window.after(100, self.updatePopUpPosition)

    def close_popup(self):
        if self.popup:
            self.pet.behaviour.setBehaviour(0)
            self.popup.destroy()
            self.popup = None
            self.popUpVisible = False
