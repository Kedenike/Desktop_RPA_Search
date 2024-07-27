import openai
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import resize_image
import json

with open('config/config.json', 'r') as file:
    config = json.load(file)

openai.api_key = config['APIKEY']
model="gpt-4o"

async def search_gpt(user_input):
    response = openai.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": "あなたは優れたアドバイザーです。悩みを聞いてあげて何を解決するべきかを適切にこたえてください。ただし日本語で回答してください"},
            {"role": "user", "content": user_input}
        ]
    )

    message = response.choices[0].message
    print(message.content)
    return message.content

async def search_gpt_for_rpa(user_input):
    response = openai.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": "あなたは優れたpythonのプログラマーです。あなたは要求されたソースコードの作成をなるべく一つにまとめて回答する必要があります。"},
            {"role": "user", "content": "pythonのpyautoguiを使って" + user_input + "をpythonのコードスニペットを提出してください" + "君ならできる！！"}
        ]
    )

    message = response.choices[0].message
    print(message.content)
    return message.content

async def search_gpt_image(text="この画像は何ですか？"):
    input_path = "image/screenshot.jpeg"
    output_path = "image/compressed_screenshot.jpeg"
    resize_image.resize_and_compress_image(input_path, output_path)
    base64_image = resize_image.encode_image(output_path)

    # Base64エンコード画像を使用したリクエスト
    response = openai.chat.completions.create(
        model = model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=300
    )

    message = response.choices[0].message
    print(message.content)
    return message.content

async def check_gpt(userInput, flatText):
    response = openai.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": "あなたは優れたpythonのプログラマーです。ただしあなたは yes または No でしか回答してはいけません"},
            {"role": "user", "content": "こちらのコード" + userInput + "は" + flatText + "という要件を満たしているかを答えてください"}
        ]
    )

    message = response.choices[0].message
    print(message.content)
    return message.content

async def check_gpt_array(userInput, flatText):
    response = openai.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": "あなたは優れたpythonのプログラマーです。ただしあなたは 複数あるコードに充てられた 数字一文字 または No でしか回答してはいけません"},
            {"role": "user", "content": "こちらのコード" + userInput + "は" + flatText + "という要件を満たしているかを数字で答えてください"}
        ]
        # ,
        # functions=[
        #     {
        #         "name": "test_search_gpt_for_rpa",
        #         "description": "subprocess用のコードを作成する",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "data": {
        #                     "test": [
        #                         "explorer", "path"
        #                     ]
        #                 }
        #             },
        #         },
        #     },
        # ],
        # function_call="auto",
    )

    message = response.choices[0].message
    print(message.content)
    return message.content
