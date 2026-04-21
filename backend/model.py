"""
Memory Prediction Model
Uses trained ML model if available, otherwise falls back to rule-based prediction
"""

import os
import numpy as np
try:
    import joblib
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

def predict_memory(current_used, memory_percent):
    """
    Predict future memory usage using ML model or rule-based logic
    """

    # Try to use trained ML model first
    if ML_AVAILABLE and os.path.exists("models/memory_model.pkl"):
        try:
            model = joblib.load("models/memory_model.pkl")
            features = np.array([[current_used, memory_percent]])
            prediction = model.predict(features)[0]
            return max(prediction, current_used)  # Ensure prediction >= current
        except Exception as e:
            print(f"ML model prediction failed: {e}")
            # Fall back to rule-based

    # Rule-based prediction (fallback)
    if memory_percent < 50:
        growth_factor = 1.02   # stable
    elif memory_percent < 75:
        growth_factor = 1.08   # moderate growth
    else:
        growth_factor = 1.20   # high memory pressure

    predicted_memory = current_used * growth_factor
    return predicted_memory
