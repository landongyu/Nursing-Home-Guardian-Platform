from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, init_app

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    init_app(app)  # 初始化数据库
    
    from models import Patient, ChatHistory, BedStatus

    @app.route('/')
    def dashboard():
        print("访问了 dashboard 路由")
        return render_template('dashboard.html')

    @app.route('/api/bed-status')
    def get_bed_status():
        beds = BedStatus.query.all()
        print("获取床位状态，共有", len(beds), "条记录")
        return jsonify([{
            'bed_number': bed.bed_number,
            'temperature': bed.temperature,
            'humidity': bed.humidity,
            'occupied': bed.occupied,
            'patient_id': bed.patient_id,
            'patient_name': bed.patient.name if bed.patient else None
        } for bed in beds])

    @app.route('/api/chat-history/<int:patient_id>')
    def get_chat_history(patient_id):
        chats = ChatHistory.query.filter_by(patient_id=patient_id).order_by(ChatHistory.timestamp.desc()).limit(10)
        return jsonify([{
            'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message': chat.message,
            'is_patient': chat.is_patient
        } for chat in chats])

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)