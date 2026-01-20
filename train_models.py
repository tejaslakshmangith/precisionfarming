"""Utility to (re)train XGBoost models on project datasets."""
import os
from ml_models import CropPredictor, FertilizerCropClassifier


def main(force_retrain: bool = True):
    # Train crop recommendation model on Data/Crop_recommendation.csv
    crop_model = CropPredictor(force_retrain=force_retrain)
    print("Crop model trained. Classes:", list(crop_model.label_encoder.classes_))

    # Train fertilizer soil-to-crop model on Data/fertilizer.csv
    fert_model = FertilizerCropClassifier(force_retrain=force_retrain)
    print("Fertilizer model trained. Classes:", list(fert_model.label_encoder.classes_))

    # Model artifacts are stored under instance/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("Saved models in:", os.path.join(base_dir, "instance"))


if __name__ == "__main__":
    main(force_retrain=True)
