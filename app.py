"""
AgriSmart - AI-Powered Agricultural Management System

Copyright (c) 2024-2026 CSBS Team 10
Computer Science & Business Systems Department

Project Contributors: CSBS Team 10
All rights reserved.

This project is a collaborative effort by CSBS Team 10 for
educational and research purposes in smart agriculture.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import os

from config import app, db, login_manager
from models import User, CropPrediction, IrrigationSchedule, FertilizerRecommendation
from ml_models import CropPredictor, FertilizerRecommender, IrrigationScheduler

# Initialize ML models
crop_predictor = CropPredictor()
fertilizer_recommender = FertilizerRecommender()
irrigation_scheduler = IrrigationScheduler()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if not username or not email or not password:
            flash('All fields are required')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent activities
    recent_predictions = CropPrediction.query.filter_by(user_id=current_user.id).order_by(CropPrediction.created_at.desc()).limit(5).all()  # type: ignore
    irrigation_schedules = IrrigationSchedule.query.filter_by(user_id=current_user.id).order_by(IrrigationSchedule.schedule_date.desc()).limit(5).all()  # type: ignore
    fertilizer_recs = FertilizerRecommendation.query.filter_by(user_id=current_user.id).order_by(FertilizerRecommendation.created_at.desc()).limit(5).all()  # type: ignore
    
    return render_template('dashboard.html', 
                        predictions=recent_predictions,
                        schedules=irrigation_schedules,
                        recommendations=fertilizer_recs)

@app.route('/crop-prediction', methods=['GET', 'POST'])
@login_required
def crop_prediction():
    if request.method == 'POST':
        try:
            # Get form data
            nitrogen = float(request.form.get('nitrogen') or 0)
            phosphorus = float(request.form.get('phosphorus') or 0)
            potassium = float(request.form.get('potassium') or 0)
            temperature = float(request.form.get('temperature') or 0)
            humidity = float(request.form.get('humidity') or 0)
            ph = float(request.form.get('ph') or 0)
            rainfall = float(request.form.get('rainfall') or 0)
            
            # Predict crop
            prediction = crop_predictor.predict(nitrogen, phosphorus, potassium, 
                                            temperature, humidity, ph, rainfall)
            
            # Save prediction
            new_prediction = CropPrediction(
                user_id=current_user.id, # type: ignore
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                temperature=temperature,
                humidity=humidity,
                ph=ph,
                rainfall=rainfall,
                predicted_crop=prediction['crop'],
                confidence=prediction['confidence']
            )
            db.session.add(new_prediction)
            db.session.commit()
            
            return render_template('crop_prediction.html', prediction=prediction)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return render_template('crop_prediction.html')
    
    return render_template('crop_prediction.html')

@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
def fertilizer_recommendation():
    if request.method == 'POST':
        try:
            # Get form data
            crop_type = request.form.get('crop_type', '')
            nitrogen = float(request.form.get('nitrogen') or 0)
            phosphorus = float(request.form.get('phosphorus') or 0)
            potassium = float(request.form.get('potassium') or 0)
            soil_type = request.form.get('soil_type', '')
            ph = float(request.form.get('ph') or 0)
            soil_moisture = float(request.form.get('soil_moisture') or 0)
            
            # If crop_type not provided, infer crop from soil stats using XGBoost model
            if crop_type:
                recommendation = fertilizer_recommender.recommend(
                    crop_type, nitrogen, phosphorus, potassium, soil_type
                )
                recommendation['predicted_crop'] = crop_type
                recommendation['prediction_confidence'] = None
                recommendation['prediction_candidates'] = None
                recommendation['target_levels'] = None
            else:
                recommendation = fertilizer_recommender.recommend_from_soil(
                    nitrogen, phosphorus, potassium, ph, soil_moisture, soil_type
                )
                crop_type = recommendation['predicted_crop']
            
            # Save recommendation
            new_rec = FertilizerRecommendation(
                user_id=current_user.id,
                crop_type=crop_type,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                soil_type=soil_type,
                fertilizer_name=recommendation['fertilizer'],
                npk_ratio=recommendation['npk_ratio'],
                application_rate=recommendation['application_rate']
            )
            db.session.add(new_rec)
            db.session.commit()
            
            return render_template('fertilizer_recommendation.html', recommendation=recommendation)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return render_template('fertilizer_recommendation.html')
    
    return render_template('fertilizer_recommendation.html')

@app.route('/irrigation-scheduling', methods=['GET', 'POST'])
@login_required
def irrigation_scheduling():
    if request.method == 'POST':
        try:
            # Get form data
            crop_type = request.form.get('crop_type', '')
            soil_type = request.form.get('soil_type', '')
            area = float(request.form.get('area') or 0)
            temperature = float(request.form.get('temperature') or 0)
            humidity = float(request.form.get('humidity') or 0)
            
            # Get irrigation schedule
            schedule = irrigation_scheduler.create_schedule(
                crop_type, soil_type, area, temperature, humidity
            )
            
            # Save schedules
            for item in schedule['schedule']:
                new_schedule = IrrigationSchedule(
                    user_id=current_user.id,
                    crop_type=crop_type,
                    soil_type=soil_type,
                    area=area,
                    schedule_date=datetime.now() + timedelta(days=item['day']),
                    water_amount=item['water_amount'],
                    duration=item['duration']
                )
                db.session.add(new_schedule)
            db.session.commit()
            
            return render_template('irrigation_scheduling.html', schedule=schedule)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return render_template('irrigation_scheduling.html')
    
    return render_template('irrigation_scheduling.html')

@app.route('/api/crop-stats')
@login_required
def crop_stats():
    """API endpoint for dashboard visualizations"""
    predictions = CropPrediction.query.filter_by(user_id=current_user.id).all()
    
    crop_counts = {}
    for pred in predictions:
        crop = pred.predicted_crop
        crop_counts[crop] = crop_counts.get(crop, 0) + 1
    
    return jsonify({
        'labels': list(crop_counts.keys()),
        'data': list(crop_counts.values())
    })

@app.route('/api/irrigation-stats')
@login_required
def irrigation_stats():
    """API endpoint for irrigation statistics"""
    schedules = IrrigationSchedule.query.filter_by(user_id=current_user.id).order_by(IrrigationSchedule.schedule_date).all()  # type: ignore
    
    dates = [s.schedule_date.strftime('%Y-%m-%d') for s in schedules[:30]]
    water_amounts = [s.water_amount for s in schedules[:30]]
    
    return jsonify({
        'dates': dates,
        'water_amounts': water_amounts
    })

@app.route('/api/get-location', methods=['POST'])
def get_location():
    """API endpoint to handle geolocation data from frontend"""
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude and longitude:
            return jsonify({
                'success': True,
                'message': 'Location detected',
                'latitude': latitude,
                'longitude': longitude
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Location data missing'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/auto-fill-location', methods=['GET'])
@login_required
def auto_fill_location():
    """API endpoint to provide location auto-fill for forms"""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    
    if not latitude or not longitude:
        return jsonify({
            'success': False,
            'message': 'Location coordinates required'
        }), 400
    
    # Get user's location from IP (fallback if frontend geolocation fails)
    # This returns approximate location based on coordinates
    try:
        # Round coordinates to 2 decimal places for approximate location
        approx_lat = round(latitude, 2)
        approx_long = round(longitude, 2)
        
        return jsonify({
            'success': True,
            'latitude': latitude,
            'longitude': longitude,
            'approximate_location': f"Latitude: {approx_lat}, Longitude: {approx_long}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # For development only. Use a production WSGI server (e.g., Gunicorn) for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)
