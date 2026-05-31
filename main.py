import os
import requests
import base64
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# Üstteki HTML dosyasını hatasız, kayma olmadan doğrudan okuyoruz
def load_interface():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h3>Hata: index.html dosyası main.py ile aynı klasörde bulunamadı!</h3>"

@app.route('/')
def index():
    return load_interface()

@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json or {}
    user_prompt = data.get('prompt', '')
    
    API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B-Instruct"
    
    system_instruction = (
        "Sen profesyonel bir frontend mimarısın. Sadece senden istenen kod mimarisini yaz. "
        "Açıklama, konuşma metni veya markdown sembolü (```) asla kullanma. "
        "Kodları tam olarak şu başlık etiketlerinin arasına ekle:\n"
        "===HTML===\n[HTML kodları]\n===CSS===\n[CSS kodları]\n===JS===\n[JS kodları]"
    )
    
    payload = {
        "inputs": f"<|im_start|>system\n{system_instruction}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {"max_new_tokens": 1600, "temperature": 0.2}
    }
    
    try:
        res = requests.post(API_URL, json=payload, timeout=25)
        if res.status_code == 200:
            raw_text = res.json()[0]['generated_text']
            generated_blocks = raw_text.split("<|im_start|>assistant\n")[-1].strip() if "<|im_start|>assistant\n" in raw_text else raw_text
            
            html_content, css_content, js_content = "", "", ""
            
            html_match = re.search(r'===HTML===(.*?)(===CSS===|===JS===|$)', generated_blocks, re.DOTALL)
            css_match = re.search(r'===CSS===(.*?)(===HTML===|===JS===|$)', generated_blocks, re.DOTALL)
            js_match = re.search(r'===JS===(.*?)(===HTML===|===CSS===|$)', generated_blocks, re.DOTALL)
            
            if html_match: html_content = html_match.group(1).strip()
            if css_match: css_content = css_match.group(1).strip()
            if js_match: js_content = js_match.group(1).strip()
            
            for term in ["```html", "```css", "```javascript", "```js", "```"]:
                html_content = html_content.replace(term, "")
                css_content = css_content.replace(term, "")
                js_content = js_content.replace(term, "")
                
            return jsonify({
                "status": "success", 
                "html": html_content.strip(), 
                "css": css_content.strip(), 
                "js": js_content.strip()
            })
        return jsonify({"status": "error", "message": f"Yapay zeka yanıt vermedi (Kod: {res.status_code})"})
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Zaman aşımı oluştu."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"İç Hata: {str(e)}"})

@app.route('/api/github-push-all', methods=['POST'])
def github_push_all():
    data = request.json or {}
    files = data.get('files')
    token = data.get('token')
    repo_name = data.get('repo')
    
    if not files or not token or not repo_name:
        return jsonify({"status": "error", "message": "Eksik veri gönderildi."})
        
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    try:
        user_res = requests.get("https://api.github.com/user", headers=headers, timeout=15)
        if user_res.status_code != 200:
            return jsonify({"status": "error", "message": "GitHub Token geçersiz!"})
            
        username = user_res.json()['login']
        requests.post("https://api.github.com/user/repos", headers=headers, json={"name": repo_name, "private": False, "auto_init": True}, timeout=15)

        for filename, content in [("index.html", files.get('html', '')), ("style.css", files.get('css', '')), ("script.js", files.get('js', ''))]:
            file_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{filename}"
            get_file = requests.get(file_url, headers=headers, timeout=15)
            sha = get_file.json()['sha'] if get_file.status_code == 200 else ""
            
            encoded_code = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            push_data = {"message": f"CloudDev Studio Deployment {filename}", "content": encoded_code}
            if sha: push_data["sha"] = sha
            requests.put(file_url, headers=headers, json=push_data, timeout=15)
            
        return jsonify({"status": "success", "message": "Tüm paket GitHub'a yüklendi!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Entegrasyon Hatası: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
