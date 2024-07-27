# import google.generativeai as genai

# GOOGLE_API_KEY=''
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-pro-latest')

# async def search_gemini(user_input):
#     response = model.generate_content("pythonのpyautoguiを使って" + user_input + "をpythonのコードスニペットを提出してください" + "君ならできる！！")
#     print(response.text)
#     return response.text

# async def check_gemini(userInput, flatText):
#     response = model.generate_content("こちらのコード" + userInput + "は" + flatText + "という要件を満たしているかを答えてください" + "ただしあなたは yes または No でしか回答してはいけません。君ならできる！！")
#     print(response.text)
#     return response.text

# async def check_gemini_array(userInput, flatText):
#     response = model.generate_content("こちらのコード" + userInput + "は" + flatText + "という要件を満たしているかを数字で答えてください" + "ただしあなたは yes または No でしか回答してはいけません。君ならできる！！")
#     print(response.text)
#     return response.text