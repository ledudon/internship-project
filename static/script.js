// チャット画面でAJAX送信＆表示
// 'next'/'end'ボタンも同様に送信

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('overlay');
  const form = document.getElementById('chatForm');
  const chatArea = document.getElementById('chatArea');
  const nextBtn = document.getElementById('nextBtn');
  const endBtn = document.getElementById('endBtn');
  const optBtns= document.querySelectorAll(".option");
  const titleText = document.getElementById('question_text');
  let question_count = 0;

  function sendMessage(text) {
    // 操作を禁止
    overlay.style.display = "flex";

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
            // 読み込み中の表示
            titleText.innerHTML = "読み込み中...";
            
            // 解説欄をクリア
            chatArea.innerHTML = "";

            // 各選択肢の初期化
            optBtns.forEach(btn => {
              btn.textContent = "";
              btn.disabled = false;
              btn.classList.remove("selected", "not-selected");
            });

            // 変数の格納
            question_number = reply_data.question_number;
            question_text = reply_data.question_text;
            options = reply_data.options;

            // 問題文と選択肢を表示
            titleText.innerHTML = `第${question_number}問: ${question_text}`;
            optBtns.forEach((btn, i) => {
              btn.textContent = `選択肢${i + 1}: ${options[i]}`;
            });
        }
        else if(message_type == "evaluation"){ // 正誤判定、解説
            result = reply_data.result;
            explanation = reply_data.explanation;

            // 解説を表示
            const div = document.createElement('div');
            div.innerHTML += `<p class="bot"><strong>結果：${result}</strong></p>`;
            div.innerHTML += `<p class="bot"><strong>解説：</strong> ${explanation}</p>`;
            chatArea.appendChild(div);
        }
        else if(message_type == "analysis"){ // 総評
            // 解説欄をクリア
            chatArea.innerHTML = "";
            titleText.innerHTML = "総評";
            nextBtn.disabled = true;
            endBtn.disabled = true;

            // 選択肢を消去
            const optBtnDiv = document.getElementById('options');
            optBtnDiv.innerHTML = ""; 

            // 各変数の格納
            accuracy_rate = reply_data.statics.accuracy_rate; 
            total_questions = reply_data.statics.total_questions;
            correct_answers = reply_data.statics.correct_answers;
            overall_evaluation = reply_data.overall_evaluation;
            strengts = reply_data.strengths;
            improvements = reply_data.improvements;
            advice = reply_data.advice;

            const div = document.createElement('div');
            div.innerHTML += `<p class="bot"><strong>**分析結果**</strong></p>`;
            div.innerHTML += `<p class="bot"> 正答率：${accuracy_rate}</p>`;
            div.innerHTML += `<p class="bot"> 総問題数：${total_questions}</p>`;
            div.innerHTML += `<p class="bot"> 正解数：${correct_answers}</p>`;
            div.innerHTML += `<p class="bot"> 総評：${overall_evaluation}</p>`;
            div.innerHTML += `<p class="bot"> 良い点：</p>`;
            chatArea.appendChild(div);

            // ホームへ戻るボタンを作成
            const btn = document.createElement('button');
            btn.textContent = "ホームに戻る";
            btn.addEventListener('click', () => {
                location.href = "/";
            });
            goHome.appendChild(btn);
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

      // 操作を許可
      overlay.style.display = "none";
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

  // クリック時の処理
  optBtns.forEach((btn, i) => {
    btn.addEventListener('click', () => {
      // 全ボタンを無効化し、選択されたボタンを強調表示 
      document.querySelectorAll(".option").forEach(b => {
        b.disabled = true
        b.classList.add("not-selected");
      });
      btn.classList.remove("not-selected");
      btn.classList.add("selected");
      // 回答を送信
      sendMessage(String(i + 1));
    });
  });

  window.onload = () => {
    // 最初に問題表示
    sendMessage('next');
    // 画面操作を禁止
    overlay.style.display = "flex";
  }
});