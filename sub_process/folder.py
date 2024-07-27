#import pyautogui as p
import subprocess
path = r"G:\code\rpa"
subprocess.Popen(['explorer', path], shell=True)

file_path = r"G:\code\rpa"
with open(file_path) as file:
    content = file.read()
    print(content)
    
import os

# フォルダ内のファイル一覧を取得
folder_path = r"C:\Users\augst\OneDrive\デスクトップ\magicanimate"
files = os.listdir(folder_path)
print(files)

# 新しいフォルダを作成
new_folder_path = os.path.join(folder_path, '新規フォルダ')
os.makedirs(new_folder_path, exist_ok=True)
print(f"新しいフォルダを作成しました: {new_folder_path}")
    
# import subprocess
# import sys

# # OS別の処理
# if sys.platform == 'win32':
#     # Windowsの場合
#     subprocess.run(['explorer', folder_path], check=True)
# elif sys.platform == 'darwin':
#     # macOSの場合
#     subprocess.run(['open', folder_path], check=True)
# else:
#     # Linuxの場合（デスクトップ環境に依存する）
#     subprocess.run(['xdg-open', folder_path], check=True)