# Flaskライブラリを読み込みます
from flask import Flask, render_template, request, jsonify  # jsonify: JSONレスポンス用
import learning_console_app as lca

# Flaskアプリケーションを作成します
app = Flask(__name__)

# トップページのルート設定
@app.route('/', methods=['GET'])
def index():
    # index.htmlテンプレートを読み込み、初期メッセージを渡します
    return render_template(
        'index.html',
        subjects=lca.SUBJECTS,
        levels=lca.LEVELS
    )

@app.route('/start', methods=['POST'])
def start():
    subject_index = int(request.form['subject'])
    level_index = int(request.form['level'])

    subject = lca.SUBJECTS[subject_index]
    level = lca.LEVELS[level_index]

    # systemプロンプトを作成し履歴をクリア
    system_prompt = lca.PROMPT_TEMPLATE.format(SUBJECT=subject, LEVEL=level)
    lca.messages.clear()
    lca.messages.append({"role": "system", "content": system_prompt})

    return render_template('chat.html')

@app.route('/api/message', methods=['POST'])
def api_message():
    """
    AJAXでメッセージ送受信を処理
    learning_console_app.chat_once() を呼び出して応答を生成し JSONで返却
    """
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    bot_reply = lca.chat_once(user_msg)
    print(bot_reply)
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    # デバッグモードでローカルサーバーを起動します
    app.run(debug=True)