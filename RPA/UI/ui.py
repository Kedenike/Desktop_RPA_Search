import tkinter as tk
import subprocess
from PIL import Image, ImageTk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sub_process import gpt, sc_delete
import asyncio
import threading
import flow

# スクリーンショットが保存された後に画像を更新するためにlaunch_wincap関数を修正
def capture_button_tapped():
    # 最初にWindowを最小化
    root.iconify()
    subprocess.Popen(["python", "UI/wincap.py"]).wait()
    update_image()
    # 最小化を解除してWindowを表示
    root.deiconify()

def update_image():
    try:
        img = Image.open("image/screenshot.jpeg")
        img = img.resize((200, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img
        root.geometry("360x330")

    except Exception as e:
        callback_field_ins(f"画像ファイルを認識できませんでした: {e}")

def launch_gpt():
    try:
        async def wrapper(text):
            result = await gpt.search_gpt_image(text=text)
            callback_field_ins(result)
            img_label.config(image='')
            img_label.image = None
            sc_delete.delete_screenshot()
        
        text = input_field.get("1.0", tk.END).strip() # こいつ挙動確認する
        if text == "":
            callback_field_ins("テキストが入力されていません")
            return

        callback_field_ins("呼ばれた")
        input_path = "image/screenshot.jpeg"
        img = Image.open(input_path)
        threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()

    except FileNotFoundError:
        async def wrapper(text):
            result = await gpt.search_gpt(text)
            callback_field_ins(result)
        text = input_field.get("1.0", tk.END).strip()
        threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()
            
def launch_gpt_rpa():
    async def wrapper(text):
        await flow.flow(text)
        callback_field_ins("終わったよ")
    text = input_field.get("1.0", tk.END).strip()
    threading.Thread(target=lambda: asyncio.run(wrapper(text))).start()


def callback_field_ins(text):
    callback_field.config(state='normal')
    callback_field.delete("1.0", tk.END)
    callback_field.insert(tk.END, text + "\n")
    callback_field.config(state='disabled')

def search_button_tapped():
    callback_field_ins("検索中")
    selected_mode = search_mode.get()
    if selected_mode == "search":
        launch_gpt()
    elif selected_mode == "rpa":
        launch_gpt_rpa()

# ウィンドウサイズを設定
window_width = 360
window_height = 230

root = tk.Tk()
# root.title("CP OCR Launcher")
root.title("")

root.geometry(f"{window_width}x{window_height}")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = screen_width - window_width - 5
y = screen_height - window_height - 80

root.geometry(f"+{x}+{y}")

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

input_field = tk.Text(second_frame, height=3, width=50)
input_field.pack(pady=5)

callback_field = tk.Text(second_frame, height=9, width=50, state='disabled')
callback_field.pack(pady=0)

img_label = tk.Label(second_frame)
img_label.pack()

button_frame = tk.Frame(second_frame)
button_frame.pack(pady=0)

search_mode = tk.StringVar(value="search")
radio_search = tk.Radiobutton(button_frame, text="サーチ", variable=search_mode, value="search")
radio_search.pack(side=tk.LEFT, padx=10)
radio_rpa = tk.Radiobutton(button_frame, text="RPA", variable=search_mode, value="rpa")
radio_rpa.pack(side=tk.LEFT, padx=10)

capture_button = tk.Button(button_frame, text="画面キャプチャ", command=capture_button_tapped)
capture_button.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(button_frame, text="検索", command=search_button_tapped)
search_button.pack(side=tk.LEFT, padx=10)

root.mainloop()