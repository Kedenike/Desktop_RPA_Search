from PIL import Image
import base64
import os

# 画像の最大サイズと解像度を設定
MAX_SIZE = 1 * 1024 * 1024  # 1MB
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

def resize_and_compress_image(input_path, output_path, max_size=MAX_SIZE, max_width=MAX_WIDTH, max_height=MAX_HEIGHT):
    # 画像を開く
    img = Image.open(input_path)
    
    # 画像の解像度を確認し、必要に応じてリサイズ
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    
    # 一時的なファイルに保存してサイズを確認
    temp_path = "temp_image.jpg"
    img.save(temp_path, format='JPEG', quality=85)
    
    # 画像のサイズを確認
    file_size = os.path.getsize(temp_path)
    
    # 画像のサイズが最大サイズを超える場合、画質を調整して再圧縮
    quality = 85
    while file_size > max_size and quality > 10:
        quality -= 5
        img.save(temp_path, format='JPEG', quality=quality)
        file_size = os.path.getsize(temp_path)
    
    # 最終的な画像を保存
    img.save(output_path, format='JPEG', quality=quality)
    os.remove(temp_path)

    # 画像をBase64エンコードする関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')