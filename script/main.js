// PWA サービスワーカー
// if ('serviceWorker' in navigator) {
//   window.addEventListener('load', function() {
//       navigator.serviceWorker.register('/service-worker.js')
//           .then(function(registration) {
//               console.log('Service Worker registered with scope:', registration.scope);
//           })
//           .catch(function(error) {
//               console.log('Service Worker registration failed:', error);
//           });
//   });
// }

//画像ホバー
document.addEventListener("DOMContentLoaded", function() {
  const image = document.getElementById("hover-image");

  image.addEventListener("mouseenter", function() {
      image.classList.add("hover-effect"); // マウスが乗ったときのクラスを追加
  });

  image.addEventListener("mouseleave", function() {
      image.classList.remove("hover-effect"); // マウスが離れたときのクラスを削除
  });
});

//フッター コピーライト 年自動更新
document.addEventListener("DOMContentLoaded", function() {
    // 現在の年を取得
    const currentYear = new Date().getFullYear();
    // idでHTMLのタグを取得
    const copyrightElement = document.getElementById("year");
  
    if (copyrightElement) {
      // 指定したidの場所に現在の年を書き込み
      copyrightElement.textContent = currentYear;
    }
  });