#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import base64
import csv
import io
import json
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional

import cv2 as cv
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from model.yolox.yolox_onnx import YoloxONNX
from utils import CvDrawText


class WebNinjutsuDetector:
    """Web版忍術検出器"""
    
    def __init__(self):
        # モデル設定
        self.model_path = 'model/yolox/yolox_nano.onnx'
        self.input_shape = (416, 416)
        self.score_th = 0.7
        self.nms_th = 0.45
        self.nms_score_th = 0.1
        
        # 印関連設定
        self.sign_interval = 2.0  # 印履歴クリア間隔（秒）
        self.jutsu_display_time = 5  # 術名表示時間（秒）
        self.chattering_check = 1  # チャタリング対策
        self.sign_max_display = 18
        self.sign_max_history = 44
        
        # モデル初期化
        self.yolox = YoloxONNX(
            model_path=self.model_path,
            input_shape=self.input_shape,
            class_score_th=self.score_th,
            nms_th=self.nms_th,
            nms_score_th=self.nms_score_th,
            providers=['CPUExecutionProvider'],  # Web版ではCPUを使用
        )
        
        # データ読み込み
        self.labels = self._load_labels()
        self.jutsu = self._load_jutsu()
        
        # フォントパス
        self.font_path = './utils/font/衡山毛筆フォント.ttf'
        
        # 印の履歴管理
        self.sign_display_queue = deque(maxlen=self.sign_max_display)
        self.sign_history_queue = deque(maxlen=self.sign_max_history)
        self.chattering_check_queue = deque(maxlen=self.chattering_check)
        
        # タイムスタンプ管理
        self.sign_interval_start = 0
        self.jutsu_index = 0
        self.jutsu_start_time = 0
        
        # チャタリング対策の初期化
        for _ in range(self.chattering_check):
            self.chattering_check_queue.append(-1)
    
    def _load_labels(self) -> List[List[str]]:
        """ラベルファイルを読み込み"""
        with open('setting/labels.csv', encoding='utf8') as f:
            labels = list(csv.reader(f))
        return labels
    
    def _load_jutsu(self) -> List[List[str]]:
        """忍術ファイルを読み込み"""
        with open('setting/jutsu.csv', encoding='utf8') as f:
            jutsu = list(csv.reader(f))
        return jutsu
    
    def process_image(self, image_data: str) -> Dict:
        """画像を処理して結果を返す"""
        try:
            # Base64画像をデコード
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            frame = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
            
            # 推論実行
            bboxes, scores, class_ids = self.yolox.inference(frame)
            
            # 検出結果の処理
            detection_results = []
            for bbox, score, class_id in zip(bboxes, scores, class_ids):
                class_id = int(class_id) + 1
                
                if score < self.score_th:
                    continue
                
                # チャタリング対策
                self.chattering_check_queue.append(class_id)
                if len(set(self.chattering_check_queue)) != 1:
                    continue
                
                # 新しい印の場合のみ履歴に追加
                if (len(self.sign_display_queue) == 0 or 
                    self.sign_display_queue[-1] != class_id):
                    self.sign_display_queue.append(class_id)
                    self.sign_history_queue.append(class_id)
                    self.sign_interval_start = time.time()
                
                detection_results.append({
                    'bbox': bbox.tolist(),
                    'score': float(score),
                    'class_id': int(class_id),
                    'label_en': self.labels[class_id][0],
                    'label_jp': self.labels[class_id][1]
                })
            
            # 履歴クリア判定
            if (time.time() - self.sign_interval_start) > self.sign_interval:
                self.sign_display_queue.clear()
                self.sign_history_queue.clear()
            
            # 術成立判定
            self._check_jutsu()
            
            # 現在の印履歴
            sign_history = ''.join([self.labels[sign_id][1] 
                                  for sign_id in self.sign_display_queue])
            
            # 術名取得
            jutsu_info = self._get_current_jutsu()
            
            return {
                'detections': detection_results,
                'sign_history': sign_history,
                'jutsu_info': jutsu_info,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _check_jutsu(self):
        """術成立判定"""
        if len(self.sign_history_queue) > 0:
            sign_history = ''.join([self.labels[sign_id][1] 
                                  for sign_id in self.sign_history_queue])
            
            for index, signs in enumerate(self.jutsu):
                if sign_history == ''.join(signs[4:]):
                    self.jutsu_index = index
                    self.jutsu_start_time = time.time()
                    break
    
    def _get_current_jutsu(self) -> Optional[Dict]:
        """現在の術情報を取得"""
        if (time.time() - self.jutsu_start_time) < self.jutsu_display_time:
            jutsu_data = self.jutsu[self.jutsu_index]
            
            if jutsu_data[0] == '':  # 属性がない場合
                jutsu_name_jp = jutsu_data[2]
                jutsu_name_en = jutsu_data[3]
            else:  # 属性がある場合
                jutsu_name_jp = f"{jutsu_data[0]}・{jutsu_data[2]}"
                jutsu_name_en = f"{jutsu_data[1]}: {jutsu_data[3]}"
            
            return {
                'name_jp': jutsu_name_jp,
                'name_en': jutsu_name_en,
                'category_jp': jutsu_data[0],
                'category_en': jutsu_data[1],
                'remaining_time': self.jutsu_display_time - (time.time() - self.jutsu_start_time)
            }
        
        return None
    
    def clear_history(self):
        """印履歴をクリア"""
        self.sign_display_queue.clear()
        self.sign_history_queue.clear()


# FastAPIアプリケーション
app = FastAPI(title="NARUTO Hand Sign Detection Web App")

# 静的ファイルの配信（ディレクトリが存在する場合のみ）
if Path("static").exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")

# グローバル検出器インスタンス
detector = WebNinjutsuDetector()


@app.get("/", response_class=HTMLResponse)
async def index():
    """メインページ"""
    html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NARUTO Hand Sign Detection - Web版</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        h1 {
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 30px;
        }
        .video-container {
            position: relative;
            display: inline-block;
            margin-bottom: 20px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        #video {
            display: block;
            width: 640px;
            height: 480px;
        }
        .controls {
            margin: 20px 0;
        }
        button {
            padding: 12px 24px;
            margin: 0 10px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }
        button:hover {
            background: #ff5252;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        .info-panel {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        .info-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .jutsu-display {
            font-size: 24px;
            font-weight: bold;
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .sign-history {
            font-size: 20px;
            font-family: monospace;
            letter-spacing: 5px;
            min-height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .status {
            margin: 10px 0;
            font-size: 14px;
        }
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        @media (max-width: 768px) {
            #video {
                width: 100%;
                height: auto;
            }
            .info-panel {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🥷 NARUTO Hand Sign Detection - Web版 🥷</h1>
        
        <div class="video-container">
            <video id="video" autoplay muted></video>
        </div>
        
        <div class="controls">
            <button id="startBtn" onclick="startCamera()">カメラ開始</button>
            <button id="stopBtn" onclick="stopCamera()" disabled>カメラ停止</button>
            <button onclick="clearHistory()">履歴クリア</button>
        </div>
        
        <div class="status" id="status">カメラを開始してください</div>
        
        <div class="info-panel">
            <div class="info-box">
                <h3>🔥 現在の術</h3>
                <div class="jutsu-display" id="jutsuDisplay">術を検出中...</div>
            </div>
            <div class="info-box">
                <h3>📜 印の履歴</h3>
                <div class="sign-history" id="signHistory">-</div>
            </div>
        </div>
        
        <div id="error" class="error" style="display: none;"></div>
    </div>

    <script>
        let video = document.getElementById('video');
        let canvas = document.createElement('canvas');
        let ctx = canvas.getContext('2d');
        let ws = null;
        let isProcessing = false;
        
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { width: 640, height: 480 }
                });
                video.srcObject = stream;
                
                // WebSocket接続
                connectWebSocket();
                
                document.getElementById('startBtn').disabled = true;
                document.getElementById('stopBtn').disabled = false;
                document.getElementById('status').textContent = 'カメラが開始されました';
                hideError();
                
                // フレーム処理開始
                startFrameProcessing();
                
            } catch (err) {
                showError('カメラにアクセスできませんでした: ' + err.message);
            }
        }
        
        function stopCamera() {
            if (video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
            }
            
            if (ws) {
                ws.close();
            }
            
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            document.getElementById('status').textContent = 'カメラが停止されました';
        }
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onopen = function() {
                console.log('WebSocket接続が確立されました');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDisplay(data);
            };
            
            ws.onclose = function() {
                console.log('WebSocket接続が閉じられました');
            };
            
            ws.onerror = function(error) {
                showError('WebSocket エラー: ' + error);
            };
        }
        
        function startFrameProcessing() {
            function processFrame() {
                if (video.videoWidth > 0 && video.videoHeight > 0 && !isProcessing) {
                    isProcessing = true;
                    
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    ctx.drawImage(video, 0, 0);
                    
                    const imageData = canvas.toDataURL('image/jpeg', 0.8);
                    
                    if (ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({
                            type: 'image',
                            data: imageData
                        }));
                    }
                    
                    setTimeout(() => {
                        isProcessing = false;
                    }, 100); // 100ms間隔で処理
                }
                
                if (!document.getElementById('stopBtn').disabled) {
                    requestAnimationFrame(processFrame);
                }
            }
            
            processFrame();
        }
        
        function updateDisplay(data) {
            if (data.error) {
                showError(data.error);
                return;
            }
            
            // 印履歴の更新
            document.getElementById('signHistory').textContent = data.sign_history || '-';
            
            // 術名の更新
            const jutsuDisplay = document.getElementById('jutsuDisplay');
            if (data.jutsu_info) {
                jutsuDisplay.innerHTML = `
                    <div>${data.jutsu_info.name_jp}</div>
                    <div style="font-size: 16px; margin-top: 5px;">${data.jutsu_info.name_en}</div>
                `;
            } else {
                jutsuDisplay.textContent = '術を検出中...';
            }
            
            // ステータス更新
            const detectionCount = data.detections ? data.detections.length : 0;
            document.getElementById('status').textContent = `検出中... (${detectionCount}個の印を検出)`;
        }
        
        function clearHistory() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'clear_history'
                }));
            }
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function hideError() {
            document.getElementById('error').style.display = 'none';
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket通信エンドポイント"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message['type'] == 'image':
                # 画像処理
                result = detector.process_image(message['data'])
                await websocket.send_text(json.dumps(result))
                
            elif message['type'] == 'clear_history':
                # 履歴クリア
                detector.clear_history()
                await websocket.send_text(json.dumps({'status': 'history_cleared'}))
                
    except WebSocketDisconnect:
        print("WebSocket接続が切断されました")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
