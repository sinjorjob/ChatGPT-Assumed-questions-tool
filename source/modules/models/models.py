from __future__ import annotations
import logging
import colorama
from ..presets import *
from ..utils import *
from .prompt import *
import openai

class OpenAIClient():
    def __init__(
        self,
        model_name,
        system_prompt="",
        temperature=1.0,
        top_p=1.0,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0,
        api_key = None
     
    ) -> None:
        self.history = []
        self.all_token_counts = []
        self.model_name = model_name
        self.interrupted = False
        self.system_prompt = system_prompt
        self.api_key = None
        self.temperature = temperature
        self.top_p = top_p
        self.stop = stop
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.http_proxy = None
        self.https_proxy = None

    def _get_response(self, messages, stream):


        openai.api_key = self.api_key
        #if self.http_proxy and self.https_proxy:
        #    openai.proxy = {
        #        "http": self.http_proxy,
        #        "https": self.https_proxy
        #    }
        
        response = openai.ChatCompletion.create(
                        model=self.model_name,
                        temperature = self.temperature,
                        #max_tokens=3024, # 4096
                        stream = stream,
                        top_p = self.top_p,
                        stop = self.stop,
                        presence_penalty = self.presence_penalty,
                        frequency_penalty = self.frequency_penalty,
                        messages = messages)
        return response        


    

    def predict(self, uploadFile, favorable_question, skeptical_question, important_question, chatbot):
        """
        OpenAIのChatCompletion.create()メソッドを使用して、Chatbotの回答を取得します。
        """
        logging.info(
            "入力は：" + colorama.Fore.RED + f"{uploadFile.name}" + colorama.Style.RESET_ALL
        )

    
        #openai.api_key = "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"
        openai.api_key = self.api_key
            
        # ファイルの内容を取得
        contents = extract_pptx_content(uploadFile)
        #print(contents)
        inputs = create_prompt(favorable_question, skeptical_question, important_question,contents)

        messages = [{"role": "user", "content": inputs}]
        response = self._get_response(messages, stream=True)

        answer = ""
        for message in response:
            content = message['choices'][0]['delta'].get('content')
            if content:         
                answer += content
                #chatbot = [(inputs.strip(), answer)]
                chatbot = [("アップロードした資料について想定される質問を提案させていただきます😀", answer)]
                yield chatbot

        print("最終回答のchatbot=", chatbot)


    def set_temperature(self, new_temperature):
        self.temperature = new_temperature

    def set_top_p(self, new_top_p):
        self.top_p = new_top_p

    def set_stop_sequence(self, new_stop_sequence: str):
        new_stop_sequence = new_stop_sequence.split(",")
        self.stop_sequence = new_stop_sequence

    def set_max_tokens(self, new_max_tokens):
        self.max_generation_token = new_max_tokens

    def set_presence_penalty(self, new_presence_penalty):
        self.presence_penalty = new_presence_penalty

    def set_frequency_penalty(self, new_frequency_penalty):
        self.frequency_penalty = new_frequency_penalty

    def set_system_prompt(self, new_system_prompt):
        self.system_prompt = new_system_prompt
        
    def set_proxy(self, new_proxy):
        self.http_proxy = new_proxy.strip()
        self.https_proxy = new_proxy.strip()
        save_proxy(self.http_proxy)
        msg = "Proxyを設定しました。"
        print("Proxyを設定したよ", self.http_proxy)
        return self.http_proxy, msg
        

    
    def set_key(self, new_access_key):
        self.api_key = new_access_key.strip()
        save_key(self.api_key)
        msg = "APIキーが変更されました。" + hide_middle_chars(self.api_key)
        logging.info(msg)
        return self.api_key, msg
    
    def load_config(self):
        self.api_key = load_key()
        self.http_proxy = load_proxy()
        self.https_proxy = load_proxy()
        return self.api_key
        
    def set_model(self, new_model):
        self.model_name = new_model.strip()
        msg = "モデルが変更されました。" + self.model_name
        logging.info(msg)
        return msg


def get_model(
    
    model_name,
    access_key=None,

) -> OpenAIClient:
    msg = "OpenAIモデルを読み込んでいます：" + f" {model_name}"
    model = None
    try:
        print("get_modelがよばれたよ")
        logging.info(f"OpenAIモデルを読み込んでいます：: {model_name}")
        model = OpenAIClient(
            model_name=model_name,
            api_key=access_key,

        )

        logging.info(msg)
    except Exception as e:
        logging.error(e)
        msg = f"{STANDARD_ERROR_MSG}: {e}"
        logging.error(msg)
    return model

