"""
learning_console_app.py - ChatGPT一問一答アプリ

Description:
    OpenAI API を使って、ステートレスに一問一答するスクリプト。
    ユーザーが入力した質問に対して、ChatGPTが応答を返します。
"""

"""
### 問題出題時
{{
    "type": "question",
    "question_number": 問題番号,
    "question_text": "問題文をここに記載",
    "options": [
        {"number": 1, "text": "選択肢1"},
        {"number": 2, "text": "選択肢2"},
        {"number": 3, "text": "選択肢3"},
        {"number": 4, "text": "選択肢4"},
        {"number": 5, "text": "選択肢5"}
    ],
    "correct_answer": 正解の選択肢番号
}}

### 解答評価時
{{
    "type": "evaluation",
    "result": "正解",
    "explanation": "解説文をここに記載"
}}

### 学習分析時
{{
    "type": "analysis",
    "statics": {{
        "accuracy_rate": "正答率%",
        "total_questions": 総問題数,
        "correnct_answers": 正答数
    }},
    "overall_evaluation": "総合評価文",
    "strength": [
        "良い点1",
        "良い点2"
    ],
    "improvements": [
        "改善点1",
        "改善点2"
    ],
    "adviece": "具体的な学習提案"
}}

## 重要事項
常に学習者の理解促進を重視し、建設的で励ましのトーンで回答してください。
会話の流れを記憶し、学習者の進捗を把握して適切にサポートしてください。
必ずJSON形式で回答し、他のテキストは一切含めないでください。
"""
# ── 標準／サードパーティライブラリのインポート ────────────────
import os              # OpenAIのAPIキーを取得するために使用する
from openai import OpenAI  # OpenAI APIクライアント

# ── プロンプトの設定 ───────────────────────────────────
PROMPT_TEMPLATE = """
# 問題の出題と回答の評価 

## 役割設定
あなたは{SUBJECT}を専攻する大学教授です。学生(ユーザー)が自分の知識や思考を確認し、
理解を促進するために{SUBJECT}に関する問題を出題、それに対する学生(ユーザー)の回答を評価してください。 

## 背景情報
- **ターゲット**：学生(ユーザー)は高校生です 
- **目標**：学生(ユーザー)が自分の実力を確認し、何かできて何が出来ていないのかを明確にできる事。また、それを改善する手助けとなること。
- **出題する問題のジャンル**：{SUBJECT}
- **出題する問題のレベル**：{LEVEL}

## タスク
学生(ユーザー)に対して問題を出題し、それに対する学生(ユーザー)の回答の正誤を判定し、問題についての解説を行う。
出題は、学生(ユーザー)が「next」と送信する限り出題し、「end」と送信した場合、それまでの回答に対する総評を行い、終了する。

## 制約条件
- 出題する問題は高校範囲です
- 出題する問題は１～５番の５択でこたえられるものとします。
- 出題する問題は100文字以下に収まるようにしてください。
- 学生(私)は選択肢番号の中から番号で回答します。 
- 選択肢の中には必ず１つだけ正答を含みます。 
- もし出題ミスや選択肢の中に解答がないなどの出題不備があった場合、その問題は総問題数や評価には含めません。

## プロセス
以下の処理を順に行ってください
１．{SUBJECT}に関する{LEVEL}に応じた問題と、正答を含む回答の５つの選択肢を考える
２．考えた問題に対する解答が考えた選択肢の中に含まれているかをチェックする。もしなかった場合１に戻る。
３．考えた問題と選択肢を学生(ユーザー)に出題する
４．学生(ユーザー)からの回答番号を受け取る
５．学生(ユーザー)の回答と問題の解答が一致しているかを判定し、問題の解説を提示する。
このとき、解説を進めていくうちに出題ミスがあったことが判明した場合、その問題は総問題数や評価には含めない。
６．学生(ユーザー)からの指示("next", "end")を受け取る。 
- 「next」を受け取った場合、１に戻る
- 「end」を受け取った場合、それまでの回答に対して
 - **正答率**
 - **総問題数**
 - **正解数**
 - **総合評価文**
 - **良い点を2つ**
 - **改善点を2つ**
 - **学習アドバイス**
 を表示し、一連のプロセスを終了する。 

## 出力形式
必ず、以下の形式に則って出力してください。
チャット上でテキストとして出題、判定、解説を行ってください。
数式を出力する場合は、Markdown形式で記述してください。
### 問題出題時
{{
    "type": "question",
    "question_number": 問題番号,
    "question_text": "問題文をここに記載",
    "options": [
        "選択肢1",
        "選択肢2",
        "選択肢3",
        "選択肢4",
        "選択肢5"
    ],
    "correct_answer": 正解の選択肢番号
}}

### 解答評価時
{{
    "type": "evaluation",
    "result": "正解",
    "explanation": "解説文をここに記載"
}}

### 学習分析時
{{
    "type": "analysis",
    "statics": {{
        "accuracy_rate": "正答率%",
        "total_questions": 総問題数,
        "correnct_answers": 正答数
    }},
    "overall_evaluation": "総合評価文",
    "strength": [
        "良い点1",
        "良い点2"
    ],
    "improvements": [
        "改善点1",
        "改善点2"
    ],
    "adviece": "具体的な学習提案"
}}

## 重要事項
常に学習者の理解促進を重視し、建設的で励ましのトーンで回答してください。
会話の流れを記憶し、学習者の進捗を把握して適切にサポートしてください。
必ずJSON形式で回答し、他のテキストは一切含めないでください。

"""

messages = []
SUBJECTS = ["数学", "英語", "理科"]
LEVELS = [
    "初学者に向けた、基本的な知識を問う問題", 
    "一般的な中学生が正答できる問題", 
    "一般的な高校生が正答できる問題", 
    "共通テストや大学入試レベルの問題"
]

def chat_once(message: str) -> str:
    # 環境変数から API キーを取得
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # APIキーを取得してクライアントを初期化
    client = OpenAI(api_key=openai_api_key)

    # ユーザーの入力をmessagesに追加
    messages.append({"role": "user", "content": message})

    # ChatGPT に投げる payload（ペイロード）を作成
    resp = client.chat.completions.create(
        model="o4-mini-2025-04-16",
        messages=messages,
        reasoning_effort="low",
        # temperature, max_tokens は省略可（デフォルト値を使う）
    )

    # choices[0] に応答が入っているので中身を取り出して返す
    bot_reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_reply})
    return bot_reply

def main():
    print("=== START:ChatGPT 一問一答アプリ ===")
    
    # ジャンル選択
    subject_index: int = int(input("出題する問題のジャンルを入力して下さい(数学：0, 英語：1, 理科：2)\n"))

    if not (0 <= subject_index <= 2):
        print("入力が不正です。")
        return

    # 問題の難度を選択
    level_index: int = int(input("出題する問題のレベルを入力して下さい(入門レベル：0, 初級レベル：1, 中級レベル：2, 上級レベル：3)\n"))
    if not (0 <= level_index <= 3):
        print("入力が不正です。")
        return

    SYSTEM_PROMPT = PROMPT_TEMPLATE.format(SUBJECT=SUBJECTS[subject_index], LEVEL=LEVELS[level_index])
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    
    q_count: int = 0
    while True:
        # 出題
        bot_reply = chat_once("next")
        print("chatGPT:\n" + bot_reply)
        q_count += 1

        # 回答
        user_input = input("You: ")
        if not (1 <= int(user_input) <= 5):
            print("不正な入力です。終了します。")
            break

        # 回答の評価
        bot_reply = chat_once(user_input)
        print("chatGPT:\n" + bot_reply)

        # 出題数が20問に達していた場合
        if q_count >= 20:
            print("出題数が20問に達しました。総評表示します。")
            break

        # 次の指示
        print("終了するなら'end'、次の問題を出題するなら'next'と入力してください")
        user_input = input("You: ")
        if user_input in ["end", "next"]:
            if user_input == "end":
                break
            else:
                continue
        else:
            print("不正な入力です。終了します。")
            break

    bot_reply = chat_once("end")
    print("chatGPT:\n" + bot_reply)

    print("=== END:ChatGPT 一問一答アプリ ===")

if __name__ == "__main__":
    main()
