import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Veritabanı modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True)
    is_pro = db.Column(db.Boolean, default=False)
    code_content = db.Column(db.Text)

# Bu satırı bir kere çalıştırıp veritabanını oluşturman lazım
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# API kısmını burada tanımla
@app.route('/api/save', methods=['POST'])
def save():
    # ... (save fonksiyonun buraya)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
    
