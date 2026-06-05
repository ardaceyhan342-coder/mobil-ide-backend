import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# DATABASE_URL ortam değişkenini Render'dan alıyoruz
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(100), unique=True)
    is_pro = db.Column(db.Boolean, default=False)
    code_content = db.Column(db.Text)

# Veritabanı tablolarını oluştur (İlk çalışmada gereklidir)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    user = User.query.filter_by(device_id=data.get('device_id')).first()
    if not user:
        user = User(device_id=data.get('device_id'), code_content=data.get('code'))
        db.session.add(user)
    else:
        user.code_content = data.get('code')
    db.session.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run()
    
