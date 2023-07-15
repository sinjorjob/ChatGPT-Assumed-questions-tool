from langchain.prompts import PromptTemplate

def create_prompt(favorable_question, skeptical_question, important_question,contents):
    # 入力テンプレートの作成
    multiple_input_prompt = PromptTemplate(
    input_variables=["favorable_question", "skeptical_question", "important_question", "contents"],
    template="""
以下の[内容]についてビジネス向けのプレゼンを行います。
聴衆からどのような質問がきそうか提案してください。
回答内容は「質問の種類（好意的な質問/懐疑的な質問/一般的ではないが、重要な質問）、質問文、回答例」の項目で表形式でまとめてください。

#提案の条件
・好意的な質問を{favorable_question}個提案してください。
・懐疑的な質問を{skeptical_question}個提案してください。
・一般的ではないが、重要な質問を{important_question}個提案してください。

#内容
{contents}

#自動修正機能
出力が表形式でない場合、表形式に修正してから最終的な回答を提示してください。
各項目の値が設定されないケースがあるので、その場合は修正してから最終的な回答だけを表形式で提示してください。
３つの質問の種類（好意的な質問/懐疑的な質問/般的ではないが、重要な質問）の数が一致しない場合表形式が崩れる場合があるので
正しく修正してから最終的な回答を提示してください。
"""
)
    prompt_sentense = multiple_input_prompt.format(favorable_question=favorable_question, 
                                       skeptical_question=skeptical_question,
                                       important_question=important_question,
                                       contents=contents
                                       )
    # プロンプトの作成
    print(prompt_sentense)
    return prompt_sentense

