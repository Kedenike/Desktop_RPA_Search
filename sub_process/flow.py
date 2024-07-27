import check as check
import gpt as gpt
import gemini as gemini
import run as run

async def flow(userInput):
    # userInput = "電卓を開いて、9876×12を実行するコードを書いて"

    # スニペット取得
    snipetText = await gpt.search_gpt_for_rpa(userInput)
    # snipetText = await gemini.search_gemini(userInput)
    snipets = check.extract_code_snippets(snipetText)

    count = 0
    flatText = ""
    if len(snipets) != 1:
        for snipet in snipets:
            flatText = str(count) + "```python" + snipet + "'''\n"
            count += 1

    checkResponse = ""
    index = 0
    noCount = 0
    if count > 0:
        for _ in range(5):
            checkResponse = await gpt.check_gpt_array(userInput, flatText)
            # checkResponse = await gemini.check_gemini_array(userInput, flatText)
            # noの回数が多かったら実行しない
            if checkResponse == "No":
                noCount += 1
                if noCount > 2:
                    index = ""
                    break

            if checkResponse.isdecimal():
                index = int(checkResponse)
                break
    # else:
    #     checkResponse = await gpt.check_gpt(userInput, flatText)
    #     # noの回数が多かったら実行しない
    #     if checkResponse == "No":
    #         return

    if type(index) is int:
        result = snipets[index]
        print("=============================")
        print(result)
        print("=============================")
        run.codeRun(result)
        return result

# asyncio.run(flow())