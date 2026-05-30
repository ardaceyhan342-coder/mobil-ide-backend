import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Kullanıcının projelerinin telefonda saklanacağı klasör
PROJECTS_DIR = os.path.abspath("./mobil_projeler")
if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# --- TARAYICIDA AÇILACAK PRO IDE ARAYÜZÜ (HTML + İŞLEVLER) ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile WebDev IDE PRO</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Arial, sans-serif; background: #1e1e1e; color: #fff; display: flex; flex-direction: column; h-weight: 100vh; }
        header { background: #2d2d2d; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #007acc; }
        .main-container { display: flex; flex: 1; flex-direction: column; }
        textarea { width: 100%; height: 250px; background: #1c1c1c; color: #00ff66; font-family: monospace; font-size: 16px; border: none; padding: 10px; box-sizing: border-box; }
        .panel { padding: 15px; background: #252526; border-top: 1px solid #3c3c3c; }
        button { background: #007acc; color: white; border: none; padding: 10px 15px; margin: 5px; cursor: pointer; border-radius: 4px; font-weight: bold; }
        button:hover { background: #0062a3; }
        .preview-box { background: white; color: black; width: 100%; height: 200px; border: none; margin-top: 10px; }
        input { background: #333; color: white; border: 1px solid #555; padding: 8px; margin: 5px; border-radius: 4px; }
    </style>
</head>
<body>

<header>
    <h2>🚀 WebDev IDE PRO (Mobil)</h2>
    <div>
        <button onclick="liveRender()">⚡ Anlık Render</button>
        <button style="background:#28a745;" onclick="pushToGithub()">🐙 GitHub'a Gönder</button>
    </div>
</header>

<div class="main-container">
    <textarea id="codeEditor" placeholder="HTML/CSS/JS kodlarınızı buraya yazın..."><!DOCTYPE html>
<html>
<head>
    <style>
        body { background: linear-gradient(to right, #667db6, #0082c8, #0082c8, #667db6); text-align: center; color: white; font-family: sans-serif; padding-top: 50px; }
        .card { background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); display: inline-block; padding: 30px; border-radius: 15px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Render & GitHub Entegrasyonu</h1>
        <p>Bu site mobildeki yerel sunucudan render ediliyor!</p>
    </div>
</body>
</html></textarea>

    <div class="panel">
        <h3>🔗 GitHub & Render Canlı Yayın Ayarları</h3>
        <input type="text" id="githubToken" placeholder="GitHub Kişisel Erişim Tokeni (PAT)">
        <input type="text" id="repoName" placeholder="Repo Adı (örn: mobil-sitem)">
        <p style="font-size: 12px; color: #aaa;">*Not: GitHub'a yüklendikten sonra Render.com üzerinden bu repoyu bağlayarak sitenizi ömür boyu ücretsiz yayınlayabilirsiniz!</p>
    </div>

    <div class="panel" style="flex: 1; display: flex; flex-direction: column;">
        <h3>🖥️ Gerçek Zamanlı Render (Canlı Önizleme)</h3>
        <iframe id="previewFrame" class="preview-box"></iframe>
    </div>
</div>

<script>
    // 1. İŞLEV: GERÇEK ZAMANLI RENDER MOTORU
    function liveRender() {
        const code = document.getElementById('codeEditor').value;
        const iframe = document.getElementById('previewFrame');
        iframe.srcdoc = code;
    }

    // 2. İŞLEV: GITHUB API ENTEGRASYONU (DAĞITIM MOTORU)
    async function pushToGithub() {
        const code = document.getElementById('codeEditor').value;
        const token = document.getElementById('githubToken').value;
        const repo = document.getElementById('repoName').value;

        if(!token || !repo) {
            alert("Lütfen GitHub Token ve Repo alanlarını doldurun!");
            return;
        }

        alert("GitHub API ile bağlantı kuruluyor... Lütfen bekleyin.");

        // Arka plandaki Python sunucumuza verileri gönderiyoruz
        const response = await fetch('/api/github-push', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, token: token, repo: repo })
        });

        const data = await response.json();
        alert(data.message);
    }

    // İlk açılışta otomatik render et
    window.onload = liveRender;
</script>

</body>
</html>
"""

# --- API ROTASI: TARAYICIYA ARAYÜZÜ BASAR ---
@app.route('/')
def index():
    return render_template_string(IDE_INTERFACE)

# --- API ROTASI: GITHUB'A KODLARI PUSH EDEN MOTOR (İŞLEVSEL ARKA PLAN) ---
@app.route('/api/github-push', methods=['POST'])
def github_push():
    data = request.json
    user_code = data.get('code')
    token = data.get('token')
    repo_name = data.get('repo')
    
    # Adım 1: GitHub'da yeni bir repo oluşturma (Yoksa)
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repo_data = {"name": repo_name, "private": False, "auto_init": True}
    
    # Repo var mı kontrol et, yoksa oluştur
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code != 200:
        return jsonify({"status": "error", "message": "GitHub Token geçersiz!"}), 401
        
    username = user_res.json()['login']
    
    create_repo_res = requests.post("https://api.github.com/user/repos", headers=headers, json=repo_data)
    # 201: Oluşturuldu, 422: Zaten var anlamına gelir (İki durumda da devam edebiliriz)

    # Adım 2: index.html dosyasını GitHub Reposuna yükleme/güncelleme
    file_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/index.html"
    
    # Dosya daha önce var mı diye bak (varsa sha değerini almamız gerekir güncellemek için)
    get_file = requests.get(file_url, headers=headers)
    sha = ""
    if get_file.status_code == 200:
        sha = get_file.json()['sha']

    import base64
    encoded_code = base64.b64encode(user_code.encode('utf-8')).decode('utf-8')
    
    push_data = {
        "message": "Mobile IDE uzerinden otomatik commit",
        "content": encoded_code
    }
    if sha:
        push_data["sha"] = sha
        
    push_res = requests.put(file_url, headers=headers, json=push_data)
    
    if push_res.status_code in [200, 201]:
        return jsonify({
            "status": "success", 
            "message": f"Başarılı! Kodlarınız GitHub'da '{repo_name}' reposuna yüklendi.\nNow, Render.com'a girip bu repoyu bağlayarak sitenizi saniyeler içinde canlıya alabilirsiniz!"
        })
    else:
        return jsonify({"status": "error", "message": f"GitHub'a yüklenirken hata oluştu: {push_res.text}"})

if __name__ == '__main__':
    # Sunucuyu telefonda başlatıyoruz
    app.run(host='0.0.0.0', port=5000, debug=True)
