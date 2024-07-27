import os

def delete_screenshot():
    try:
        os.remove("image/screenshot.jpeg")
        print("screenshot.jpegを削除しました")
    except FileNotFoundError:
        print("screenshot.jpegが見つかりませんでした")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
