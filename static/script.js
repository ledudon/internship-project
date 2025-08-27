// チャット画面でAJAX送信＆表示
// 'next'/'end'ボタンも同様に送信

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('chatForm');
  const chatArea = document.getElementById('chatArea');
  const nextBtn = document.getElementById('nextBtn');
  const endBtn = document.getElementById('endBtn');

  function sendMessage(text) {
    // 入力表示
    text = marked.parse(text);
    chatArea.innerHTML += `<p class="user"><strong>あなた:</strong> ${text}</p>`;
    chatArea.scrollTop = chatArea.scrollHeight;
    // サーバー送信
    const res = fetch('/api/message', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
      })
      .then(response => response.json())
      .then(data => {
        // 応答表示
        reply_data = JSON.parse(data.reply);
        message_type = reply_data.type;
        if(message_type == "question"){ // 出題
            questoin_number = reply_data.questoin_number;
            question_text = reply_data.question_text;
            options = reply_data.options;
            // 問題文と選択肢を表示
            chatArea.innerHTML += `<p class="bot"><strong>AI:第</strong> ${question_number} <strong>問</strong></p>`;
            chatArea.innerHTML += `<p class="bot"> ${question_text}</p>`;
            options.forEach((option, index) => {
              chatArea.innerHTML += `<p class="bot"><strong>選択肢${index + 1}:</strong> ${option}</p>`;
            });
        }
        else if(message_type == "evaluation"){ // 正誤判定、解説
            result = reply_data.result;
            explanation = reply_data.explanation;
            chatArea.innerHTML += `<p class="bot"><strong>AI:</strong> ${result}</p>`;
            chatArea.innerHTML += `<p class="bot"><strong>解説:</strong> ${explanation}</p>`;
        }
        else if(message_type == "analysis"){ // 総評
            accuracy_rate = reply_data.statics.accuracy_rate;
            total_questions = reply_data.statics.total_questions;
            correct_answers = reply_data.statics.correct_answers;
            overall_evaluation = reply_data.overall_evaluation;
            strengts = reply_data.strengths;
            improvements = reply_data.improvements;
            advice = reply_data.advice;
            
            chatArea.innerHTML += `<p class="bot"><strong>AI:</strong> **分析結果**</p>`
            chatArea.innerHTML += `<p class="bot"> 正答率：${accuracy_rate}</p>`
            chatArea.innerHTML += `<p class="bot"> 総問題数：${total_questions}</p>`
            chatArea.innerHTML += `<p class="bot"> 正解数：${correct_answers}</p>`
            chatArea.innerHTML += `<p class="bot"> 総評：${overall_evaluation}</p>`
            chatArea.innerHTML += `<p class="bot"> 良い点：</p>`
        }
        chatArea.scrollTop = chatArea.scrollHeight;

        // KaTeXレンダリング（新しく追加された部分だけ対象にする）
        renderMathInElement(chatArea, {
            delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false}
            ]
        });
      });
  }
  // 送信ボタンの押下イベント
  form.addEventListener('submit', (e) => {
    // デフォルトのフォーム送信を防止
    e.preventDefault();
    // formのmessageのvalueの空白を取り除いた文字列をinputに代入
    const input = form.message.value.trim();
    // 空文字列の場合は何もしない
    if (!input) return;
    // メッセージ送信
    sendMessage(input);
    // 入力フィールドをクリア
    form.message.value = '';
  });
  // nextボタンの押下イベント
  nextBtn.addEventListener('click', () => sendMessage('next'));
  // endボタンの押下イベント
  endBtn.addEventListener('click', () => sendMessage('end'));
});