import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import pandas as pd


class CropPredictor:
    def __init__(self, data_path=None, model_path=None, force_retrain=False):
        self.model = None
        self.label_encoder = LabelEncoder()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = data_path or os.path.join(base_dir, 'Data', 'Crop_recommendation.csv')
        self.model_path = model_path or os.path.join(base_dir, 'instance', 'crop_xgb_model.joblib')
        self.feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.crops = [
            'rice',
            'wheat',
            'maize',
            'chickpea',
            'kidneybeans',
            'pigeonpeas',
            'mothbeans',
            'mungbean',
            'blackgram',
            'lentil',
            'pomegranate',
            'banana',
            'mango',
            'grapes',
            'watermelon',
            'muskmelon',
            'apple',
            'orange',
            'papaya',
            'coconut',
            'cotton',
            'jute',
            'coffee',
        ]

        self._load_or_train(force_retrain)

    def _load_or_train(self, force_retrain):
        if not force_retrain and os.path.exists(self.model_path):
            payload = joblib.load(self.model_path)
            self.model = payload['model']
            self.label_encoder.classes_ = payload['classes']
            return

        if os.path.exists(self.data_path):
            self._train_from_dataset()
        else:
            self._train_synthetic()

    def _train_from_dataset(self):
        df = pd.read_csv(self.data_path)
        df = df.drop(columns=[c for c in df.columns if c.lower().startswith('unnamed')], errors='ignore')
        df = df.dropna(subset=self.feature_columns + ['label'])
        df['label'] = df['label'].str.lower()

        X = df[self.feature_columns].astype(float)
        y = df['label']
        y_encoded = self.label_encoder.fit_transform(y)

        self.model = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective='multi:softprob',
            num_class=len(self.label_encoder.classes_),
            random_state=42,
        )
        self.model.fit(X, y_encoded)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({'model': self.model, 'classes': self.label_encoder.classes_}, self.model_path)

    def _train_synthetic(self):
        np.random.seed(42)
        n_samples = 2200

        N = np.random.uniform(0, 140, n_samples)
        P = np.random.uniform(5, 145, n_samples)
        K = np.random.uniform(5, 205, n_samples)
        temperature = np.random.uniform(8, 44, n_samples)
        humidity = np.random.uniform(14, 100, n_samples)
        ph = np.random.uniform(3.5, 9.5, n_samples)
        rainfall = np.random.uniform(20, 300, n_samples)

        X = np.column_stack([N, P, K, temperature, humidity, ph, rainfall])

        y = []
        for i in range(n_samples):
            crop_idx = self._determine_crop(
                N[i],
                P[i],
                K[i],
                temperature[i],
                humidity[i],
                ph[i],
                rainfall[i],
            )
            y.append(self.crops[crop_idx])

        y_encoded = self.label_encoder.fit_transform(y)

        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=8,
            learning_rate=0.1,
            random_state=42,
            objective='multi:softmax',
            num_class=len(self.crops),
        )
        self.model.fit(X, y_encoded)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({'model': self.model, 'classes': self.label_encoder.classes_}, self.model_path)

    def _determine_crop(self, n, p, k, temp, hum, ph, rain):
        """Rule-based crop determination for synthetic data."""
        if temp < 20 and rain > 100:
            return 1  # wheat
        if temp > 30 and rain > 200:
            return 0  # rice
        if 20 <= temp <= 30 and rain < 100:
            return 2  # maize
        if ph > 7 and temp > 25:
            return 11  # banana
        if n > 80 and k > 80:
            return 20  # cotton
        if temp > 28 and rain > 150:
            return 22  # coffee
        return np.random.randint(0, len(self.crops))

    def predict(self, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
        """Predict the best crop for given conditions."""
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

        prediction = self.model.predict(features)
        probabilities = self.model.predict_proba(features)[0]

        crop = self.label_encoder.inverse_transform(prediction)[0]
        confidence = float(max(probabilities)) * 100

        top_indices = np.argsort(probabilities)[-3:][::-1]
        recommendations = [
            {
                'crop': self.crops[idx],
                'probability': float(probabilities[idx]) * 100,
            }
            for idx in top_indices
        ]

        return {
            'crop': crop,
            'confidence': round(confidence, 2),
            'recommendations': recommendations,
        }


class FertilizerCropClassifier:
    """Train an XGBoost classifier on fertilizer.csv to map soil stats to crops."""

    def __init__(self, data_path=None, model_path=None, force_retrain=False):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = data_path or os.path.join(base_dir, 'Data', 'fertilizer.csv')
        self.model_path = model_path or os.path.join(base_dir, 'instance', 'fertilizer_xgb_model.joblib')
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = ['N', 'P', 'K', 'pH', 'soil_moisture']
        self.crop_stats = {}

        self._load_or_train(force_retrain)

    def _load_or_train(self, force_retrain):
        if not force_retrain and os.path.exists(self.model_path):
            payload = joblib.load(self.model_path)
            self.model = payload['model']
            self.label_encoder.classes_ = payload['classes']
            self.crop_stats = payload.get('crop_stats', {})
        else:
            if os.path.exists(self.data_path):
                self._train_from_dataset()
            else:
                self._train_synthetic()

    def _prepare_dataframe(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Fertilizer dataset not found at {self.data_path}")

        df = pd.read_csv(self.data_path)
        df = df.drop(columns=[c for c in df.columns if c.lower().startswith('unnamed')], errors='ignore')
        df = df.dropna(subset=['Crop'])
        df['Crop'] = df['Crop'].str.lower()
        missing_cols = [c for c in self.feature_columns if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Dataset missing required columns: {', '.join(missing_cols)}")

        return df

    def _train_from_dataset(self):
        df = self._prepare_dataframe()

        X = df[self.feature_columns].astype(float)
        y = df['Crop']
        y_encoded = self.label_encoder.fit_transform(y)

        self.model = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective='multi:softprob',
            num_class=len(self.label_encoder.classes_),
            random_state=42,
        )
        self.model.fit(X, y_encoded)

        grouped = df.groupby('Crop')[self.feature_columns].mean().round(2)
        self.crop_stats = grouped.to_dict(orient='index')

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(
            {
                'model': self.model,
                'classes': self.label_encoder.classes_,
                'crop_stats': self.crop_stats,
            },
            self.model_path,
        )

    def _train_synthetic(self):
        """Generate synthetic fertilizer data for training when CSV is not available."""
        np.random.seed(42)
        
        # Define crop types matching the crop predictor
        crops = [
            'rice', 'wheat', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
            'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
            'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
            'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
        ]
        
        # Generate synthetic data for each crop type
        n_samples_per_crop = 100
        data = []
        
        for crop in crops:
            # Generate realistic NPK values and soil parameters for each crop
            # These are approximate typical ranges
            if crop in ['rice', 'wheat', 'maize', 'sugarcane']:
                # High N requirement cereals
                N = np.random.uniform(80, 120, n_samples_per_crop)
                P = np.random.uniform(30, 60, n_samples_per_crop)
                K = np.random.uniform(30, 60, n_samples_per_crop)
                pH = np.random.uniform(5.5, 7.5, n_samples_per_crop)
                soil_moisture = np.random.uniform(60, 85, n_samples_per_crop)
            elif crop in ['cotton', 'jute']:
                # Fiber crops
                N = np.random.uniform(60, 100, n_samples_per_crop)
                P = np.random.uniform(30, 50, n_samples_per_crop)
                K = np.random.uniform(40, 70, n_samples_per_crop)
                pH = np.random.uniform(6.0, 7.5, n_samples_per_crop)
                soil_moisture = np.random.uniform(50, 75, n_samples_per_crop)
            elif crop in ['banana', 'mango', 'coconut', 'pomegranate']:
                # Fruit trees - high K requirement
                N = np.random.uniform(50, 90, n_samples_per_crop)
                P = np.random.uniform(25, 50, n_samples_per_crop)
                K = np.random.uniform(60, 100, n_samples_per_crop)
                pH = np.random.uniform(5.5, 7.0, n_samples_per_crop)
                soil_moisture = np.random.uniform(55, 80, n_samples_per_crop)
            elif crop in ['grapes', 'watermelon', 'muskmelon', 'orange', 'papaya', 'apple']:
                # Other fruits
                N = np.random.uniform(40, 80, n_samples_per_crop)
                P = np.random.uniform(20, 50, n_samples_per_crop)
                K = np.random.uniform(50, 90, n_samples_per_crop)
                pH = np.random.uniform(5.5, 7.5, n_samples_per_crop)
                soil_moisture = np.random.uniform(50, 80, n_samples_per_crop)
            elif crop in ['chickpea', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil']:
                # Legumes - lower N requirement (nitrogen fixing)
                N = np.random.uniform(20, 50, n_samples_per_crop)
                P = np.random.uniform(30, 60, n_samples_per_crop)
                K = np.random.uniform(20, 50, n_samples_per_crop)
                pH = np.random.uniform(6.0, 8.0, n_samples_per_crop)
                soil_moisture = np.random.uniform(45, 70, n_samples_per_crop)
            else:
                # Default for other crops
                N = np.random.uniform(40, 80, n_samples_per_crop)
                P = np.random.uniform(25, 55, n_samples_per_crop)
                K = np.random.uniform(30, 60, n_samples_per_crop)
                pH = np.random.uniform(5.5, 7.5, n_samples_per_crop)
                soil_moisture = np.random.uniform(50, 75, n_samples_per_crop)
            
            for i in range(n_samples_per_crop):
                data.append({
                    'Crop': crop,
                    'N': N[i],
                    'P': P[i],
                    'K': K[i],
                    'pH': pH[i],
                    'soil_moisture': soil_moisture[i]
                })
        
        df = pd.DataFrame(data)
        
        X = df[self.feature_columns].astype(float)
        y = df['Crop']
        y_encoded = self.label_encoder.fit_transform(y)

        self.model = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            objective='multi:softprob',
            num_class=len(self.label_encoder.classes_),
            random_state=42,
        )
        self.model.fit(X, y_encoded)

        grouped = df.groupby('Crop')[self.feature_columns].mean().round(2)
        self.crop_stats = grouped.to_dict(orient='index')

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(
            {
                'model': self.model,
                'classes': self.label_encoder.classes_,
                'crop_stats': self.crop_stats,
            },
            self.model_path,
        )

    def predict_crop(self, nitrogen, phosphorus, potassium, ph, soil_moisture):
        if self.model is None:
            self._load_or_train()

        features = np.array([[nitrogen, phosphorus, potassium, ph, soil_moisture]], dtype=float)
        probabilities = self.model.predict_proba(features)[0]

        top_indices = np.argsort(probabilities)[-3:][::-1]
        top = [
            {
                'crop': self.label_encoder.inverse_transform([idx])[0],
                'probability': round(float(probabilities[idx]) * 100, 2),
            }
            for idx in top_indices
        ]

        best_crop = top[0]['crop']
        confidence = top[0]['probability']

        return {
            'crop': best_crop,
            'confidence': confidence,
            'recommendations': top,
            'target_levels': self.crop_stats.get(best_crop, {}),
        }


class FertilizerRecommender:
    def __init__(self):
        self.crop_classifier = FertilizerCropClassifier()
        self.fertilizer_db = {
            'rice': {'N': 80, 'P': 40, 'K': 40, 'fertilizers': ['Urea', 'DAP', 'MOP']},
            'wheat': {'N': 120, 'P': 60, 'K': 40, 'fertilizers': ['Urea', 'DAP', 'MOP']},
            'maize': {'N': 100, 'P': 50, 'K': 50, 'fertilizers': ['Urea', 'SSP', 'MOP']},
            'cotton': {'N': 150, 'P': 75, 'K': 75, 'fertilizers': ['Urea', 'DAP', 'MOP']},
            'sugarcane': {'N': 200, 'P': 80, 'K': 80, 'fertilizers': ['Urea', 'SSP', 'MOP']},
            'banana': {'N': 200, 'P': 100, 'K': 200, 'fertilizers': ['Urea', 'SSP', 'MOP']},
            'mango': {'N': 100, 'P': 50, 'K': 100, 'fertilizers': ['Urea', 'SSP', 'MOP']},
            'potato': {'N': 120, 'P': 80, 'K': 120, 'fertilizers': ['Urea', 'DAP', 'MOP']},
            'tomato': {'N': 150, 'P': 100, 'K': 100, 'fertilizers': ['NPK Complex', 'DAP']},
        }

        for crop, stats in self.crop_classifier.crop_stats.items():
            base = self.fertilizer_db.get(crop, {})
            self.fertilizer_db[crop] = {
                'N': stats.get('N', base.get('N', 100)),
                'P': stats.get('P', base.get('P', 50)),
                'K': stats.get('K', base.get('K', 50)),
                'pH': stats.get('pH', base.get('pH')),
                'soil_moisture': stats.get('soil_moisture', base.get('soil_moisture')),
                'fertilizers': base.get('fertilizers', ['NPK Complex']),
            }

    def recommend(self, crop_type, current_n, current_p, current_k, soil_type):
        """Recommend fertilizer based on crop and current NPK levels."""
        crop_type = crop_type.lower()

        if crop_type in self.fertilizer_db:
            required = self.fertilizer_db[crop_type]
        else:
            required = {'N': 100, 'P': 50, 'K': 50, 'fertilizers': ['NPK Complex']}

        n_deficit = max(0, required['N'] - current_n)
        p_deficit = max(0, required['P'] - current_p)
        k_deficit = max(0, required['K'] - current_k)

        if n_deficit > p_deficit and n_deficit > k_deficit:
            fertilizer = 'Urea'
            npk_ratio = '46-0-0'
            rate = f"{n_deficit * 2} kg/hectare"
        elif p_deficit > k_deficit:
            fertilizer = 'DAP (Di-ammonium Phosphate)'
            npk_ratio = '18-46-0'
            rate = f"{p_deficit * 2.2} kg/hectare"
        elif k_deficit > 0:
            fertilizer = 'MOP (Muriate of Potash)'
            npk_ratio = '0-0-60'
            rate = f"{k_deficit * 1.7} kg/hectare"
        else:
            fertilizer = 'NPK Complex'
            npk_ratio = '19-19-19'
            rate = "50 kg/hectare (maintenance)"

        soil_factor = 1.0
        if soil_type.lower() == 'sandy':
            soil_factor = 1.2
        elif soil_type.lower() == 'clay':
            soil_factor = 0.9

        return {
            'fertilizer': fertilizer,
            'npk_ratio': npk_ratio,
            'application_rate': rate,
            'n_deficit': round(n_deficit, 2),
            'p_deficit': round(p_deficit, 2),
            'k_deficit': round(k_deficit, 2),
            'required_n': required['N'],
            'required_p': required['P'],
            'required_k': required['K'],
            'n_deficit_percent': int((n_deficit / required['N'] * 100) if required['N'] > 0 else 0),
            'p_deficit_percent': int((p_deficit / required['P'] * 100) if required['P'] > 0 else 0),
            'k_deficit_percent': int((k_deficit / required['K'] * 100) if required['K'] > 0 else 0),
            'soil_adjustment_factor': soil_factor,
            'target_ph': required.get('pH'),
            'target_soil_moisture': required.get('soil_moisture'),
        }

    def recommend_from_soil(self, nitrogen, phosphorus, potassium, ph, soil_moisture, soil_type):
        """Predict the likely crop from soil stats and return a fertilizer plan."""
        prediction = self.crop_classifier.predict_crop(nitrogen, phosphorus, potassium, ph, soil_moisture)
        crop_type = prediction['crop']
        recommendation = self.recommend(crop_type, nitrogen, phosphorus, potassium, soil_type)
        recommendation['predicted_crop'] = crop_type
        recommendation['prediction_confidence'] = prediction['confidence']
        recommendation['prediction_candidates'] = prediction['recommendations']
        recommendation['target_levels'] = prediction.get('target_levels', {})
        recommendation['input_soil'] = {
            'N': nitrogen,
            'P': phosphorus,
            'K': potassium,
            'pH': ph,
            'soil_moisture': soil_moisture,
        }
        return recommendation


class IrrigationScheduler:
    def __init__(self):
        self.crop_water_requirements = {
            'rice': {'daily': 8, 'frequency': 1},
            'wheat': {'daily': 5, 'frequency': 3},
            'maize': {'daily': 6, 'frequency': 2},
            'cotton': {'daily': 6.5, 'frequency': 3},
            'sugarcane': {'daily': 10, 'frequency': 2},
            'potato': {'daily': 5.5, 'frequency': 2},
            'tomato': {'daily': 5, 'frequency': 2},
            'banana': {'daily': 7, 'frequency': 2},
            'mango': {'daily': 4, 'frequency': 5},
        }

    def create_schedule(self, crop_type, soil_type, area, temperature, humidity):
        """Create irrigation schedule for next 30 days."""
        crop_type = crop_type.lower()

        if crop_type in self.crop_water_requirements:
            water_req = self.crop_water_requirements[crop_type]
        else:
            water_req = {'daily': 6, 'frequency': 3}

        temp_factor = 1 + (temperature - 25) * 0.02
        humidity_factor = 1 - (humidity - 60) * 0.005

        soil_factor = 1.0
        if soil_type.lower() == 'sandy':
            soil_factor = 1.3
        elif soil_type.lower() == 'clay':
            soil_factor = 0.8
        elif soil_type.lower() == 'loamy':
            soil_factor = 1.0

        base_water = water_req['daily'] * area * temp_factor * humidity_factor * soil_factor

        schedule = []
        for day in range(0, 30, water_req['frequency']):
            duration = int(base_water / 10)
            schedule.append(
                {
                    'day': day,
                    'date': f"Day {day}",
                    'water_amount': round(base_water, 2),
                    'duration': duration,
                }
            )

        total_water = sum(s['water_amount'] for s in schedule)

        return {
            'schedule': schedule,
            'total_water': round(total_water, 2),
            'frequency': water_req['frequency'],
            'crop_type': crop_type,
            'adjustments': {
                'temperature_factor': round(temp_factor, 2),
                'humidity_factor': round(humidity_factor, 2),
                'soil_factor': soil_factor,
            },
        }
