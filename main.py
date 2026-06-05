import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- V7 COSMIC PRO INTERFACE ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudDev Cosmic v7 Pro</title>
    <style>
        body { 
            margin: 0; 
            font-family: system-ui, -apple-system, sans-serif; 
            background: #08090c; 
            color: #f8fafc; 
            display: flex; 
            flex-direction: column; 
            min-height: 100vh; 
        }
        header { 
            background: #11131c; 
            padding: 14px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid #1e293b; 
            box-shadow: 0 4px 30px rgba(0,0,0,0.4); 
        }
        header h3 { 
            margin: 0; 
            font-size: 16px; 
            font-weight: 800; 
            background: linear-gradient(to right, #38bdf8, #c084fc); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        
        .tab-bar { 
            display: flex; 
            background: #0b0c12; 
            border-bottom: 1px solid #1e293b; 
        }
        .tab-btn { 
            background: none; 
            border: none; 
            color: #64748b; 
            padding: 14px 22px; 
            font-size: 13px; 
            font-weight: 600; 
            cursor: pointer; 
            border-bottom: 2px solid transparent; 
            transition: all 0.2s; 
        }
        .tab-btn.active { 
            color: #f8fafc; 
            border-bottom: 2px solid #38bdf8; 
            background: #11131c; 
        }
        
        .tab-content { 
            display: none; 
            padding: 16px; 
            flex: 1; 
            flex-direction: column; 
            gap: 16px; 
            box-sizing: border-box; 
        }
        .tab-content.active { 
            display: flex; 
        }
        
        .editor-container { 
            background: #0d0f17; 
            border: 1px solid #1e293b; 
            border-radius: 12px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
        }
        .editor-header { 
            background: #161926; 
            padding: 10px 16px; 
            font-size: 12px; 
            color: #64748b; 
            border-bottom: 1px solid #1e293b; 
        }
        
        .editor-body { 
            display: flex; 
            height: 320px; 
            font-family: monospace; 
            font-size: 14px; 
            background: #0d0f17; 
        }
        textarea { 
            flex: 1; 
            background: transparent; 
            color: #e2e8f0; 
            border: none; 
            padding: 16px; 
            box-sizing: border-box; 
            resize: none; 
            outline: none; 
            height: 100%; 
            overflow-y: auto; 
            font-family: monospace; 
        }
        
        .card { 
            background: #11131c; 
            border: 1px solid #1e293b; 
            border-radius: 12px; 
            padding: 18px; 
            display: flex; 
            flex-direction: column; 
            gap: 14px; 
        }
        .card h4 { 
            margin: 0; 
            font-size: 14px; 
            font-weight: 700; 
        }
        
        input { 
            background: #181b28; 
            color: #f8fafc; 
            border: 1px solid #1e293b; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 13px; 
            outline: none; 
        }
        
        button { 
            background: #38bdf8; 
            color: #090d16; 
            border: none; 
            padding: 12px 20px; 
            font-size: 13px; 
            font-weight: 700; 
            border-radius: 8px; 
            cursor: pointer; 
            display: inline-flex; 
            align-items: center; 
            justify-content: center; 
            gap: 8px; 
        }
        .btn-success { background: #4ade80; color: #052e16; }
        .btn-ai { background: #c084fc; color: #2e1065; }
        
        .preview-wrapper { 
            border-radius: 10px; 
            overflow: hidden; 
            border: 1px solid #1e293b; 
            background: #fff; 
        }
        iframe { 
            width: 100%; 
            height: 300px; 
            border: none; 
            background: white; 
        }
        
        .ai-box { 
            background: #05060a; 
            border-left: 4px solid #c084fc; 
            padding: 14px; 
            border-radius: 8px; 
            font-size: 13px; 
            color: #cbd5e1; 
            white-space: pre-wrap; 
        }
        .template-grid { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 12px; 
        }
    </style>
</head>
<body>

<header>
    <h3>✨ CloudDev Cosmic v7 Pro</h3>
    <button onclick="liveRender()">⚡ Çalıştır</button>
</header>

<div class="tab-bar">
    <button id="btn-editor" class="tab-btn active" onclick="switchTab('editor-tab')">📝 Düzenleyici</button>
    <button id="btn-templates" class="tab-btn" onclick="switchTab('templates-tab')">🗂️ Şablonlar</button>
    <button id="btn-ai" class="tab-btn" onclick="switchTab('ai-tab')">🤖 Sınırsız AI Motoru</button>
    <button id="btn-git" class="tab-btn" onclick="switchTab('git-tab')">🐙 Git & Dağıtım</button>
</div>

<div id="editor-tab" class="tab-content active">
    <div class="editor-container">
        <div class="editor-header">
            <span>index.html</span>
        </div>
        <div class="editor-body">
            <textarea id="codeEditor" oninput="autoSaveCode()" placeholder="Kodlarınızı buraya yazın..."></textarea>
        </div>
    </div>
    
    <div class="card">
        <h4>🖥️ Canlı Önizleme Ekranı</h4>
        <div class="preview-wrapper">
            <iframe id="previewFrame"></iframe>
        </div>
    </div>
</div>

<div id="templates-tab" class="tab-content">
    <div class="card">
        <h4>🗂️ Hazır Tasarım Altyapıları</h4>
        <div class="template-grid">
            <button style="background:#1e2235; color:white;" onclick="loadTemplate('portfolio')">💼 Premium Portfolyo</button>
            <button style="background:#1e2235; color:white;" onclick="loadTemplate('ecommerce')">🛒 E-Ticaret Arayüzü</button>
        </div>
    </div>
</div>

<div id="ai-tab" class="tab-content">
    <div class="card">
        <h4>🤖 Evrensel Yapay Zeka Kod Tasarımcısı</h4>
        <input type="text" id="aiPrompt" placeholder="Örn: Arka planı koyu, modern bir müzik çalar yap...">
        <button class="btn-ai" onclick="askRealAI()">✨ Kodu Yapay Zekayla Baştan Yarat</button>
        <div id="aiResult" class="ai-box">Talebiniz doğrultusunda kod üzerinde çalışmak için hazırım...</div>
    </div>
</div>

<div id="git-tab" class="tab-content">
    <div class="card">
        <h4>🐙 GitHub Canlı Yayın Motoru</h4>
        <input type="text" id="githubToken" placeholder="GitHub Personal Access Token">
        <input type="text" id="repoName" placeholder="Repo Adı (Örn: harika-projem)">
        <button class="btn-success" onclick="pushToGithub()">🚀 Projeyi Deploy Et</button>
    </div>
</div>

<script>
    const editor = document.getElementById('codeEditor');

    const defaultCode = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body { background: #f8fafc; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
  .card { background: white; padding: 24px; border-radius: 20px; width: 280px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
  button { background: #0f172a; color: white; border: none; padding: 14px; width: 100%; border-radius: 10px; font-weight: bold; cursor: pointer; }
</style>
</head>
<body>
  <div class="card">
    <h3 style="margin:5px 0;">Cosmic Pro Kulaklık</h3>
    <p style="color:#10b981; font-weight:bold; font-size:18px;">3.499 TL</p>
    <button>Sepete Ekle</button>
  </div>
</body>
</html>`;

    window.onload = function() {
        const savedCode = localStorage.getItem('clouddev_v7_code');
        if(savedCode) {
            editor.value = savedCode;
        } else {
            editor.value = defaultCode;
        }
        liveRender();
    }

    function autoSaveCode() {
        localStorage.setItem('clouddev_v7_code', editor.value);
    }

    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        
        if(tabId === 'editor-tab') {
            document.getElementById('btn-editor').classList.add('active');
            liveRender();
        }
        if(tabId === 'templates-tab') document.getElementById('btn-templates').classList.add('active');
        if(tabId === 'ai-tab') document.getElementById('btn-ai').classList.add('active');
        if(tabId === 'git-tab') document.getElementById('btn-git').classList.add('active');
    }

    function liveRender() {
        document.getElementById('previewFrame').srcdoc = editor.value;
    }

    async function askRealAI() {
        const prompt = document.getElementById('aiPrompt').value;
        const aiResult = document.getElementById('aiResult');

        if(!prompt) { alert("Lütfen yapay zekaya ne yapması gerektiğini söyleyin!"); return; }
        aiResult.innerText = "Yapay zeka çalışıyor...";

        try {
            const response = await fetch('/api/ask-ai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt, current_code: editor.value })
            });
            const data = await response
            
