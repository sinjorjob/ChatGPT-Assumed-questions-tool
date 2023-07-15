
import gradio as gr
from modules.presets import *
from gradio import themes
from modules.utils import *
from modules.models.models import get_model

my_api_key = ""
with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

def create_new_model():
    current_model = get_model(model_name = ONLINE_MODELS[DEFAULT_MODEL], access_key = my_api_key)
    print("current_model.temperature=" ,current_model.temperature)
    return current_model


with gr.Blocks(css=customCSS, theme='gradio/soft') as demo:
    user_name = gr.State("")
    user_question = gr.State("")
    user_api_key = gr.State(load_key())
    current_model = gr.State(create_new_model)
    with gr.Row():
        gr.HTML(CHUANHU_TITLE, elem_id="app_title")
        status_display = gr.Markdown(elem_id="status_display")
        
    #画面左側のメインエリアの定義
    with gr.Row().style(equal_height=True):
        
        with gr.Column(scale=5):
            gr.Markdown(APP_DESCRIPTION)

            with gr.Row():
                uploadFile = gr.inputs.File(label="PPTファイルをアップロード")
               
                with gr.Tab(label=("質問のパラメータ設定")):
               
                    favorable_question = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            interactive=True,
                            label="好意的な質問",
                            info="生成される好意的な質問の数を指定(Default=3)"
                        )
                    skeptical_question = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            interactive=True,
                            label="懐疑的な質問",
                            info="生成される懐疑的な質問の数を指定(Default=3)"
                        )
                    important_question = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            interactive=True,
                            label="一般的ではないが、重要な質問",
                            info="生成される一般的ではないが、重要な質問の数を指定(Default=3)"
                        )
            with gr.Row():
                chatbot = gr.Chatbot(elem_id="chuanhu_chatbot").style(height="100%")
          
        with gr.Column():
            with gr.Column(min_width=50, scale=1):
                with gr.Tab(label=("基本設定")):
                    keyTxt = gr.Textbox(
                        show_label=True,
                        placeholder=f"OpenAIのAPI-keyをここに入力してください...",
                        value=load_key(),
                        type="password",
                        visible=True,
                        label="API-Key",
                    )
                    usageTxt = gr.Markdown("残高を表示するには、「実行」ボタンを押してリクエストを一度送信してください。", elem_id="usage_display", elem_classes="insert_block")
                    model_select_dropdown = gr.Dropdown(
                        label=("OpenAIモデルを選択してください。"), choices=ONLINE_MODELS, multiselect=False, value=ONLINE_MODELS[DEFAULT_MODEL], interactive=True
                    )
                 
                    
                with gr.Tab(label=("詳細設定")):
                    gr.Markdown(("# ⚠️ 変更は慎重に ⚠️\n\nもし動作しない場合は、デフォルト設定に戻してください。"))
                    
                    temperature_slider = gr.Slider(
                        minimum=-0,
                        maximum=2.0,
                        value=1.0,
                        step=0.1,
                        interactive=True,
                        label="temperature",
                        info="0に近づく程回答が固定、2に近づくほどランダムになる(Default=1)"
                    )
                    top_p_slider = gr.Slider(
                        minimum=-0,
                        maximum=1.0,
                        value=1.0,
                        step=0.05,
                        interactive=True,
                        label="top-p",
                        info="1に近づくほど多彩な単語が出力される(Default=1)"
                    )
                    stop_sequence_txt = gr.Textbox(
                        show_label=True,
                        placeholder=("ここにストップ文字を英語のカンマで区切って入力してください..."),
                        label="stop",
                        value="",
                        lines=1,
                        info="指定した文字にマッチした場合に回答の出力をストップする",
                    )

                    presence_penalty_slider = gr.Slider(
                        minimum=-2.0,
                        maximum=2.0,
                        value=0.0,
                        step=0.01,
                        interactive=True,
                        label="presence penalty",
                        info="値が大きいほど新しいネタを提案してくれる可能性が上がる(Default=0)"
                    )
                    frequency_penalty_slider = gr.Slider(
                        minimum=-2.0,
                        maximum=2.0,
                        value=0.0,
                        step=0.01,
                        interactive=True,
                        label="frequency penalty",
                        info="値が大きいほど同じ単語が出現する確率が低下する(Default=0)"
                    )


    # ChatGPT-APIをCall
    chatgpt_predict_args = dict(
        fn=predict,
        inputs=[
            current_model,  #OpenAIのモデルインスタンス
            uploadFile, # アップロードしたファイル
            favorable_question,  # 好意的な質問の数
            skeptical_question,  # 懐疑的な質問の数
            important_question,  # 重要な質問の数
            chatbot,  #初期は空
        ],
        outputs=[chatbot],  # 戻り値の形式 →   [('<質問文>','<回答文>')]
        show_progress=True,
    )   

    #ファイルアップロード検出時にpredictメソッドを実行
    uploadFile.upload(**chatgpt_predict_args)
    
    
    
    def create_greeting(request: gr.Request):
        current_model = get_model(model_name = ONLINE_MODELS[DEFAULT_MODEL], access_key = my_api_key)
        current_model.load_config() #API_KEYのロード
        print("現在のAPIキー＝", current_model.api_key)
       
        return current_model

    demo.load(create_greeting, inputs=None, outputs=[ current_model], api_name="load")
    

    #詳細設定のパラメータ変更を反映
    temperature_slider.change(set_temperature, [current_model, temperature_slider], None)
    top_p_slider.change(set_top_p, [current_model, top_p_slider], None)
    stop_sequence_txt.change(set_stop_sequence, [current_model, stop_sequence_txt], None)
    presence_penalty_slider.change(set_presence_penalty, [current_model, presence_penalty_slider], None)
    frequency_penalty_slider.change(set_frequency_penalty, [current_model, frequency_penalty_slider], None)

    # API_Keyの更新
    keyTxt.change(set_key, [current_model, keyTxt], [user_api_key, status_display], api_name="set_key")

    # モデルの選択
    model_select_dropdown.change(set_model, [current_model,model_select_dropdown], [status_display] ,api_name="get_model")
if __name__ == "__main__":
    demo.queue(concurrency_count=CONCURRENT_COUNT).launch(
        server_port=7777,
    )


