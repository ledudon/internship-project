// 簡単なJavaScript

// ボタンを押した時の動作
function sayHello(){
    // アラートを表示
    alert("こんにちは！JavaScriptが動いています");

    // メッセージを画面に表示
    const messageDiv = document.getElementById('message');
    messageDiv.innerHTML = "ボタンが押されました！";

    // コンソールにメッセージ出力
    console.log("ボタンがクリックされました");
}

// ページが読み込まれたときの動作
document.addEventListener('DOMContentLoaded', function(){
    console.log("ページが読み込まれました");
})
