from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

class Patient(db.Model):
    __tablename__ = 'patient'  # 明确指定表名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bed_status = db.relationship('BedStatus', backref='patient', uselist=False)
    chat_history = db.relationship('ChatHistory', backref='patient', lazy=True)

class BedStatus(db.Model):
    __tablename__ = 'bed_status'  # 明确指定表名
    id = db.Column(db.Integer, primary_key=True)
    bed_number = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    occupied = db.Column(db.Boolean, default=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'  # 明确指定表名
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_patient = db.Column(db.Boolean, default=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))