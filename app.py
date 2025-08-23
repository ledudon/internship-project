# 簡単なFlaskアプリ
from flask import Flask, jsonify

# Flaskアプリを作る
app = Flask(__name__)

# 日本語文字化け対策
app.json.ensure_ascii = False

# ホームページの設定
@app.route('/')
def home():
    return '''
<h1>こんにちは! </h1>
<p>Flaskが動いています</p>
<p>おめでとうございます! </p>
'''

# APIテスト用（文字化け対策実施済み）
@app.route('/test')
def test():
    return jsonify({
        'message': 'テスト成功',
        'status': 'OK',
        'comment': '日本語も正常に表示されます'
    })

# サーバーを開始
if __name__ == '__main__':
    print("サーバーを開始します")
    print("ブラウザで <http://127.0.0.1:5000> を開いてください")
    app.run(debug=True)


