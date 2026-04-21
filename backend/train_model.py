"""
Train ML Model for Memory Prediction
This script trains a machine learning model on collected memory data
and saves the model metrics to the database.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from database import get_training_data, save_model_metrics
import joblib
import os

def train_memory_model():
    """
    Train a linear regression model to predict memory usage
    """
    print("=" * 60)
    print("🤖 TRAINING MEMORY PREDICTION MODEL")
    print("=" * 60)

    # Get training data from database
    data = get_training_data(500)
    if len(data) < 10:
        print(f"❌ Not enough training data! Only {len(data)} samples found.")
        print("Collect more data first by running the application.")
        return False

    print(f"✓ Loaded {len(data)} training samples from database")

    # Prepare features and target
    X = []  # Features: current_used, memory_percent
    y = []  # Target: predicted_memory

    for sample in data:
        X.append([sample['current_used_mb'], sample['memory_usage_percent']])
        y.append(sample['predicted_memory_mb'])

    X = np.array(X)
    y = np.array(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples")

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n📊 MODEL PERFORMANCE:")
    print(f"  MSE: {mse:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R² Score: {r2:.4f}")

    # Save model metrics to database
    if save_model_metrics("LinearRegression_Memory", r2, mse, rmse, len(X_train)):
        print("✓ Model metrics saved to database!")

        # Save model to file
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/memory_model.pkl")
        print("✓ Model saved to models/memory_model.pkl")

        return True
    else:
        print("❌ Failed to save model metrics!")
        return False

if __name__ == "__main__":
    train_memory_model()</content>
<parameter name="filePath">c:\Users\divib\OneDrive\Desktop\Sem4MiniPro\minipro\backend\train_model.py