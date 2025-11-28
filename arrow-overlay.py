import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import sys
import os

class ArrowOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arrow Overlay")
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.overrideredirect(True)
        self.root.geometry("100x100")
        self.root.withdraw()  # Hide initially
        
        # Create a canvas for drawing arrows
        self.canvas = tk.Canvas(self.root, width=100, height=100, bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Create arrow images with proper offsets for tip alignment
        self.arrows = {
            'up': self.create_arrow_image('up'),
            'down': self.create_arrow_image('down'),
            'left': self.create_arrow_image('left'),
            'right': self.create_arrow_image('right')
        }
        
        # Arrow tip positions within the 100x100 window
        self.tip_positions = {
            'up': (50, 5),    # Tip is at top center
            'down': (50, 95), # Tip is at bottom center  
            'left': (5, 50),  # Tip is at left center
            'right': (95, 50) # Tip is at right center
        }
        
        # Set up keyboard hooks
        self.setup_keyboard_hooks()
        
        # Flag to track if an arrow is currently displayed
        self.arrow_active = False
        
        # Create system tray icon (simplified - using a small control window)
        self.create_control_window()
        
    def create_control_window(self):
        """Create a small control window for exiting the application"""
        self.control = tk.Toplevel(self.root)
        self.control.title("Arrow Overlay Control")
        self.control.geometry("250x100")
        self.control.attributes("-topmost", False)
        
        label = tk.Label(self.control, text="Arrow Overlay is running\nPress Shift + Arrow Keys to show arrows", 
                        pady=10)
        label.pack()
        
        quit_btn = tk.Button(self.control, text="Quit Application", command=self.quit_app,
                           bg="#ff6b6b", fg="white", font=("Arial", 10, "bold"))
        quit_btn.pack(pady=5)
        
        # Make sure control window closes with main app
        self.control.protocol("WM_DELETE_WINDOW", self.quit_app)
    
    def create_arrow_image(self, direction):
        """Create an arrow image pointing in the specified direction"""
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Define arrow coordinates based on direction
        if direction == 'up':
            points = [(50, 5), (30, 45), (40, 45), (40, 85), (60, 85), (60, 45), (70, 45)]
        elif direction == 'down':
            points = [(50, 95), (30, 55), (40, 55), (40, 15), (60, 15), (60, 55), (70, 55)]
        elif direction == 'left':
            points = [(5, 50), (45, 30), (45, 40), (85, 40), (85, 60), (45, 60), (45, 70)]
        elif direction == 'right':
            points = [(95, 50), (55, 30), (55, 40), (15, 40), (15, 60), (55, 60), (55, 70)]
        
        # Draw the arrow with orange fill
        draw.polygon(points, fill=(255, 165, 0, 255), outline=(200, 130, 0, 255), width=2)
        
        return ImageTk.PhotoImage(img)
    
    def setup_keyboard_hooks(self):
        """Set up keyboard hooks for Shift + Arrow key combinations"""
        keyboard.add_hotkey('shift+up', lambda: self.show_arrow('up'))
        keyboard.add_hotkey('shift+down', lambda: self.show_arrow('down'))
        keyboard.add_hotkey('shift+left', lambda: self.show_arrow('left'))
        keyboard.add_hotkey('shift+right', lambda: self.show_arrow('right'))
    
    def show_arrow(self, direction):
        """Display the arrow with tip at the current mouse position"""
        if self.arrow_active:
            return  # Don't show multiple arrows at once
            
        self.arrow_active = True
        
        # Get current mouse position
        x, y = self.root.winfo_pointerxy()
        
        # Calculate position so arrow tip aligns with mouse cursor
        tip_x, tip_y = self.tip_positions[direction]
        window_x = x - tip_x  # Position window so tip is at mouse X
        window_y = y - tip_y  # Position window so tip is at mouse Y
        
        # Position the overlay window
        self.root.geometry(f"100x100+{window_x}+{window_y}")
        
        # Clear canvas and display the appropriate arrow
        self.canvas.delete("all")
        self.canvas.create_image(50, 50, image=self.arrows[direction])
        
        # Make the window click-through
        self.make_click_through()
        
        # Show the window
        self.root.deiconify()
        
        # Schedule the arrow to disappear after 2 seconds
        threading.Thread(target=self.hide_after_delay, daemon=True).start()
    
    def make_click_through(self):
        """Make the window click-through on supported platforms"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                # Set window to be click-through
                style = ctypes.windll.user32.GetWindowLongA(hwnd, -20)
                ctypes.windll.user32.SetWindowLongA(hwnd, -20, style | 0x80000 | 0x20)
        except Exception as e:
            print(f"Click-through not supported: {e}")
    
    def hide_after_delay(self):
        """Hide the arrow after 2 seconds"""
        time.sleep(2)
        self.root.after(0, self.hide_arrow)
    
    def hide_arrow(self):
        """Hide the arrow overlay"""
        self.root.withdraw()
        self.arrow_active = False
    
    def quit_app(self):
        """Clean up and exit the application"""
        keyboard.unhook_all()
        self.root.quit()
        self.root.destroy()
        if hasattr(self, 'control'):
            self.control.destroy()
        sys.exit(0)
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.quit_app()

if __name__ == "__main__":
    # Hide console window on Windows
    try:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    print("Arrow Overlay Started")
    print("A control window will appear - use it to quit the application")
    
    app = ArrowOverlay()
    app.run()
