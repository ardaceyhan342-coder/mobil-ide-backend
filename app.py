@app.route('/api/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    device_id = data.get('device_id')
    user = User.query.filter_by(device_id=device_id).first()

    # Kullanıcı kayıtlı mı ve Pro mu kontrolü
    if not user or not user.is_pro:
        return jsonify({"status": "error", "message": "Bu özellik için Pro abonelik gereklidir."}), 403

    # ... Buraya Hugging Face API kodlarını ekle ...
    
