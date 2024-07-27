def extract_code_snippets(text, start_tag='```python', end_tag='```'):
    """
    指定したファイルからコードスニペットを抽出する。

    :param text: スニペットを抽出する文字列
    :param start_tag: スニペットの開始を示すタグ
    :param end_tag: スニペットの終了を示すタグ
    :return: 抽出されたコードスニペットのリスト
    """
    snippets = []  # 抽出されたスニペットを格納するリスト
    snippet = ""
    formatedText = text
    checkText = "" # 値が更新されない場合に抜ける用のText
    count = 0

    while formatedText.find(start_tag) >= 0:
        idx = formatedText.find(start_tag)
        snippet = formatedText[idx + len(start_tag) + 1:] # len(start_tag)
        
        idx = snippet.find(end_tag)
        snippet = snippet[:idx]
        
        # TODO: snippetの時のindexで切っているため、変な箇所で切られてしまっているので修正する
        formatedText = formatedText[idx + len(end_tag):]

        if formatedText == checkText:
            count += 1
        if count >= 2:
            break
        checkText = formatedText
        snippets.append(snippet)
 
    return snippets