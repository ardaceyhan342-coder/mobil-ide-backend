import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- V9 CLEAN COSMIC PRODUCTION INTERFACE ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudDev Studio v9 Cosmic Pro</title>
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
        body { margin: 0; font-family: system-ui, -apple-system, sans-serif; background: var(--bg-main); color: var(--text); display: flex; flex-direction: column; min-height: 100vh; }
        header { background: var(--bg-panel); padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); box-shadow: 0 4px 30px rgba(0,0,0,0.4); }
        header h3 { margin: 0; font-size: 16px; font-weight: 800; background: linear-gradient(to right, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        .tab-bar { display: flex; background: #0b0c12; border-bottom: 1px solid var(--border); overflow-x: auto; scrollbar-width: none; }
        .tab-bar::-webkit-scrollbar { display: none; }
        .tab-btn { background: none; border: none; color: var(--text-dim); padding: 14px 22px; font-size: 13px; font-weight: 600; cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap; transition: all 0.2s; }
        .tab-btn.active { color: var(--text); border-bottom: 2px solid var(--accent); background: var(--bg-panel); }
        .tab-btn.ai-tab.active { border-bottom: 2px solid var(--accent-ai); }
        
        .tab-content { display: none; padding: 16px; flex: 1; flex-direction: column; gap: 16px; box-sizing: border-box; }
        .tab-content.active { display: flex; }
        
        .editor-container { background: #0d0f17; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .editor-header { background: #161926; padding: 10px 16px; font-size: 12px; color: var(--text-dim); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        
        .editor-body { display: flex; height: 380px; font-family: monospace; font-size: 14px; line-height: 1.6; background: #0d0f17; }
        .line-numbers { padding: 16px 8px; text-align: right; background: #0a0b10; color: #334155; user-select: none; min-width: 35px; border-right: 1px solid #141724; overflow-y: hidden; white-space: pre; box-sizing: border-box; }
        textarea { flex: 1; background: transparent; color: #e2e8f0; border: none; padding: 16px; box-sizing: border-box; resize: none; outline: none; height: 100%; overflow-y: auto; white-space: pre; font-family: monospace; }
        
        .card { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 14px; }
        .card h4 { margin: 0; font-size: 14px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
        
        input { background: #181b28; color: var(--text); border: 1px solid var(--border); padding: 12px; border-radius: 8px; font-size: 13px; outline: none; }
        input:focus { border-color: var(--accent); }
        
        button { background: var(--accent); color: #090d16; border: none; padding: 12px 20px; font-size: 13px; font-weight: 700; border-radius: 8px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.2s; }
        button:active { transform: scale(0.97); }
        .btn-success { background: var(--success); color: #052e16; }
        .btn-ai { background: var(--accent-ai); color: #2e1065; }
        .btn-secondary { background: #1e2235; color: var(--text); border: 1px solid var(--border); }
        
        .preview-wrapper { border-radius: 10px; overflow: hidden; border: 1px solid var(--border); background: #fff; }
        iframe { width: 100%; height: 320px; border: none; background: white; }
        
        .ai-box { background: #05060a; border-left: 4px solid var(--accent-ai); padding: 14px; border-radius: 8px; font-size: 13px; color: #cbd5e1; white-space: pre-wrap; max-height: 200px; overflow-y: auto; font-family: monospace; }
        .template-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .save-indicator { font-size: 11px; color: var(--success); font-weight: 600; display: none; }
        
        .actions-row { display: flex; gap: 10px; }
    </style>
</head>
<body>

<header>
    <h3>✨ CloudDev Cosmic v9</h3>
    <div class="actions-row">
        <button class="btn-secondary" onclick="downloadCode()">📥 İndir</button>
        <button onclick="liveRender()">⚡ Çalıştır</button>
    </div>
</header>

<div class="tab-bar">
    <button id="btn-editor" class="tab-btn active" onclick="switchTab('editor-tab')">📝 Düzenleyici</button>
    <button id="btn-templates" class="tab-btn" onclick="switchTab('templates-tab')">🗂️ Şablonlar</button>
    <button id="btn-ai" class="tab-btn ai-tab" onclick="switchTab('ai-tab')">🤖 Sınırsız AI Motoru</button>
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
            <textarea id="codeEditor" oninput="handleEditorInput()" onscroll="syncScroll()" placeholder="Kodlarınızı buraya yazın..."></textarea>
        </div>
    </div>
    
    <div class="card">
        <h4><span style="color:var(--accent);">🖥️</span> Canlı Önizleme Ekranı</h4>
        <div class="preview-wrapper">
            <iframe id="previewFrame"></iframe>
        </div>
    </div>
</div>

<div id="templates-tab" class="tab-content">
    <div class="card">
        <h4>🗂️ Hazır Tasarım Altyapıları</h4>
        <div class="template-grid">
            <button class="btn-secondary" onclick="loadTemplate('portfolio')">💼 Premium Portfolyo</button>
            <button class="btn-secondary" onclick="loadTemplate('ecommerce')">🛒 E-Ticaret Arayüzü</button>
            <button class="btn-secondary" onclick="loadTemplate('landing')">🚀 Kripto Sayfası</button>
            <button class="btn-secondary" onclick="loadTemplate('dashboard')">📊 Yönetim Paneli</button>
        </div>
    </div>
</div>

<div id="ai-tab" class="tab-content">
    <div class="card" style="border-color: var(--accent-ai);">
        <h4 style="color: var(--accent-ai);">🤖 Evrensel Yapay Zeka Kod Tasarımcısı</h4>
        <p style="color:var(--text-dim); font-size:12px; margin:0;">İstediğiniz web sayfasını, oyunu veya uygulamayı Türkçe yazın. Yapay zeka kodu güncelleyecektir.</p>
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
        <button class="btn-success" onclick="pushToGithub()">🚀 Projeyi Deplo Et</button>
    </div>
</div>

<script>
    const editor = document.getElementById('codeEditor');
    const lineNumbers = document.getElementById('lineNumbers');

    const defaultCode = `<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
  body { background: #0a0b10; color: white; font-family: sans-serif; text-align: center; padding-top: 100px; }
  .welcome { padding: 30px; background: #11131c; border-radius: 16px; border: 1px solid #1e293b; display: inline-block; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
  h1 { color: #38bdf8; }
</style>
</head>
<body>
  <div class="welcome">
    <h1>🌌 CloudDev Cosmic v9 Pro</h1>
    <p>Kodlarınızı yazın veya Sınırsız AI motoruyla hayalinizdeki siteyi inşa edin.</p>
  </div>
</body>
</html>`;

    window.onload = function() {
        const savedCode = localStorage.getItem('clouddev_v6_code');
        if(savedCode) {
            editor.value = savedCode;
        } else {
            editor.value = defaultCode;
        }
        updateLineNumbers();
        liveRender();
    }

    function handleEditorInput() {
        updateLineNumbers();
        autoSaveCode();
    }

    function updateLineNumbers() {
        const lines = editor.value.split('\\n').length;
        let numString = '';
        for (let i = 1; i <= lines; i++) {
            numString += i + '\\n';
        }
        lineNumbers.textContent = numString;
    }

    function syncScroll() {
        lineNumbers.scrollTop = editor.scrollTop;
    }

    function autoSaveCode() {
        localStorage.setItem('clouddev_v6_code', editor.value);
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
        
        if(tabId === 'editor-tab') { liveRender(); setTimeout(updateLineNumbers, 50); }
    }

    function liveRender() {
        try {
            document.getElementById('previewFrame').srcdoc = editor.value;
        } catch(err) {
            console.log("Önizleme yükleme hatası izole edildi.");
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
        aiResult.innerText = "Yapay zeka tüm kod bloklarını inceliyor. Lütfen bekleyin...";

        try {
            const response = await fetch('/api/ask-ai', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt, current_code: editor.value })
            });
            const data = await response.json();
            
            if(data.status === "success") {
                aiResult.innerText = "Yapay zeka kodu başarıyla enjekte etti!";
                editor.value = data.updated_code;
                updateLineNumbers();
                autoSaveCode();
                liveRender();
            } else {
                aiResult.innerText = "Hata: " + data.message;
            }
        } catch (e) {
            aiResult.innerText = "Bağlantı hatası.";
        }
    }

    const templates = {
        portfolio: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { background: #090a0f; color: #f3f4f6; font-family: sans-serif; padding: 50px 20px; text-align: center; }
.container { max-width: 600px; margin: auto; background: #121420; padding: 30px; border-radius: 20px; border: 1px solid #1f2937; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
h1 { color: #38bdf8; margin-bottom: 5px; }
.tag { color: #a855f7; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
</style>
</head>
<body>
<div class="container">
  <h1>Arda Ceyhan</h1>
  <div class="tag">Full Stack Cloud Developer</div>
  <p>Yapay zeka destekli mobil sistemler ve yenilikçi web mimarileri üzerine çalışan bağımsız geliştirici.</p>
</div>
</body>
</html>`,
        ecommerce: `<!DOCTYPE html>
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
</html>`,
        landing: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { background: #030712; color: white; font-family: sans-serif; text-align: center; padding: 120px 20px 0; margin: 0; height: 100vh; background-image: radial-gradient(circle at top, #1e1b4b 0%, #030712 70%); }
.btn { background: linear-gradient(to right, #38bdf8, #a855f7); color: white; padding: 16px 32px; border-radius: 50px; border: none; font-weight: bold; font-size: 16px; cursor: pointer; }
</style>
</head>
<body>
  <h1>Merkeziyetsiz Geleceğe Adım Atın</h1>
  <button class="btn">Ekosistemi Keşfet</button>
</body>
</html>`,
        dashboard: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { background: #0f172a; color: white; font-family: sans-serif; margin: 0; display: flex; height: 100vh; }
.main { flex: 1; padding: 24px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px; }
.stat { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
.num { font-size: 24px; font-weight: bold; color: #38bdf8; }
</style>
</head>
<body>
<div class="main">
  <h2>Yönetim Paneli</h2>
  <div class="grid">
    <div class="stat"><div>Aktif Kullanıcı</div><div class="num">1,420</div></div>
    <div class="stat"><div>Aylık Ciro</div><div class="num">$12,850</div></div>
  </div>
</div>
</body>
</html>`
    };

    function loadTemplate(key) {
        if(confirm("Yazmakta olduğunuz kodlar silinecek. Devam edilsin mi?")) {
            editor.value = templates[key];
            updateLineNumbers();
            autoSaveCode();
            switchTab('editor-tab');
        }
    }

    async function pushToGithub() {
        const code = editor.value;
        const token = document.getElementById('githubToken').value;
        const repo = document.getElementById('repoName').value;
        if(!token || !repo) { alert("Lütfen boş alanları doldurun!"); return; }

        const response = await fetch('/api/github-push', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, token: token, repo: repo })
        });
        const data = await response.json();
        alert(data.message);
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
    
    system_instruction = (
        "Sen gelişmiş bir frontend mimarısın. Sana verilen HTML/CSS/JS bütünleşik kod yapısını bozmadan, "
        "kullanıcının isteği doğrultusunda kodu baştan aşağı geliştir veya yeni özellikler enjekte et. "
        "Yanıtında asla markdown sembolleri (```html) veya hiçbir açıklama/konuşma metni kullanma. Doğrudan tarayıcının çalıştırabileceği saf tek parça kodu döndür."
    )
    
    payload = {
        "inputs": f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\nMevcut Kod:\n{current_code}\n\nYapılacak Değişiklik/İstek: {user_prompt}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {"max_new_tokens": 1800, "temperature": 0.3}
    }
    
    try:
        res = requests.post(API_URL, json=payload, timeout=25)
        if res.status_code == 200:
            raw_text = res.json()[0]['generated_text']
            updated_code = raw_text.split("<|im_start|>assistant\n")[-1].strip() if "<|im_start|>assistant\n" in raw_text else raw_text
            
            for clean_term in ["```html", "```css", "```javascript", "```js", "```", "<|im_end|>"]:
                updated_code = updated_code.replace(clean_term, "")
            
            if "<!DOCTYPE html>" in updated_code:
                updated_code = updated_code[updated_code.find("<!DOCTYPE html>"):]
                
            return jsonify({
                "status": "success",
                "updated_code": updated_code.strip()
            })
        return jsonify({"status": "error", "message": f"AI Servis Hatası (Kod: {res.status_code})"})
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Zaman aşımı oluştu."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/github-push', methods=['POST'])
def github_push():
    data = request.json or {}
    user_code = data.get('code', '')
    token = data.get('token', '')
    repo_name = data.get('repo', '')
    
    if not token or not repo_name:
        return jsonify({"status": "error", "message": "Eksik parametre!"})
        
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        user_res = requests.get("https://api.github.com/user", headers=headers, timeout=15)
        if user_res.status_code != 200:
            return jsonify({"status": "error", "message": "GitHub Token geçersiz!"})
            
        username = user_res.json()['login']
        repo_data = {"name": repo_name, "private": False, "auto_init": True}
        requests.post("https://api.github.com/user/repos", headers=headers, json=repo_data, timeout=15)

        file_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/index.html"
        get_file = requests.get(file_url, headers=headers, timeout=15)
        sha = ""
        if get_file.status_code == 200:
            sha = get_file.json()['sha']

        encoded_code = base64.b64encode(user_code.encode('utf-8')).decode('utf-8')
        push_data = {"message": "CloudDev Cosmic v9 Deploy", "content": encoded_code}
        if sha: push_data["sha"] = sha
            
        push_res = requests.put(file_url, headers=headers, json=push_data, timeout=15)
        if push_res.status_code in [200, 201]:
            return jsonify({"status": "success", "message": "Projeniz başarıyla güncellendi!"})
        return jsonify({"status": "error", "message": "Yükleme hatası."})
    except Exception as e:
    
