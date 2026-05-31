import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- V6.7 LANDSCAPE & STABLE PRO ---
IDE_INTERFACE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cosmic Studio v6.7 Pro</title>
    <style>
        :root { --bg: #0a0a0a; --panel: #161616; --text: #f0f0f0; --accent: #3b82f6; --border: #262626; }
        body { margin: 0; display: flex; height: 100vh; background: var(--bg); color: var(--text); font-family: sans-serif; overflow: hidden; }
        
        /* SOL TARAF: EDİTÖR */
        .editor-side { width: 45%; display: flex; flex-direction: column; border-right: 1px solid var(--border); }
        .tabs { display: flex; background: #000; }
        .tab { padding: 12px; cursor: pointer; font-size: 11px; text-transform: uppercase; border-bottom: 2px solid transparent; }
        .tab.active { border-bottom: 2px solid var(--accent); color: var(--accent); }
        textarea { flex: 1; background: #111; color: #fff; border: none; padding: 15px; font-family: 'Courier New', monospace; outline: none; resize: none; }
        
        /* SAĞ TARAF: ÖNİZLEME & AI */
        .preview-side { width: 55%; display: flex; flex-direction: column; padding: 10px; gap: 10px; }
        iframe { flex: 1; border-radius: 8px; border: none; background: #fff; }
        .actions { display: flex; gap: 5px; }
        button { flex: 1; padding: 10px; background: var(--accent); border: none; color: white; font-weight: bold; cursor: pointer; border-radius: 4px; }
        #log { background: #000; padding: 10px; font-size: 10px; color: #0f0; height: 80px; overflow-y: auto; border: 1px solid var(--border); }
    </style>
</head>
<body>

<div class="editor-side">
    <div class="tabs">
        <div id="t-html" class="tab active" onclick="setFile('html')">HTML</div>
        <div id="t-css" class="tab" onclick="setFile('css')">CSS</div>
        <div id="t-js" class="tab" onclick="setFile('js')">JS</div>
    </div>
    <textarea id="editor" oninput="update()"></textarea>
</div>

<div class="preview-side">
    <iframe id="frame"></iframe>
    <div id="log">> Sistem hazır...</div>
    <div class="actions">
        <button onclick="askAI()">🤖 AI Üret</button>
        <button onclick="alert('Yayına hazır!')" style="background:#22c55e;">🚀 Deploy</button>
    </div>
</div>

<script>
    let data = { html: '<h1>Merhaba Cosmic!</h1>', css: 'body{background:#000;color:#fff;}', js: 'console.log("Ready");' };
    let active = 'html';

    function setFile(f) {
        data[active] = document.getElementById('editor').value;
        active = f;
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.getElementById('t-'+f).classList.add('active');
        document.getElementById('editor').value = data[f];
    }

    function update() {
        data[active] = document.getElementById('editor').value;
        let combined = data.html.replace('</head>', `<style>${data.css}</style></head>`)
                                .replace('</body>', `<script>${data.js}<\\/script></body>`);
        document.getElementById('frame').srcdoc = combined;
    }

    async function askAI() {
        let p = prompt("Ne tasarlamamı istersin?");
        if(!p) return;
        document.getElementById('log').innerText = "> Üretiliyor...";
        let r = await fetch('/api/ai', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({p}) });
        let res = await r.json();
        if(res.h) { data.html=res.h; data.css=res.c; data.js=res.j; setFile('html'); update(); document.getElementById('log').innerText = "> Başarılı!"; }
    }
    
    // Açılış
    document.getElementById('editor').value = data.html;
    update();
</script>
</body>
</html>"""

@app.route('/')
def index(): return render_template_string(IDE_INTERFACE)

@app.route('/api/ai', methods=['POST'])
def ai():
    try:
        p = request.json.get('p')
        url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B-Instruct"
        payload = {"inputs": f"Gorev: {p}. Yanıtı sadece bu formatta ver: ===HTML===[kod]===CSS===[kod]===JS===[kod]"}
        r = requests.post(url, json=payload, timeout=30)
        t = r.json()[0]['generated_text']
        
        # Güvenli parçalama
        h = t.split("===HTML===")[1].split("===CSS===")[0].strip() if "===HTML===" in t else ""
        c = t.split("===CSS===")[1].split("===JS===")[0].strip() if "===CSS===" in t else ""
        j = t.split("===JS===")[1].strip() if "===JS===" in t else ""
        return jsonify({"h": h, "c": c, "j": j})
    except: return jsonify({"error": "AI yanıt vermedi"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
