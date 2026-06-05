import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- V11 COSMIC ULTIMATE INTERFACE (TÜM ÖZELLİKLER KORUNDU + MÜZİK ŞABLONU EKLENDİ) ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudDev Studio v11 Cosmic Ultimate</title>
    <style>
        :root {
            --bg-main: #08090c;
            --bg-panel: #11131c;
            --accent: #38bdf8;
            --accent-ai: #c084fc;
            --text: #f8fafc;
            --text-dim: #64748b;
            --border: #1e293b;
            --success: #4ade80;
        }
        
        body.theme-cyberpunk {
            --bg-main: #0f051d;
            --bg-panel: #1a0b2e;
            --accent: #ff007f;
            --accent-ai: #00ffff;
            --text: #ffffff;
            --text-dim: #9d4edd;
            --border: #3c1670;
            --success: #39ff14;
        }
        
        body.theme-matrix {
            --bg-main: #000000;
            --bg-panel: #0d0d0d;
            --accent: #00ff41;
            --accent-ai: #008f11;
            --text: #00ff41;
            --text-dim: #005c0c;
            --border: #00ff41;
            --success: #ffffff;
        }

        body { 
            margin: 0; 
            font-family: system-ui, -apple-system, sans-serif; 
            background: var(--bg-main); 
            color: var(--text); 
            display: flex; 
            flex-direction: column; 
            min-height: 100vh; 
            transition: background 0.3s, color 0.3s; 
        }
        header { 
            background: var(--bg-panel); 
            padding: 14px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid var(--border); 
            box-shadow: 0 4px 30px rgba(0,0,0,0.4); 
        }
        header h3 { 
            margin: 0; 
            font-size: 16px; 
            font-weight: 800; 
            background: linear-gradient(to right, var(--accent), var(--accent-ai)); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        
        .actions-row { 
            display: flex; 
            gap: 10px; 
            align-items: center;
        }
        select { 
            background: #1e2235; 
            color: var(--text); 
            border: 1px solid var(--border); 
            padding: 10px; 
            border-radius: 8px; 
            font-size: 12px; 
            font-weight: 600; 
            outline: none; 
            cursor: pointer; 
        }
        
        .tab-bar { 
            display: flex; 
            background: #0b0c12; 
            border-bottom: 1px solid var(--border); 
            overflow-x: auto; 
            scrollbar-width: none; 
        }
        .tab-bar::-webkit-scrollbar { display: none; }
        .tab-btn { 
            background: none; 
            border: none; 
            color: var(--text-dim); 
            padding: 14px 22px; 
            font-size: 13px; 
            font-weight: 600; 
            cursor: pointer; 
            border-bottom: 2px solid transparent; 
            white-space: nowrap; 
            transition: all 0.2s; 
        }
        .tab-btn.active { 
            color: var(--text); 
            border-bottom: 2px solid var(--accent); 
            background: var(--bg-panel); 
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
            border: 1px solid var(--border); 
            border-radius: 12px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
            position: relative; 
        }
        .editor-header { 
            background: #161926; 
            padding: 10px 16px; 
            font-size: 12px; 
            color: var(--text-dim); 
            border-bottom: 1px solid var(--border); 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }
        
        .editor-body { 
            display: flex; 
            height: 380px; 
            font-family: monospace; 
            font-size: 14px; 
            line-height: 1.6; 
            background: #0d0f17; 
            position: relative; 
        }
        .line-numbers { 
            padding: 16px 8px; 
            text-align: right; 
            background: #0a0b10; 
            color: #334155; 
            user-select: none; 
            min-width: 45px; 
            border-right: 1px solid #141724; 
            overflow: hidden; 
            white-space: pre; 
            box-sizing: border-box; 
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
            white-space: pre; 
            font-family: monospace; 
        }
        
        .editor-footer { 
            background: #161926; 
            padding: 6px 16px; 
            font-size: 11px; 
            color: var(--text-dim); 
            border-top: 1px solid var(--border); 
            display: flex; 
            justify-content: flex-end; 
            gap: 14px; 
        }
        
        .card { 
            background: var(--bg-panel); 
            border: 1px solid var(--border); 
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
            color: var(--text); 
            border: 1px solid var(--border); 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 13px; 
            outline: none; 
        }
        
        button { 
            background: var(--accent); 
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
            transition: all 0.2s; 
        }
        button:active { transform: scale(0.97); }
        .btn-success { background: var(--success); color: #052e16; }
        .btn-ai { background: var(--accent-ai); color: #2e1065; }
        .btn-secondary { background: #1e2235; color: var(--text); border: 1px solid var(--border); }
        
        .preview-wrapper { 
            border-radius: 10px; 
            overflow: hidden; 
            border: 1px solid var(--border); 
            background: #fff; 
        }
        iframe { 
            width: 100%; 
            height: 320px; 
            border: none; 
            background: white; 
        }
        
        .ai-box { 
            background: #05060a; 
            border-left: 4px solid var(--accent-ai); 
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
        .save-indicator { 
            font-size: 11px; 
            color: var(--success); 
            font-weight: 600; 
            display: none; 
        }
    </style>
</head>
<body class="theme-cosmic">

<header>
    <h3>✨ CloudDev Cosmic v11 Pro</h3>
    <div class="actions-row">
        <select id="themeSelect" onchange="changeTheme()">
            <option value="theme-cosmic">🌌 Cosmic</option>
            <option value="theme-cyberpunk">🔮 Cyberpunk</option>
            <option value="theme-matrix">📟 Matrix</option>
        </select>
        <button class="btn-secondary" onclick="downloadCode()">📥 İndir</button>
        <button onclick="liveRender()">⚡ Çalıştır</button>
    </div>
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
            <span id="saveStatus" class="save-indicator">✓ Otomatik Kaydedildi</span>
        </div>
        <div class="editor-body">
            <div id="lineNumbers" class="line-numbers">1</div>
            <textarea id="codeEditor" oninput="handleEditorInput()" onscroll="syncScroll()" placeholder="Kodlarınızı buraya yazın..." wrap="off"></textarea>
        </div>
        <div class="editor-footer">
            <span id="charCount">Karakter: 0</span>
            <span id="lineCount">Satır: 1</span>
            <span id="sizeCount">Boyut: 0.00 KB</span>
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
            <button style="background:#1e2235; color:white;" onclick="loadTemplate('music')">🎵 Kozmik Müzik Çalar</button>
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
    const lineNumbers = document.getElementById('lineNumbers');

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
        const savedCode = localStorage.getItem('clouddev_v10_code');
        const savedTheme = localStorage.getItem('clouddev_theme') || 'theme-cosmic';
        
        document.body.className = savedTheme;
        document.getElementById('themeSelect').value = savedTheme;

        if(savedCode) {
            editor.value = savedCode;
        } else {
            editor.value = defaultCode;
        }
        updateLineNumbers();
        updateMetrics();
        liveRender();
    }

    function handleEditorInput() {
        updateLineNumbers();
        updateMetrics();
        autoSaveCode();
    }

    function changeTheme() {
        const selectedTheme = document.getElementById('themeSelect').value;
        document.body.className = selectedTheme;
        localStorage.setItem('clouddev_theme', selectedTheme);
    }

    function updateLineNumbers() {
        const lines = editor.value.split('\\n');
        let numString = '';
        for (let i = 1; i <= lines.length; i++) {
            numString += i + '\\n';
        }
        lineNumbers.textContent = numString;
    }

    function updateMetrics() {
        const text = editor.value;
        const totalLines = text.split('\\n').length;
        const totalChars = text.length;
        const byteSize = new Blob([text]).size;
        const kbSize = (byteSize / 1024).toFixed(2);

        document.getElementById('charCount').textContent = `Karakter: ${totalChars}`;
        document.getElementById('lineCount').textContent = `Satır: ${totalLines}`;
        document.getElementById('sizeCount').textContent = `Boyut: ${kbSize} KB`;
    }

    function syncScroll() {
        lineNumbers.scrollTop = editor.scrollTop;
    }

    function autoSaveCode() {
        localStorage.setItem('clouddev_v10_code', editor.value);
        const indicator = document.getElementById('saveStatus');
        indicator.style.display = 'inline';
        setTimeout(() => { indicator.style.display = 'none'; }, 1500);
    }

    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        
        if(tabId === 'editor-tab') document.getElementById('btn-editor').classList.add('active');
        if(tabId === 'templates-tab') document.getElementById('btn-templates').classList.add('active');
        if(tabId === 'ai-tab') document.getElementById('btn-ai').classList.add('active');
        if(tabId === 'git-tab') document.getElementById('btn-git').classList.add('active');
        
        if(tabId === 'editor-tab') { 
            liveRender(); 
            setTimeout(() => { updateLineNumbers(); syncScroll(); }, 50); 
        }
    }

    function liveRender() {
        try {
            document.getElementById('previewFrame').srcdoc = editor.value;
        } catch(e) {
            console.log("Önizleme yüklenemedi.");
        }
    }

    function downloadCode() {
        const code = editor.value;
        const blob = new Blob([code], { type: 'text/html' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'index.html';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    async function askRealAI() {
        const prompt = document.getElementById('aiPrompt').value;
        const aiResult = document.getElementById('aiResult');

        if(!prompt) { alert("Lütfen yapay zekaya ne yapması gerektiğini söyleyin!"); return; }
        aiResult.innerText = "Yapay zeka kod mimarisini işliyor...";

        try {
            const response = await fetch('/api/ask-ai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt, current_code: editor.value })
            });
            const data = await response.json();
            
            if(data.status === "success") {
                aiResult.innerText = "Kod başarıyla entegre edildi!";
                editor.value = data.updated_code;
                handleEditorInput();
                liveRender();
            } else {
                aiResult.innerText = "Hata: " + data.message;
            }
        } catch (e) {
            aiResult.innerText = "Bağlantı zaman aşımına uğradı.";
        }
    }

    const templates = {
        portfolio: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { background: #090a0f; color: #f3f4f6; font-family: sans-serif; padding: 50px 20px; text-align: center; }
.container { max-width: 600px; margin: auto; background: #121420; padding: 30px; border-radius: 20px; border: 1px solid #1f2937; }
h1 { color: #38bdf8; }
</style>
</head>
<body>
<div class="container">
  <h1>Geliştirici Portfolyosu</h1>
  <p>CloudDev v11 Canlı Tasarım Altyapısı.</p>
</div>
</body>
</html>`,
        ecommerce: defaultCode,
        music: `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { background: #0e0b16; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .player { background: #1b1429; padding: 24px; border-radius: 24px; width: 300px; text-align: center; border: 1px solid #4717f6; color: white; }
    .cover { background: linear-gradient(45deg, #a239ca, #4717f6); width: 100px; height: 100px; margin: 0 auto 20px auto; border-radius: 50%; }
    .controls { display: flex; justify-content: center; gap: 15px; margin-top: 15px; }
    button { background: #a239ca; color: white; border: none; padding: 10px 18px; border-radius: 12px; cursor: pointer; font-weight: bold; }
  </style>
</head>
<body>
  <div class="player">
    <div class="cover"></div>
    <h4 style="margin:5px 0;">Cosmic Symphony</h4>
    <p style="color:#a239ca; font-size:12px; margin:0 0 15px 0;">CloudDev Records</p>
    <div class="controls"><button>⏮</button><button>▶</button><button>⏭</button></div>
  </div>
</body>
</html>`
    };

    function loadTemplate(key) {
        if(confirm("Mevcut kodlarınız silinecek. Devam edilsin mi?")) {
            editor.value = templates[key];
            handleEditorInput();
            switchTab('editor-tab');
        }
    }

    async function pushToGithub() {
        const code = editor.value;
        const token = document.getElementById('githubToken').value;
        const repo = document.getElementById('repoName').value;
        if(!token || !repo) { alert("Lütfen alanları eksiksiz doldurun!"); return; }

        try {
            const response = await fetch('/api/github-push', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code, token: token, repo: repo })
            });
            const data = await response.json();
            alert(data.message);
        } catch(e) {
            alert("GitHub push bağlantı hatası.");
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(IDE_INTERFACE)

@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_prompt = data.get('prompt', '')
    current_code = data.get('current_code', '')
    
    API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B-Instruct"
    system_instruction = "Sen profesyonel bir frontend mühendisisin. Verilen HTML kodunu bo
