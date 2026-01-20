from flask_login import UserMixin
from datetime import datetime
from config import db
from typing import Optional

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('CropPrediction', backref='user', lazy=True)
    irrigation_schedules = db.relationship('IrrigationSchedule', backref='user', lazy=True)
    fertilizer_recommendations = db.relationship('FertilizerRecommendation', backref='user', lazy=True)
    
    def __init__(self, username: str, email: str, password_hash: str, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email
        self.password_hash = password_hash

class CropPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    predicted_crop = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id: int, nitrogen: float, phosphorus: float, potassium: float,
                 temperature: float, humidity: float, ph: float, rainfall: float,
                 predicted_crop: str, confidence: float, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.temperature = temperature
        self.humidity = humidity
        self.ph = ph
        self.rainfall = rainfall
        self.predicted_crop = predicted_crop
        self.confidence = confidence

class IrrigationSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)
    soil_type = db.Column(db.String(50), nullable=False)
    area = db.Column(db.Float, nullable=False)
    schedule_date = db.Column(db.DateTime, nullable=False)
    water_amount = db.Column(db.Float, nullable=False)  # in liters
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id: int, crop_type: str, soil_type: str, area: float,
                 schedule_date: datetime, water_amount: float, duration: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.crop_type = crop_type
        self.soil_type = soil_type
        self.area = area
        self.schedule_date = schedule_date
        self.water_amount = water_amount
        self.duration = duration

class FertilizerRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_type = db.Column(db.String(50), nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(50), nullable=False)
    fertilizer_name = db.Column(db.String(100), nullable=False)
    npk_ratio = db.Column(db.String(20), nullable=False)
    application_rate = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id: int, crop_type: str, nitrogen: float, phosphorus: float,
                 potassium: float, soil_type: str, fertilizer_name: str, npk_ratio: str,
                 application_rate: str, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.crop_type = crop_type
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.soil_type = soil_type
        self.fertilizer_name = fertilizer_name
        self.npk_ratio = npk_ratio
        self.application_rate = application_rate
