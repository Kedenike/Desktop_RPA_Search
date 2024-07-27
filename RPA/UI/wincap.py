import tkinter as tk
from PIL import ImageGrab
import pyautogui
import os

class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.1)
        self.root.configure(background='black')
        self.root.bind('<Escape>', self.close_window)
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='#06D001', width=3)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.root.destroy()
        self.capture_screen(self.start_x, self.start_y, end_x, end_y)

    def capture_screen(self, start_x, start_y, end_x, end_y):
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        os.makedirs(os.path.dirname("image/screenshot.jpeg"), exist_ok=True)
        screenshot.save("image/screenshot.jpeg")
        print("スクリーンショットが保存されました: screenshot.jpeg")

    def close_window(self, event):
        self.root.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.mainloop()
