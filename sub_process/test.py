import tkinter as tk
from PIL import ImageGrab
import pyautogui
import os

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        window_width = 360
        window_height = 230

        self.title("")
        self.geometry(f"{window_width}x{window_height}")

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=1)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width - window_width - 5
        y = screen_height - window_height - 80

        self.geometry(f"+{x}+{y}")

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self.label = tk.Label(self, text="メイン画面")
        self.label.pack(pady=10)
        
        self.button = tk.Button(self, text="スクリーンキャプチャを開始", command=self.open_screen_capture)
        self.button.pack(expand=True)

    def open_screen_capture(self):
        self.withdraw()  # メインウィンドウを非表示にする
        screen_capture = ScreenCaptureApp(self)

    def on_return(self):
        # スクリーンキャプチャから戻ってきたときに実行したい関数
        self.label.config(text="キャプチャが完了しました！")
        print("スクリーンキャプチャが完了しました")

class ScreenCaptureApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.1)
        self.configure(background='black')
        self.bind('<Escape>', self.close_window)
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.canvas = tk.Canvas(self, cursor="cross", bg="black")
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
        self.master.deiconify()
        self.master.on_return()
        self.destroy()
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
        self.master.deiconify()
        self.master.on_return()
        self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()