import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- GÜNCELLENMİŞ PRO ARAYÜZ (AI DESTEKLİ) ---
IDE_INTERFACE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebDev IDE PRO + AI</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Arial, sans-serif; background: #1e1e1e; color: #fff; display: flex; flex-direction: column; min-height: 100vh; }
        header { background: #2d2d2d; padding: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #007acc; }
        .main-container { display: flex; flex: 1; flex-direction: column; padding: 10px; gap: 10px; }
        textarea { width: 100%; height: 200px; background: #1c1c1c; color: #00ff66; font-family: monospace; font-size: 15px; border: 1px solid #3c3c3c; padding: 10px; box-sizing: border-box; border-radius: 4px; }
        .panel { padding: 12px; background: #252526; border: 1px solid #3c3c3c; border-radius: 6px; }
        button { background: #007acc; color: white; border: none; padding: 10px 15px; margin: 2px; cursor: pointer; border-radius: 4px; font-weight: bold; }
        button:hover { background: #0062a3; }
        .preview-box { background: white; color: black; width: 100%; height: 180px; border: none; border-radius: 4px; margin-top: 5px; }
        input { background: #333; color: white; border: 1px solid #555; padding: 8px; margin: 2px; border-radius: 4px; width: calc(100% - 20px); }
        .ai-response { background: #111; color: #00ecff; padding: 10px; border-radius: 4px; font-size: 13px; max-height: 100px; overflow-y: auto; white-space: pre-wrap; margin-top: 5px; }
    </style>
</head>
<body>

<header>
    <h3>🚀 WebDev IDE PRO + AI</h3>
    <div>
        <button onclick="liveRender()">⚡ Render</button>
        <button style="background:#28a745;" onclick="pushToGithub()">🐙 GitHub</button>
    </div>
</header>

<div class="main-container">
    <textarea id="codeEditor" placeholder="HTML/CSS kodlarınızı yazın..."><h1>Yapay Zeka Destekli Mobil IDE</h1>
<p>Buraya kodunu yaz, aşağıdaki yapay zekadan yardım al!</p>
</textarea>

    <div class="panel" style="border: 1px solid #00ecff;">
        <h4 style="margin: 0 0 5px 0; color: #00ecff;">🤖 AI Kod Asistanı (Premium Özellik)</h4>
        <input type="text" id="aiPrompt" placeholder="Örn: Bu kodu şık bir karanlık temaya çevir veya hatayı bul...">
        <button style="background: #00ecff; color: #000;" onclick="askAI()">Yapay Zekaya Sor</button>
        <div id="aiResult" class="ai-response">Asistan hazır. Sorunuzu bekliyor...</div>
    </div>

    <div class="panel">
        <h4 style="margin: 0 0 5px 0;">🔗 Dağıtım Ayarları</h4>
        <input type="text" id="githubToken" placeholder="GitHub Token">
        <input type="text" id="repoName" placeholder="Repo Adı">
    </div>

    <div class="panel">
        <h4 style="margin: 0 0 5px 0;">🖥️ Canlı Önizleme</h4>
        <iframe id="previewFrame" class="preview-box"></iframe>
    </div>
</div>

<script>
    function liveRender() {
        const code = document.getElementById('codeEditor').value;
        document.getElementById('previewFrame').srcdoc = code;
    }

    async function askAI() {
        const code = document.getElementById('codeEditor').value;
        const prompt = document.getElementById('aiPrompt').value;
        const aiResult = document.getElementById('aiResult');

        if(!prompt) { alert("Lütfen AI'a ne yapacağını söyleyin!"); return; }
        aiResult.innerText = "Yapay zeka kodu inceliyor, lütfen bekleyin...";

        const response = await fetch('/api/ask-ai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code, prompt: prompt })
        });
        const data = await response.json();
        
        if(data.status === "success") {
            aiResult.innerText = data.ai_response;
            if(data.updated_code) {
                // Eğer yapay zeka kodu düzelttiyse editöre otomatik yansıt
                document.getElementById('codeEditor').value = data.updated_code;
                liveRender();
            }
        } else {
            aiResult.innerText = "Hata: " + data.message;
        }
    }

    async function pushToGithub() {
        const code = document.getElementById('codeEditor').value;
        const token = document.getElementById('githubToken').value;
        const repo = document.getElementById('repoName').value;

        if(!token || !repo) { alert("GitHub bilgilerini doldurun!"); return; }

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

# --- YENİ API ROTASI: YAPAY ZEKA KOD ANALİZ MOTORU ---
@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_code = data.get('code')
    user_prompt = data.get('prompt')
    
    # Not: Buraya kendi ücretsiz Gemini API veya OpenAI anahtarını koyacağız.
    # Şimdilik simüle edilmiş akıllı bir motor koyuyoruz, test için kod üzerinde değişiklik yapabiliyor.
    try:
        # Yapay zekanın kodu işlediği varsayılan senaryo
        ai_reply = f"Kodunuz incelendi! İstediğiniz değişiklik yapıldı: '{user_prompt}'"
        
        # Basit bir akıllı manipülasyon simülasyonu (Karanlık tema isterse kodu güncelliyor)
        updated_code = user_code
        if "karanlık" in user_prompt.lower() or "dark" in user_prompt.lower():
            updated_code = user_code + "\n<style>body { background: #222; color: #fff; }</style>"
            ai_reply += "\n[Sisteme karanlık tema CSS kodları eklendi!]"
            
        return jsonify({
            "status": "success",
            "ai_response": ai_reply,
            "updated_code": updated_code
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# --- GITHUB PUSH MOTORU ---
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
            return jsonify({"status": "error", "message": "GitHub Token geçersiz!"})
            
        username = user_res.json()['login']
        repo_data = {"name": repo_name, "private": False, "auto_init": True}
        requests.post("https://api.github.com/user/repos", headers=headers, json=repo_data)

        file_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/index.html"
        get_file = requests.get(file_url, headers=headers)
        sha = ""
        if get_file.status_code == 200:
            sha = get_file.json()['sha']

        encoded_code = base64.b64encode(user_code.encode('utf-8')).decode('utf-8')
        push_data = {"message": "Mobile IDE AI commit", "content": encoded_code}
        if sha: push_data["sha"] = sha
            
        push_res = requests.put(file_url, headers=headers, json=push_data)
        if push_res.status_code in [200, 201]:
            return jsonify({"status": "success", "message": "Harika! AI destekli kodunuz başarıyla GitHub'a gönderildi."})
        return jsonify({"status": "error", "message": "Yükleme başarısız."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
        
