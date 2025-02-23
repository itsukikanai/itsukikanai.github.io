let stream = null;
let mediaRecorder = null;
let recordedChunks = [];
let isRecording = false;
let recordStartTime = null;
let recordTimerInterval = null;

// DOM要素取得
const videoElement = document.getElementById('preview');
const cameraSwitchBtn = document.getElementById('cameraSwitch');
const lensBtns = document.querySelectorAll('.lens-btn');
const recordBtn = document.getElementById('recordBtn');
const recordTimer = document.getElementById('recordTimer');
const audioToggleBtn = document.getElementById('audioToggle');
const downloadLink = document.getElementById('downloadLink');

// 現在のカメラが前面か背面かを管理（true=front, false=back）
let isFrontCamera = false;
// ズーム選択値（0.5, 1, 2など）
let currentZoomValue = 1;

// カメラ起動用
async function startStream() {
  // 既存のストリームがあれば停止
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }

  // デバイス一覧を取得
  const devices = await navigator.mediaDevices.enumerateDevices();
  const videoDevices = devices.filter(device => device.kind === 'videoinput');

  // レンズ選択
  let selectedDevice = null;

  if (isFrontCamera) {
    // 前面カメラ
    selectedDevice = videoDevices.find(d => d.label.toLowerCase().includes('front'))
      || videoDevices[0]; // 見つからなければ先頭を使用
  } else {
    // 背面カメラ: zoomValueに応じてデバイスを切り替える
    // （実際にはiOS Safariで複数デバイスが得られない場合もあるので注意）
    if (currentZoomValue <= 0.75) {
      // 超広角
      selectedDevice = videoDevices.find(d => d.label.toLowerCase().includes('ultra'));
    } else if (currentZoomValue >= 1.5) {
      // 望遠
      selectedDevice = videoDevices.find(d => d.label.toLowerCase().includes('tele'));
    }
    // 該当が無い場合や中間値の場合は広角を選択
    if (!selectedDevice) {
      selectedDevice = videoDevices.find(d => d.label.toLowerCase().includes('back'))
        || videoDevices[0];
    }
  }

  // デバイスID取得
  const deviceId = selectedDevice ? selectedDevice.deviceId : null;

  const constraints = {
    video: {
      deviceId: deviceId ? { exact: deviceId } : undefined,
      // フレームレートなど必要に応じ設定可能
      width: { ideal: 1920 },
      height: { ideal: 1080 }
    },
    audio: true
  };

  try {
    stream = await navigator.mediaDevices.getUserMedia(constraints);
    videoElement.srcObject = stream;
    // 音声トグル初期表示
    audioToggleBtn.textContent = stream.getAudioTracks()[0].enabled ? '🔈' : '🔇';
  } catch (err) {
    console.error('カメラの取得に失敗した: ', err);
  }
}

// 撮影時間を更新する
function updateRecordTimer() {
  if (!recordStartTime) return;
  const now = new Date().getTime();
  const diff = now - recordStartTime;
  const sec = Math.floor(diff / 1000) % 60;
  const min = Math.floor(diff / 60000) % 60;
  const hr = Math.floor(diff / 3600000);
  const pad = num => num.toString().padStart(2, '0');
  recordTimer.textContent = `${pad(hr)}:${pad(min)}:${pad(sec)}`;
}

// 録画開始
function startRecording() {
  if (!stream) return;
  recordedChunks = [];

  // video/mp4やvideo/webmなど、必要に応じて選択
  const mimeType = 'video/mp4';
  try {
    mediaRecorder = new MediaRecorder(stream, { mimeType });
  } catch (e) {
    console.error('MediaRecorderの初期化に失敗: ', e);
    return;
  }

  mediaRecorder.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) {
      recordedChunks.push(event.data);
    }
  };

  mediaRecorder.onstop = () => {
    const blob = new Blob(recordedChunks, { type: mimeType });
    const url = URL.createObjectURL(blob);

    // 日時入りファイル名
    const now = new Date();
    const pad = num => ('0' + num).slice(-2);
    const formatted = now.getFullYear().toString() +
                      pad(now.getMonth() + 1) +
                      pad(now.getDate()) + '_' +
                      pad(now.getHours()) +
                      pad(now.getMinutes()) +
                      pad(now.getSeconds());

    downloadLink.href = url;
    downloadLink.download = `IMG_${formatted}.mp4`;
    downloadLink.style.display = 'inline-block';
  };

  mediaRecorder.start();
  isRecording = true;
  recordBtn.classList.add('recording');

  // 撮影時間計測開始
  recordStartTime = new Date().getTime();
  recordTimer.textContent = '00:00:00';
  recordTimerInterval = setInterval(updateRecordTimer, 500);
}

// 録画停止
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }
  isRecording = false;
  recordBtn.classList.remove('recording');

  // タイマー停止
  clearInterval(recordTimerInterval);
}

// ----------------- イベント登録 -----------------

// 初期起動
startStream();

// 録画ボタン押下
recordBtn.addEventListener('click', () => {
  if (!isRecording) {
    startRecording();
  } else {
    stopRecording();
  }
});

// カメラ切り替え
cameraSwitchBtn.addEventListener('click', async () => {
  isFrontCamera = !isFrontCamera;
  cameraSwitchBtn.textContent = isFrontCamera ? '背' : '前';
  await startStream();
});

// レンズボタン押下（ズーム値に応じて自動で背面カメラ切替を再取得）
lensBtns.forEach(btn => {
  btn.addEventListener('click', async () => {
    // 全てのボタンのactiveクラスを外す
    lensBtns.forEach(b => b.classList.remove('active'));
    // 押下ボタンにactive付与
    btn.classList.add('active');

    // 前面カメラの場合は背面に切り替えてからズームを反映
    if (isFrontCamera) {
      isFrontCamera = false;
      cameraSwitchBtn.textContent = '前';
    }
    currentZoomValue = parseFloat(btn.dataset.zoom);
    await startStream();
  });
});

// 音声トグル
audioToggleBtn.addEventListener('click', () => {
  if (!stream) return;
  const audioTracks = stream.getAudioTracks();
  audioTracks.forEach(track => {
    track.enabled = !track.enabled;
    audioToggleBtn.textContent = track.enabled ? '🔈' : '🔇';
  });
});