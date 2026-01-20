# Installation and Usage Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/tejaslakshmangith/majorproject.git
cd majorproject
```

2. **Create and activate virtual environment**:
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Access the application**:
Open your web browser and navigate to: `http://localhost:5000`

## Features Overview

### 1. User Authentication
- **Register**: Create a new account with username, email, and password
- **Login**: Secure login with session management
- **Logout**: Safe logout functionality

### 2. Dashboard
- View all your agricultural activities in one place
- Interactive charts showing:
  - Crop distribution (pie chart)
  - Water usage trends (line chart)
- Recent predictions, irrigation schedules, and fertilizer recommendations

### 3. Crop Prediction (XGBoost AI)
**Input Parameters**:
- Nitrogen (N) - kg/ha (0-140)
- Phosphorus (P) - kg/ha (5-145)
- Potassium (K) - kg/ha (5-205)
- Temperature - °C (8-44)
- Humidity - % (14-100)
- Soil pH (3.5-9.5)
- Rainfall - mm (20-300)

**Output**:
- Best recommended crop
- Confidence percentage
- Top 3 alternative crop recommendations

**Supported Crops** (23 types):
Rice, Wheat, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee

### 4. Fertilizer Recommendation
**Input Parameters**:
- Crop Type (dropdown selection)
- Current Nitrogen (N) - kg/ha
- Current Phosphorus (P) - kg/ha
- Current Potassium (K) - kg/ha
- Soil Type (Sandy, Loamy, Clay, Black, Red)

**Output**:
- Recommended fertilizer name
- NPK ratio
- Application rate
- Nutrient deficit analysis
- Visual progress bars showing deficits

### 5. Irrigation Scheduling
**Input Parameters**:
- Crop Type (dropdown selection)
- Soil Type (Sandy, Loamy, Clay)
- Field Area - hectares
- Average Temperature - °C
- Humidity - %

**Output**:
- 30-day irrigation schedule
- Total water requirement
- Irrigation frequency
- Adjustment factors (temperature, humidity, soil)
- Day-by-day water amounts and durations
- Visual bar chart of water usage

## Testing the System

Run the test script to verify all features:
```bash
python test_features.py
```

This will test:
- User registration
- Crop prediction with XGBoost
- Fertilizer recommendations
- Irrigation scheduling

## Project Structure

```
majorproject/
├── app.py                          # Main Flask application
├── config.py                       # App configuration and database setup
├── models.py                       # Database models
├── ml_models.py                    # ML algorithms (XGBoost)
├── test_features.py                # Feature testing script
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── INSTALLATION.md                 # This file
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Dashboard
│   ├── crop_prediction.html       # Crop prediction page
│   ├── fertilizer_recommendation.html
│   └── irrigation_scheduling.html
└── static/                        # Static files
    └── css/
        └── style.css              # Custom CSS
```

## Database

The application uses SQLite database (`agriculture.db`) which is created automatically on first run.

**Tables**:
- `user` - User accounts
- `crop_prediction` - Crop prediction history
- `irrigation_schedule` - Irrigation schedules
- `fertilizer_recommendation` - Fertilizer recommendation history

## Technologies Used

- **Backend**: Flask 3.1+
- **ML Framework**: XGBoost 3.1+
- **Data Processing**: NumPy, Pandas, scikit-learn
- **Database**: SQLite with SQLAlchemy
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Flask-Login
- **Visualization**: Chart.js, Plotly

## Troubleshooting

### Issue: Dependencies not installing
**Solution**: Upgrade pip and setuptools
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete the database and restart
```bash
rm agriculture.db
python app.py
```

### Issue: Port 5000 already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

## Security Notes

⚠️ **Important**: Before deploying to production:
1. Change the `SECRET_KEY` in `config.py`
2. Set `debug=False` in `app.py`
3. Use a production WSGI server (e.g., Gunicorn)
4. Use environment variables for sensitive data
5. Use HTTPS

## Support

For issues or questions, please open an issue on GitHub.

## License

MIT License - See LICENSE file for details
