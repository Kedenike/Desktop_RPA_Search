import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sub_process import gpt, sc_delete, flow, wincap
import asyncio
import threading

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # ウィンドウサイズを設定
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

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        second_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=second_frame, anchor="nw")

        self.input_field = tk.Text(second_frame, height=3, width=50)
        self.input_field.pack(pady=5)

        self.callback_field = tk.Text(second_frame, height=9, width=50, state='disabled')
        self.callback_field.pack(pady=0)

        self.img_label = tk.Label(second_frame)
        self.img_label.pack()

        button_frame = tk.Frame(second_frame)
        button_frame.pack(pady=0)

        self.search_mode = tk.StringVar(value="search")
        radio_search = tk.Radiobutton(button_frame, text="サーチ", variable=self.search_mode, value="search")
        radio_search.pack(side=tk.LEFT, padx=10)
        radio_rpa = tk.Radiobutton(button_frame, text="RPA", variable=self.search_mode, value="rpa")
        radio_rpa.pack(side=tk.LEFT, padx=10)

        capture_button = tk.Button(button_frame, text="画面キャプチャ", command=self.capture_button_tapped)
        capture_button.pack(side=tk.LEFT, padx=10)

        search_button = tk.Button(button_frame, text="検索", command=self.search_button_tapped)
        search_button.pack(side=tk.LEFT, padx=10)
        
    def capture_button_tapped(self):
        self.withdraw()  # メインウィンドウを非表示にする
        _ = wincap.ScreenCaptureApp(self)

    def on_return_capture(self):
        self.update_image()

    def update_image(self):
        try:
            img = Image.open("image/screenshot.jpeg")
            img = img.resize((200, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.img_label.config(image=img)
            self.img_label.image = img
            self.geometry("360x330")
            print("update_image")

        except Exception as e:
            self.callback_field_ins(f"画像ファイルを認識できませんでした: {e}")

    def launch_gpt(self, text):
        try:
            async def wrapper(text):
                result = await gpt.search_gpt_image(text=text)
                self.callback_field_ins(result)
                self.img_label.config(image='')
                self.img_label.image = None
                sc_delete.delete_screenshot()

            input_path = "image/screenshot.jpeg"
            img = Image.open(input_path)
            threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()

        except FileNotFoundError:
            async def wrapper(text):
                result = await gpt.search_gpt(text)
                self.callback_field_ins(result)
            threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()
                
    def launch_gpt_rpa(self, text):
        async def wrapper(text):
            await flow.flow(text)
            self.callback_field_ins("終わったよ")
        threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()

    def callback_field_ins(self, text):
        self.callback_field.config(state='normal')
        self.callback_field.delete("1.0", tk.END)
        self.callback_field.insert(tk.END, text + "\n")
        self.callback_field.config(state='disabled')

    def search_button_tapped(self):
        text = self.validate_input_field()
        self.callback_field_ins("検索中")
        selected_mode = self.search_mode.get()
        if selected_mode == "search":
            self.launch_gpt(text)
        elif selected_mode == "rpa":
            self.launch_gpt_rpa(text)

    def validate_input_field(self):
        text = self.input_field.get("1.0", tk.END).strip()
        if text == "":
            print("発火")
            self.callback_field_ins("テキストが入力されていません")
            raise ValueError("値が空")
        return text

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()