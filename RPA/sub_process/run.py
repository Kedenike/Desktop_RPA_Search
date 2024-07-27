import uuid
import datetime
import os

def codeRun(result):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)

    date = now.strftime('%Y-%m-%d-%H-%M-%S')

    file_name = "content/saved_code_" + date + "_" +str(uuid.uuid4()) + ".py"
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    # ファイルに保存
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(result)

    # ファイルを実行
    import subprocess
    subprocess.run(["python", file_name])

# 確認用コード
# codeRun("test")