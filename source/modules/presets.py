import gradio as gr
from pathlib import Path


CHUANHU_TITLE =("&#x1f30e; 質問パーティーメーカー &#x1f30e;")

USAGE_API_URL="https://api.openai.com/dashboard/billing/usage"

KEY_FILE = "config.json"
APP_DESCRIPTION = """
## アップロードしたPPTファイルに対する想定質問と回答例を自動生成するツールです。
"""
small_and_beautiful_theme = gr.themes.Soft(
        primary_hue=gr.themes.Color(
            c50="rgba(2, 193, 96, 0.1)",
            c100="rgba(2, 193, 96, 0.2)",
            c200="#02C160",
            c300="rgba(2, 193, 96, 0.32)",
            c400="rgba(2, 193, 96, 0.32)",
            c500="rgba(2, 193, 96, 1.0)",
            c600="rgba(2, 193, 96, 1.0)",
            c700="rgba(2, 193, 96, 0.32)",
            c800="rgba(2, 193, 96, 0.32)",
            c900="#02C160",
            c950="#02C160",
        ),
        secondary_hue=gr.themes.Color(
            c50="#576b95",
            c100="#576b95",
            c200="#576b95",
            c300="#576b95",
            c400="#576b95",
            c500="#576b95",
            c600="#576b95",
            c700="#576b95",
            c800="#576b95",
            c900="#576b95",
            c950="#576b95",
        ),
        neutral_hue=gr.themes.Color(
            name="gray",
            c50="#f9fafb",
            c100="#f3f4f6",
            c200="#e5e7eb",
            c300="#d1d5db",
            c400="#B2B2B2",
            c500="#808080",
            c600="#636363",
            c700="#515151",
            c800="#393939",
            c900="#272727",
            c950="#171717",
        ),
        radius_size=gr.themes.sizes.radius_sm,
    ).set(
        button_primary_background_fill="#0628ae",
        button_primary_background_fill_dark="#06AE56",
        button_primary_background_fill_hover="#07c8ae",
        button_primary_border_color="#06AE56",
        button_primary_border_color_dark="#06AE56",
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",
        button_secondary_background_fill="#F2F2F2",
        button_secondary_background_fill_dark="#2B2B2B",
        button_secondary_text_color="#393939",
        button_secondary_text_color_dark="#FFFFFF",
        # background_fill_primary="#F7F7F7",
        # background_fill_primary_dark="#1F1F1F",
        block_title_text_color="*primary_500",
        block_title_background_fill="*primary_100",
        input_background_fill="#F6F6F6",
    )

ONLINE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",

]
DEFAULT_MODEL = 0


ENABLE_STREAMING_OPTION = True # 回答をリアルタイムで表示するかどうかを選択する

# ChatGPTの設定
INITIAL_SYSTEM_PROMPT = "You are a helpful assistant."
API_HOST = "api.openai.com"
COMPLETION_URL = "https://api.openai.com/v1/chat/completions"
BALANCE_API_URL="https://api.openai.com/dashboard/billing/credit_grants"
USAGE_API_URL="https://api.openai.com/dashboard/billing/usage"
HISTORY_DIR = Path("history")
HISTORY_DIR = "history"
TEMPLATES_DIR = "templates"

# エラーメッセージ
STANDARD_ERROR_MSG = "☹️一般的なエラーメッセージの先頭に表示される標準的な接頭辞を示す。" 
GENERAL_ERROR_MSG = ("会話を取得する際にエラーが発生しました。バックエンドログを確認してください。")
ERROR_RETRIEVE_MSG = ("ネットワーク接続を確認するか、APIキーが有効かどうかを確認してください。")
CONNECTION_TIMEOUT_MSG = ("接続タイムアウトにより、会話を取得できません。") 
READ_TIMEOUT_MSG = "読み取りタイムアウトにより、会話を取得できません。"
PROXY_ERROR_MSG = ("プロキシエラーにより、会話を取得できません。") 
SSL_ERROR_PROMPT = "SSLエラーにより、会話を取得できません。"
NO_APIKEY_MSG = ("APIキーが空です。正しいキーが入力されているかどうかを確認してください。")
NO_INPUT_MSG = ("会話内容が入力されていません。") 
BILLING_NOT_APPLICABLE_MSG = "請求書情報は適用されません" # ローカルで実行されたモデルが返す請求書情報

TIMEOUT_STREAMING = 60 # ストリーミング対話時のタイムアウト時間
TIMEOUT_ALL = 200 # ストリーミング以外の対話時のタイムアウト時間
ENABLE_STREAMING_OPTION = True # 回答をリアルタイムで表示するかどうかを選択するチェックボックスを有効にするかどうか
HIDE_MY_KEY = False # APIキーをUIで非表示にしたい場合は、この値をTrueに設定してください
CONCURRENT_COUNT = 100 # 同時に使用できるユーザー数の上限


MODEL_TOKEN_LIMIT = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0314": 32768
}
DEFAULT_TOKEN_LIMIT = 3000 # デフォルトのトークン上限
TOKEN_OFFSET = 1000  #：モデルのトークン上限からこの値を引いて、ソフト上限を得ます。ソフト上限に達すると、トークン使用量を自動的に減らそうとします。
DEFAULT_TOKEN_LIMIT = 3000 #：デフォルトのトークン上限
REDUCE_TOKEN_FACTOR = 0.5# ：モデルのトークン上限に乗じて、目標トークン数を得ます。トークン使用量を減らす場合は、トークン使用量を目標トークン数以下に減らします。


ALREADY_CONVERTED_MARK = "<!-- ALREADY CONVERTED BY PARSER. -->"

