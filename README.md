# AgriSmart - AI-Powered Agricultural Management System

A comprehensive web-based agricultural management system that uses AI/ML algorithms to help farmers optimize crop productivity through intelligent crop prediction, fertilizer recommendations, and irrigation scheduling.

## Features

### 🌾 Crop Prediction
- Predicts the best crop for given soil and climate conditions
- Uses **XGBoost** machine learning algorithm
- Analyzes 7 parameters: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, and Rainfall
- Provides confidence scores and top 3 crop recommendations

### 🧪 Fertilizer Recommendation
- Recommends optimal fertilizers based on crop type and current NPK levels
- Calculates nutrient deficiencies
- Provides specific application rates
- Accounts for soil type variations

### 💧 Irrigation Scheduling
- Creates 30-day irrigation schedules
- Considers crop water requirements, soil type, and weather conditions
- Calculates water amounts and irrigation durations
- Visual charts for water usage tracking

### 📊 Dashboard & Visualization
- Beautiful, interactive dashboard with real-time statistics
- Chart.js visualizations for crop distribution and water usage
- Track all predictions, schedules, and recommendations
- User-friendly interface with responsive design

### 🔐 User Authentication
- Secure login and registration system
- User-specific data management
- Session-based authentication

## Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: XGBoost, scikit-learn
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Flask-Login
- **Data Processing**: NumPy, Pandas

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tejaslakshmangith/majorproject.git
cd majorproject
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application:
Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Register**: Create a new account
2. **Login**: Sign in with your credentials
3. **Dashboard**: View your statistics and recent activities
4. **Crop Prediction**: Enter soil and climate data to predict the best crop
5. **Fertilizer Recommendation**: Get personalized fertilizer recommendations
6. **Irrigation Scheduling**: Create smart irrigation schedules for your crops

## Project Structure

```
majorproject/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── ml_models.py           # Machine learning models (XGBoost)
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── crop_prediction.html
│   ├── fertilizer_recommendation.html
│   └── irrigation_scheduling.html
└── static/               # Static files (CSS, JS)
    └── css/
        └── style.css
```

## Machine Learning Model

The system uses **XGBoost** (eXtreme Gradient Boosting) algorithm for crop prediction:
- Multi-class classification with 23 crop types
- 100 estimators with max depth of 8
- Trained on synthetic data based on agronomic principles
- Achieves high accuracy with probability-based recommendations

## Features Highlights

- ✅ Login-based system with secure authentication
- ✅ AI/ML-powered crop prediction using XGBoost
- ✅ Intelligent fertilizer recommendations
- ✅ Smart irrigation scheduling
- ✅ Beautiful and responsive UI
- ✅ Interactive data visualizations
- ✅ Real-time dashboard with statistics
- ✅ Crop productivity enhancement insights

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Author

Created with ❤️ for enhancing agricultural productivity through AI/ML

---

**Note**: This system is designed to help farmers make data-driven decisions. Always consult with local agricultural experts for best results.