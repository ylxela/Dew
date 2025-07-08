import tkinter as tk
import random

# ==============================================================================
# CONFIGURATION AND INITIAL SETUP
# ==============================================================================

# Pet position and animation variables
x = 100  # Initial x position of the pet
y = 150  # Initial y position of the pet
cycle = 0  # Current frame index for animations
check = 0  # Current state/behavior of the pet (0=idle, 1=panic, 2=water)

# Interaction state variables
is_dragging = False  # Flag to track if pet is being dragged
is_hovering = False  # Flag to track if mouse is hovering over pet
drag_start_x = 0  # Starting x position for drag
drag_start_y = 0  # Starting y position for drag

pet_width = 65  # Default width, will be updated
pet_height = 64  # Default height, will be updated

# Remove the old behavior number ranges since we're not using random events anymore
# Define animation frame counts for easy reference
IDLE_FRAMES = 3
PANIC_FRAMES = 6
WATER_FRAMES = 3  # This will be updated when we load the actual frames

# Image path for GIF files (using raw string to handle backslashes)
impath = ''

# ==============================================================================
# MOUSE INTERACTION FUNCTIONS
# ==============================================================================

def start_drag(event):
    """
    Initiates drag operation when mouse button is pressed on the pet.

    Args:
        event: Tkinter event object containing mouse coordinates
    """
    global is_dragging, drag_start_x, drag_start_y, check, cycle

    is_dragging = True
    drag_start_x = event.x
    drag_start_y = event.y

    # Switch to panic state when dragging starts
    check = 1  # Panic state
    cycle = 0  # Reset animation cycle
    print("Dragging started - panic mode!")


def drag_pet(event):
    """
    Handles pet movement during drag operation.

    Args:
        event: Tkinter event object containing mouse coordinates
    """
    global x, y, is_dragging

    if is_dragging:
        # Calculate new position based on mouse movement
        new_x = window.winfo_pointerx() - drag_start_x
        new_y = window.winfo_pointery() - drag_start_y

        # Update pet position variables - THIS IS THE KEY FIX
        x = new_x
        y = new_y

        # Move the window to new position
        window.geometry(f'{pet_width}x{pet_height}+{new_x}+{new_y}')


def stop_drag(event):
    """
    Ends drag operation when mouse button is released.

    Args:
        event: Tkinter event object
    """
    global is_dragging, check, cycle

    if is_dragging:
        is_dragging = False
        print("Dragging stopped - returning to normal behavior")

        # Reset animation cycle
        cycle = 0


def start_hover(event):
    """
    Called when mouse enters the pet area.

    Args:
        event: Tkinter event object
    """
    global is_hovering, check, cycle

    if not is_dragging:  # Only switch to hover if not dragging
        is_hovering = True
        check = 2  # Water state
        cycle = 0  # Reset animation cycle
        print("Mouse hover started - water mode!")


def stop_hover(event):
    """
    Called when mouse leaves the pet area.

    Args:
        event: Tkinter event object
    """
    global is_hovering, check, cycle

    if not is_dragging:  # Only switch to idle if not dragging
        is_hovering = False
        check = 0  # Idle state
        cycle = 0  # Reset animation cycle
        print("Mouse hover stopped - idle mode!")


# ==============================================================================
# BEHAVIOR CONTROL FUNCTIONS
# ==============================================================================

def determine_behavior():
    """
    Determines the pet's behavior based on current interaction state.

    Returns:
        int: Behavior state (0=idle, 1=panic, 2=water)
    """
    global is_dragging, is_hovering

    if is_dragging:
        return 1  # Panic state
    elif is_hovering:
        return 2  # Water state
    else:
        return 0  # Idle state


def update_animation():
    """
    Main update function that handles animation frame updates and pet behavior.
    """
    global cycle, check, is_dragging, x, y

    # Determine current behavior based on interaction state
    new_check = determine_behavior()

    # If behavior changed, reset animation cycle
    if new_check != check:
        cycle = 0
        check = new_check

    # Select appropriate animation frame and advance cycle
    if check == 0:  # Idle state
        frame = idle[cycle]
        cycle = (cycle + 1) % len(idle)

    elif check == 1:  # Panic state
        frame = panic[cycle]
        cycle = (cycle + 1)
        if (cycle > 4): cycle = 3

    elif check == 2:  # Water state
        frame = water[cycle]
        cycle = (cycle + 1) % len(water)

    else:  # Fallback to idle
        frame = idle[0]
        check = 0
        cycle = 0

    # Update window position using global coordinates (dragging updates this)
    if not is_dragging:
        window.geometry(f'{pet_width}x{pet_height}+{x}+{y}')

    # Always update the image
    label.configure(image=frame)

    # Schedule next update - different speeds for different animations
    if check == 0:  # Idle - slower animation
        window.after(400, update_animation)
    elif check == 1:  # Panic - faster animation
        window.after(100, update_animation)
    elif check == 2:  # Water - medium speed animation
        window.after(150, update_animation)
    else:
        window.after(400, update_animation)  # Default fallback


# ==============================================================================
# WINDOW AND GRAPHICS SETUP
# ==============================================================================

# Create main window
window = tk.Tk()

try:
    # Load all GIF animations by extracting individual frames
    idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % (i)) for i in range(IDLE_FRAMES)]
    panic = [tk.PhotoImage(file=impath + 'panic.gif', format='gif -index %i' % (i)) for i in range(PANIC_FRAMES)]
    water = [tk.PhotoImage(file=impath + 'water.gif', format='gif -index %i' % (i)) for i in range(WATER_FRAMES)]
    pet_width = idle[0].width()
    pet_height = idle[0].height()
    print("GIF files loaded successfully!")
except Exception as e:
    print(f"Error loading GIF files: {e}")
    print("Make sure the GIF files exist in the specified directory.")
    exit()


# Configure window appearance
window.config(highlightbackground='black')  # Set background color
window.overrideredirect(True)  # Remove window decorations
window.wm_attributes('-transparentcolor', 'black')  # Make black pixels transparent

# FIXED: Make window always stay on top of other applications
window.wm_attributes('-topmost', True)

# Create label to display the pet animations
label = tk.Label(window, bd=0, bg='black')
label.pack()

# Bind mouse events for drag and drop functionality
label.bind("<Button-1>", start_drag)        # Left mouse button press
label.bind("<B1-Motion>", drag_pet)         # Mouse movement while button held
label.bind("<ButtonRelease-1>", stop_drag)  # Left mouse button release

# Bind mouse events for hover functionality
label.bind("<Enter>", start_hover)          # Mouse enters pet area
label.bind("<Leave>", stop_hover)           # Mouse leaves pet area

# ==============================================================================
# START THE PROGRAM
# ==============================================================================

window.geometry(f'{pet_width}x{pet_height}+{x}+{y}')

# Start the animation loop
window.after(1, update_animation)

# Start the main GUI loop
window.mainloop()