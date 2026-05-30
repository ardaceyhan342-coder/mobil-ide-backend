import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ULTRA MODERN PRO + AI + TEMPLATE INTERFACE ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudDev Studio Mobile</title>
    <style>
        :root {
            --bg-main: #141414;
            --bg-panel: #1e1e1e;
            --accent: #007acc;
            --accent-ai: #8a2be2;
            --text: #ffffff;
            --text-dim: #aaaaaa;
            --border: #2d2d2d;
        }
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-main); color: var(--text); display: flex; flex-direction: column; min-height: 100vh; }
        
        /* Üst Bar */
        header { background: var(--bg-panel); padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); box-shadow: 0 2px 8px rgba(0,0,0,0.5); }
        header h3 { margin: 0; font-size: 16px; font-weight: 600; letter-spacing: 0.5px; color: #fff; }
        .header-buttons { display: flex; gap: 8px; }
        
        /* Sekme Sistemi (Tabs) */
        .tab-bar { display: flex; background: #1a1a1a; border-bottom: 1px solid var(--border); overflow-x: auto; }
        .tab-btn { background: none; border: none; color: var(--text-dim); padding: 12px 20px; font-size: 13px; font-weight: 500; cursor: pointer; border-bottom: 2px solid transparent; white-space: nowrap; transition: all 0.2s; }
        .tab-btn.active { color: var(--text); border-bottom-2px solid var(--accent); background: var(--bg-panel); }
        .tab-btn.ai-tab.active { border-bottom-2px solid var(--accent-ai); }
        
        /* İçerik Alanları */
        .tab-content { display: none; padding: 16px; flex: 1; flex-direction: column; gap: 16px; }
        .tab-content.active { display: flex; }
        
        /* Editör Alanı Tasarımı */
        .editor-container { position: relative; background: #1c1c1c; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }
        .editor-header { background: #252526; padding: 6px 12px; font-size: 11px; color: var(--text-dim); border-bottom: 1px solid var(--border); font-family: monospace; }
        textarea { width: 100%; height: 320px; background: #1c1c1c; color: #ce9178; font-family: 'Fira Code', Consolas, Monaco, monospace; font-size: 14px; border: none; padding: 12px; box-sizing: border-box; resize: none; outline: none; line-height: 1.5; }
        
        /* Modern Kartlar ve Formlar */
        .card { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 16px; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .card h4 { margin: 0; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 6px; }
        
        /* Giriş ve Buton Elemanları */
        input, select { background: #2d2d2d; color: var(--text); border: 1px solid var(--border); padding: 10px 14px; border-radius: 6px; font-size: 13px; outline: none; transition: border 0.2s; }
        input:focus, select:focus { border-color: var(--accent); }
        
        button { background: var(--accent); color: white; border: none; padding: 10px 16px; font-size: 13px; font-weight: 600; border-radius: 6px; cursor: pointer; transition: background 0.2s, transform 0.1s; display: inline-flex; align-items: center; justify-content: center; gap: 6px; }
        button:active { transform: scale(0.98); }
        .btn-success { background: #28a745; }
        .btn-ai { background: var(--accent-ai); }
        .btn-secondary { background: #3e3e3f; }
        
        /* Önizleme Alanı */
        .preview-wrapper { border-radius: 8px; overflow: hidden; border: 1px solid var(--border); background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        iframe { width: 100%; height: 280px; border: none; background: white; }
        
        /* Yapay Zeka Yanıt Kutusu */
        .ai-box { background: #121212; border-left: 3px solid var(--accent-ai); padding: 12px; border-radius: 4px; font-size: 13px; color: #00ecff; white-space: pre-wrap; max-height: 150px; overflow-y: auto; font-family: monospace; }
        
        /* Şablon Izgarası */
        .template-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    </style>
</head>
<body>

<header>
    <h3>✨ CloudDev Studio</h3>
    <div class="header-buttons">
        <button onclick="liveRender()">⚡ Çalıştır</button>
    </div>
</header>

<div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('editor-tab')">📝 Editör</button>
    <button class="tab-btn" onclick="switchTab('templates-tab')">🗂️ Şablonlar</button>
    <button class="tab-btn ai-tab" onclick="switchTab('ai-tab')">🤖 AI Asistan</button>
    <button class="tab-btn" onclick="switchTab('git-tab')">🐙 Git & Deploy</button>
</div>

<div id="editor-tab" class="tab-content active">
    <div class="editor-container">
        <div class="editor-header">index.html - HTML5 Workspace</div>
        <textarea id="codeEditor" placeholder="Kodlarınızı buraya yazın..."><!DOCTYPE html>
<html>
<head>
    <style>
        body { background: #121212; color: #ffffff; text-align: center; font-family: sans-serif; padding-top: 80px; }
        .welcome { padding: 20px; border-radius: 10px; background: #1e1e1e; display: inline-block; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
    </style>
</head>
<body>
    <div class="welcome">
        <h2>🚀 CloudDev Dünyasına Hoş Geldiniz!</h2>
        <p>Arayüz tamamen yenilendi. Şablonları ve AI'ı dene!</p>
    </div>
</body>
</html></textarea>
    </div>
    
    <div class="card">
        <h4><span style="color:var(--accent);">🖥️</span> Canlı Ekran (Render Ekranı)</h4>
        <div class="preview-wrapper">
            <iframe id="previewFrame"></iframe>
        </div>
    </div>
</div>

<div id="templates-tab" class="tab-content">
    <div class="card">
        <h4>🗂️ Tek Tıkla Hazır Yapılar Ekle</h4>
        <p style="color: var(--text-dim); font-size: 13px; margin: 0 0 10px 0;">Projene anında profesyonel yapılar enjekte et. Mevcut kodunun yerine yazılır.</p>
        <div class="template-grid">
            <button class="btn-secondary" onclick="loadTemplate('portfolio')">💼 Portfolyo Sitesi</button>
            <button class="btn-secondary" onclick="loadTemplate('ecommerce')">🛒 E-Ticaret Arayüzü</button>
            <button class="btn-secondary" onclick="loadTemplate('landing')">🚀 Ürün Tanıtım (Landing)</button>
            <button class="btn-secondary" onclick="loadTemplate('login')">🔑 Giriş Yap Formu</button>
        </div>
    </div>
</div>

<div id="ai-tab" class="tab-content">
    <div class="card" style="border-color: var(--accent-ai);">
        <h4 style="color: var(--accent-ai);">🤖 Gelişmiş AI Mühendisi</h4>
        <input type="text" id="aiPrompt" placeholder="Örn: Butonları yuvarlat ve gradyan arka plan ekle...">
        <button class="btn-ai" onclick="askAI()">✨ Kodu Yapay Zekaya İşlet</button>
        <div id="aiResult" class="ai-box">Komutlarınızı bekliyorum... Kodunuz üzerinde doğrudan değişiklik yapabilirim.</div>
    </div>
</div>

<div id="git-tab" class="tab-content">
    <div class="card">
        <h4>🐙 GitHub Depo Senkronizasyonu</h4>
        <input type="text" id="githubToken" placeholder="GitHub Personal Access Token (PAT)">
        <input type="text" id="repoName" placeholder="Repo Adı (Örn: mobil-projem)">
        <button class="btn-success" onclick="pushToGithub()">🚀 GitHub Reposuna Gönder</button>
    </div>
</div>

<script>
    // Sekme Değiştirme Fonksiyonu
    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
        
        if(tabId === 'editor-tab') { liveRender(); }
    }

    // Canlı Render
    function liveRender() {
        const code = document.getElementById('codeEditor').value;
        document.getElementById('previewFrame').srcdoc = code;
    }

    // Hazır Şablon Yükleyici
    const templates = {
        portfolio: `<!DOCTYPE html>\\n<html>\\n<head>\\n<style>\\nbody{background:#0f172a;color:#f8fafc;font-family:sans-serif;padding:30px;}\\n.profile{text-align:center;padding:40px;background:#1e293b;border-radius:12px;}\\n.btn{background:#38bdf8;color:#0f172a;padding:10px 20px;border-radius:6px;text-decoration:none;font-weight:bold;}\\n</style>\\n</head>\\n<body>\\n<div class="profile">\\n<h1>Merhaba, Ben Arda 👋</h1>\\n<p>Mobil Cihazlar İçin Geleceğin Teknolojilerini Geliştiriyorum.</p><br>\\n<a href="#" class="btn">Projelerimi Gör</a>\\n</div>\\n</body>\\n</html>`,
        ecommerce: `<!DOCTYPE html>\\n<html>\\n<head>\\n<style>\\nbody{background:#f1f5f9;font-family:sans-serif;padding:20px;display:flex;justify-content:center;}\\n.product{background:#fff;padding:20px;border-radius:12px;box-shadow:0 4px 6px -1px rgba(0,0,0,0.1);width:260px;text-align:center;}\\n.price{color:#22c55e;font-size:20px;font-weight:bold;}\\n.buy-btn{background:#6366f1;color:#fff;border:none;padding:10px;width:100%;border-radius:6px;font-weight:bold;}\\n</style>\\n</head>\\n<body>\\n<div class="product">\\n<h3>Kablosuz Oyuncu Kulaklığı</h3>\\n<p class="price">1.499 TL</p>\\n<button class="buy-btn">Sepete Ekle</button>\\n</div>\\n</body>\\n</html>`,
        landing: `<!DOCTYPE html>\\n<html>\\n<head>\\n<style>\\nbody{background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:#fff;text-align:center;font-family:sans-serif;padding-top:100px;}\\n.cta{font-size:24px;margin-bottom:30px;}\\n.start-btn{background:#fff;color:#764ba2;padding:15px 30px;border-radius:30px;font-weight:bold;border:none;box-shadow:0 4px 15px rgba(0,0,0,0.2);}\\n</style>\\n</head>\\n<body>\\n<h1>Harika Bir Mobil Uygulama Projesi</h1>\\n<p class="cta">Hayallerinizi Gerçeğe Dönüştürmek İçin İlk Adımı Atın.</p>\\n<button class="start-btn">Hemen Ücretsiz Başla</button>\\n</body>\\n</html>`,
        login: `<!DOCTYPE html>\\n<html>\\n<head>\\n<style>\\nbody{background:#09090b;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;margin:0;}\\n.login-card{background:#18181b;padding:30px;border-radius:8px;border:1px solid #27272a;width:280px;color:#fff;}\\ninput{width:100%;padding:10px;margin:8px 0;background:#09090b;border:1px solid #27272a;color:#fff;border-radius:4px;box-sizing:border-box;}\\nbutton{width:100%;padding:10px;background:#fff;color:#000;border:none;font-weight:bold;border-radius:4px;margin-top:10px;}\\n</style>\\n</head>\\n<body>\\n<div class="login-card">\\n<h3>Hesabınıza Giriş Yapın</h3>\\n<input type="text" placeholder="Kullanıcı Adı">\\n<input type="password" placeholder="Şifre">\\n<button>Giriş Yap</button>\\n</div>\\n</body>\\n</html>`
    };

    function loadTemplate(key) {
        if(confirm("Seçtiğiniz şablon yüklenecek. Mevcut kodlarınız silinecektir. Onaylıyor musunuz?")) {
            document.getElementById('codeEditor').value = templates[key];
            switchTab('editor-tab');
        }
    }

    // AI İşleme Motoru
    async function askAI() {
        const code = document.getElementById('codeEditor').value;
        const prompt = document.getElementById('aiPrompt').value;
        const aiResult = document.getElementById('aiResult');

        if(!prompt) { alert("Lütfen talimat yazın!"); return; }
        aiResult.innerText = "Yapay zeka kod mimarisini inceliyor ve düzenliyor...";

        const response = await fetch('/api/ask-ai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, prompt: prompt })
        });
        const data = await response.json();
        
        if(data.status === "success") {
            aiResult.innerText = data.ai_response;
            if(data.updated_code) {
                document.getElementById('codeEditor').value = data.updated_code;
            }
        } else {
            aiResult.innerText = "Hata oluştu: " + data.message;
        }
    }

    // GitHub Dağıtım Motoru
    async function pushToGithub() {
        const code = document.getElementById('codeEditor').value;
        const token = document.getElementById('githubToken').value;
        const repo = document.getElementById('repoName').value;

        if(!token || !repo) { alert("GitHub token ve depo adını eksiksiz girin!"); return; }

        const response = await fetch('/api/github-push', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, token: token, repo: repo })
        });
        const data = await response.json();
        alert(data.message);
    }

    window.onload = liveRender;
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(IDE_INTERFACE)

@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_code = data.get('code')
    user_prompt = data.get('prompt').lower()
    
    try:
        ai_reply = f"İşlem Başarılı! İstediğiniz stil entegrasyonu uygulandı: '{user_prompt}'"
        updated_code = user_code
        
        # Akıllı AI Manipülasyon kuralları (Gelişmiş kural seti)
        if "karanlık" in user_prompt or "dark" in user_prompt:
            updated_code = user_code + "\\n<style>body { background: #121212 !important; color: #ffffff !important; }</style>"
            ai_reply += "\\n[Sistem karanlık arka plan kodlarını enjekte etti.]"
        elif "buton" in user_prompt or "button" in user_prompt:
            updated_code = user_code + "\\n<style>button, .buy-btn, .btn, .start-btn { border-radius: 50px !important; text-transform: uppercase; letter-spacing: 1px; }</style>"
            ai_reply += "\\n[Projedeki tüm buton elemanları yuvarlatıldı ve modernize edildi.]"
        elif "gradyan" in user_prompt or "gradient" in user_prompt:
            updated_code = user_code + "\\n<style>body { background: linear-gradient(135deg, #1e3a8a, #cd1818) !important; color: white; }</style>"
            ai_reply += "\\n[Göz alıcı modern bir gradyan arka plan tanımlandı.]"
        else:
            ai_reply = f"Analiz Tamamlandı: '{user_prompt}' komutuna göre CSS düzenlemeleri alt satıra eklendi."
            updated_code = user_code + f"\\n\\n<style>body { border: 2px solid #8a2be2; }</style>"

        return jsonify({"status": "success", "ai_response": ai_reply, "updated_code": updated_code})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/github-push', methods=['POST'])
def github_push():
    data = request.json
    user_code = data.get('code')
    token = data.get('token')
    repo_name = data.get('repo')
    
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        user_res = requests.get("https://api.github.com/user", headers=headers)
        if user_res.status_code != 200:
            return jsonify({"status": "error", "message": "GitHub Token geçersiz veya yetkisiz!"})
            
        username = user_res.json()['login']
        repo_data = {"name": repo_name, "private": False, "auto_init": True}
        requests.post("https://api.github.com/user/repos", headers=headers, json=repo_data)

        file_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/index.html"
        get_file = requests.get(file_url, headers=headers)
        sha = ""
        if get_file.status_code == 200:
            sha = get_file.json()['sha']

        encoded_code = base64.b64encode(user_code.encode('utf-8')).decode('utf-8')
        push_data = {"message": "CloudDev Studio V3 Auto-Deploy", "content": encoded_code}
        if sha: push_data["sha"] = sha
            
        push_res = requests.put(file_url, headers=headers, json=push_data)
        if push_res.status_code in [200, 201]:
            return jsonify({"status": "success", "message": f"Mükemmel! Kodlar '{repo_name}' reposuna push edildi. Render otomatik derlemeye geçti!"})
        return jsonify({"status": "error", "message": "Dosya gönderilirken API hatası oluştu."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
        
