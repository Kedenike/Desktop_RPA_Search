import tkinter as tk
import json

class SetupWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
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
        
        second_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=second_frame, anchor="nw")
        
        self.label = tk.Label(second_frame, text='sk-から始まるAPIキーを用意してください')
        self.label.pack()

        self.config
        initial_API_key = ""
        try:
            with open('config/config.json', 'r') as file:
                self.config = json.load(file)
                initial_API_key = self.config['APIKEY']
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            
        self.input_field = tk.Text(second_frame, height=3, width=50)
        self.input_field.insert(tk.END, initial_API_key)
        self.input_field.pack(pady=5)

        button_frame = tk.Frame(second_frame)
        button_frame.pack(pady=0)

        search_button = tk.Button(button_frame, text="設定する", command=self.setting_button_tapped)
        search_button.pack(side=tk.LEFT, padx=10)
        
    def setting_button_tapped(self):
        data = {
            "APIKEY": self.input_field.get("1.0", tk.END).strip(),
        }
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        try:
            with open('config/config.json', 'w') as file:
                file.write(json_str)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            
        self.master.deiconify()
        self.destroy()
        
if __name__ == "__main__":
    app = SetupWindow()
    app.mainloop()