import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- ADIM 1: ŞABLON KÜTÜPHANESİ ---
# JavaScript içinde tırnak hatası yaratmamak için şablonları Python içinde izole ediyoruz.
PORTFOLIO_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { background: #090a0f; color: #f3f4f6; font-family: sans-serif; padding: 50px 20px; text-align: center; }
    .container { max-width: 600px; margin: auto; background: #121420; padding: 30px; border-radius: 20px; border: 1px solid #1f2937; }
    h1 { color: #38bdf8; }
    p { color: #9ca3af; font-size: 16px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Geliştirici Portfolyosu</h1>
    <p>CloudDev v11 Canlı Tasarım Mimarisi ile oluşturuldu.</p>
  </div>
</body>
</html>"""

MUSIC_TEMPLATE = """<!DOCTYPE html>
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
</html>"""

# V10'daki varsayılan e-ticaret şablonu
DEFAULT_ECOMMERCE = """<!DOCTYPE html>
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
</html>"""

# Ana Arayüz (HTML / CSS / JS)
IDE_INTERFACE = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudDev Studio v11 Step-by-Step</title>
    <style>
        :root {{
            --bg-main: #08090c;
            --bg-panel: #11131c;
            --accent: #38bdf8;
            --text: #f8fafc;
            --text-dim: #64748b;
            --border: #1e2937;
        }}
        body {{ 
            margin: 0; font-family: system-ui, sans-serif; 
            background: var(--bg-main); color: var(--text);
            display: flex; flex-direction: column; min-height: 100vh;
        }}
        header {{ 
            background: var(--bg-panel); padding: 14px 20px; 
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border);
        }}
        header h3 {{ margin: 0; background: linear-gradient(to right, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .tab-bar {{ display: flex; background: #0b0c12; border-bottom: 1px solid var(--border); }}
        .tab-btn {{ background: none; border: none; color: var(--text-dim); padding: 14px 22px; font-size: 13px; font-weight: 600; cursor: pointer; }}
        .tab-btn.active {{ color: var(--text); border-bottom: 2px solid var(--accent); background: var(--bg-panel); }}
        .tab-content {{ display: none; padding: 16px; flex: 1; flex-direction: column; gap: 16px; box-sizing: border-box; }}
        .tab-content.active {{ display: flex; }}
        .editor-container {{ background: #0d0f17; border: 1px solid var(--border); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }}
        .editor-header {{ background: #161926; padding: 10px 16px; font-size: 12px; color: var(--text-dim); border-bottom: 1px solid var(--border); }}
        .editor-body {{ display: flex; height: 300px; }}
        textarea {{ flex: 1; background: transparent; color: #e2e8f0; border: none; padding: 16px; resize: none; outline: none; font-family: monospace; font-size: 14px; }}
        .preview-wrapper {{ border-radius: 10px; overflow: hidden; border: 1px solid var(--border); background: #fff; }}
        iframe {{ width: 100%; height: 300px; border: none; background: white; }}
        .template-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }}
        .template-item {{ background: #161926; border: 1px solid var(--border); border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }}
        button.action-id {{ background: var(--accent); color: #090d16; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>

<header>
    <h3>☁️ CloudDev Studio v11</h3>
    <button class="action-id" onclick="liveRender()">⚡ Çalıştır</button>
</header>

<div class="tab-bar">
    <button id="btn-editor" class="tab-btn active" onclick="switchTab('editor-tab')">📝 Düzenleyici</button>
    <button id="btn-templates" class="tab-btn" onclick="switchTab('templates-tab')">🗂 Şablonlar</button>
</div>

<div id="editor-tab" class="tab-content active">
    <div class="editor-container">
        <div class="editor-header">index.html</div>
        <div class="editor-body">
            <textarea id="codeEditor" oninput="liveRender()" placeholder="Kodlarınızı yazın..."></textarea>
        </div>
    </div>
    <div class="preview-wrapper">
        <iframe id="previewFrame"></iframe>
    </div>
</div>

<div id="templates-tab" class="tab-content">
    <div class="template-grid">
        <div class="template-item">
            <h4>💼 Premium Portfolyo</h4>
            <p style="font-size:12px; color:var(--text-dim);">Kişisel marka ve projeleriniz için modern görünüm.</p>
            <button class="action-id" onclick="loadTemplate('portfolio')">Yükle</button>
        </div>
        <div class="template-item">
            <h4>🛒 E-Ticaret Kartı</h4>
            <p style="font-size:12px; color:var(--text-dim);">Etkileşimli buton ve minimalist ürün kartı.</p>
            <button class="action-id" onclick="loadTemplate('ecommerce')">Yükle</button>
        </div>
        <div class="template-item">
            <h4>🎵 Kozmik Müzik Çalar</h4>
            <p style="font-size:12px; color:var(--text-dim);">Şık çalma listesi alanıyla modern UI tasarımı.</p>
            <button class="action-id" onclick="loadTemplate('music')">Yükle</button>
        </div>
    </div>
</div>

<script>
    const editor = document.getElementById('codeEditor');
    const previewFrame = document.getElementById('previewFrame');

    // Python tarafındaki şablon verilerini JS'e güvenli şekilde aktarıyoruz
    const templates = {{
        portfolio: `{PORTFOLIO_TEMPLATE}`,
        ecommerce: `{DEFAULT_ECOMMERCE}`,
        music: `{MUSIC_TEMPLATE}`
    }};

    window.onload = function() {{
        editor.value = templates.ecommerce;
        liveRender();
    }};

    function liveRender() {{
        try {{
            previewFrame.srcdoc = editor.value;
        }} catch(e) {{
            console.log("Önizleme hatası.");
        }}
    }}

    function switchTab(tabId) {{
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        
        if(tabId === 'editor-tab') document.getElementById('btn-editor').classList.add('active');
        if(tabId === 'templates-tab') document.getElementById('btn-templates').classList.add('active');
    }}

    function loadTemplate(key) {{
        if(confirm("Mevcut kodlarınız silinecektir. Devam edilsin mi?")) {{
            editor.value = templates[key];
            liveRender();
            switchTab('editor-tab');
        }}
    }}
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(IDE_INTERFACE)

if __name__ == '__main__':
    # Render port yönetimi ve lokal test uyumluluğu
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
