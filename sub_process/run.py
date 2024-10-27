import uuid
import datetime
import os
import time

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

    time.sleep(2)

    # subprocess.run(["python", file_name])
    exec(result)
    print("subprocess")

# 確認用コード
# codeRun("test")

# import uuid
# import datetime
# import os
# import subprocess
# import time
# import sys

# def codeRun(result):
#     t_delta = datetime.timedelta(hours=9)
#     JST = datetime.timezone(t_delta, 'JST')
#     now = datetime.datetime.now(JST)

#     date = now.strftime('%Y-%m-%d-%H-%M-%S')

#     # exeファイルのディレクトリを基準にファイルパスを設定
#     base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
#     file_name = os.path.join(base_dir, "content", f"saved_code_{date}_{uuid.uuid4()}.py")
    
#     # ディレクトリが存在しない場合は作成
#     os.makedirs(os.path.dirname(file_name), exist_ok=True)

#     # ファイルに保存
#     with open(file_name, "w", encoding='utf-8') as file:
#         file.write(result)

#     print("subprocess start")

#     # sys.executableを使用してサブプロセスを実行
#     if getattr(sys, 'frozen', False):
#         print("true")
#         # PyInstallerでコンパイルされた場合
#         subprocess.run([sys.executable, "-c", result])
#     else:
#         print("false")
#         # 通常のPythonスクリプトとして実行される場合
#         subprocess.run([sys.executable, file_name])

#     print("subprocess completed")


# import os
# import subprocess

# def subprocess_args(include_stdout=True):
#     if hasattr(subprocess, 'STARTUPINFO'):
#         si = subprocess.STARTUPINFO()
#         si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#         env = os.environ
#     else:
#         si = None
#         env = None

#     if include_stdout:
#         ret = {'stdout': subprocess.PIPE, 'stdin': subprocess.PIPE, 'stderr': subprocess.PIPE, 'startupinfo': si, 'env': env}
#     else:
#         ret = {'stdin': subprocess.PIPE, 'stderr': subprocess.PIPE, 'startupinfo': si, 'env': env}
#     return ret

# import sys
# import os
# import subprocess
# import datetime
# import uuid
# import time

# def codeRun(result):
#     t_delta = datetime.timedelta(hours=9)
#     JST = datetime.timezone(t_delta, 'JST')
#     now = datetime.datetime.now(JST)

#     date = now.strftime('%Y-%m-%d-%H-%M-%S')

#     file_name = "content/saved_code_" + date + "_" + str(uuid.uuid4()) + ".py"
    
#     # ディレクトリが存在しない場合は作成
#     os.makedirs(os.path.dirname(file_name), exist_ok=True)

#     # ファイルに保存
#     with open(file_name, "w", encoding='utf-8') as file:
#         file.write(result)

#     time.sleep(2)

#     # sys.executableを使用し、subprocess_args関数を適用
#     subprocess.run([sys.executable, file_name], **subprocess_args())
#     print("subprocess")


