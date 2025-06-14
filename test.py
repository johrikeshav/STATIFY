import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split # Still good practice for real data
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --- 1. Define Your Data (as per your description) ---

# Your training inputs: 50 samples, each with 7 features (inputs)
# This is a list of lists.
# For demonstration, we'll create realistic-looking dummy data.
# In a real scenario, you would populate these lists with your actual data.
model_training_data = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
    [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
    [1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1],
    [2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8],
    [2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5],
    [3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2],
    [4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9],
    [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6],
    [5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3],
    [6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0],
    [7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7],
    [7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4],
    [8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1],
    [9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8],
    [9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5],
    [10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2],
    [11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9],
    [12.0, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6],
    [12.7, 12.8, 12.9, 13.0, 13.1, 13.2, 13.3],
    [13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14.0],
    [14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7],
    [14.8, 14.9, 15.0, 15.1, 15.2, 15.3, 15.4],
    [15.5, 15.6, 15.7, 15.8, 15.9, 16.0, 16.1],
    [16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 16.8],
    [16.9, 17.0, 17.1, 17.2, 17.3, 17.4, 17.5],
    [17.6, 17.7, 17.8, 17.9, 18.0, 18.1, 18.2],
    [18.3, 18.4, 18.5, 18.6, 18.7, 18.8, 18.9],
    [19.0, 19.1, 19.2, 19.3, 19.4, 19.5, 19.6],
    [19.7, 19.8, 19.9, 20.0, 20.1, 20.2, 20.3],
    [20.4, 20.5, 20.6, 20.7, 20.8, 20.9, 21.0],
    [21.1, 21.2, 21.3, 21.4, 21.5, 21.6, 21.7],
    [21.8, 21.9, 22.0, 22.1, 22.2, 22.3, 22.4],
    [22.5, 22.6, 22.7, 22.8, 22.9, 23.0, 23.1],
    [23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 23.8],
    [23.9, 24.0, 24.1, 24.2, 24.3, 24.4, 24.5],
    [24.6, 24.7, 24.8, 24.9, 25.0, 25.1, 25.2],
    [25.3, 25.4, 25.5, 25.6, 25.7, 25.8, 25.9],
    [26.0, 26.1, 26.2, 26.3, 26.4, 26.5, 26.6],
    [26.7, 26.8, 26.9, 27.0, 27.1, 27.2, 27.3],
    [27.4, 27.5, 27.6, 27.7, 27.8, 27.9, 28.0],
    [28.1, 28.2, 28.3, 28.4, 28.5, 28.6, 28.7],
    [28.8, 28.9, 29.0, 29.1, 29.2, 29.3, 29.4],
    [29.5, 29.6, 29.7, 29.8, 29.9, 30.0, 30.1],
    [30.2, 30.3, 30.4, 30.5, 30.6, 30.7, 30.8],
    [30.9, 31.0, 31.1, 31.2, 31.3, 31.4, 31.5],
    [31.6, 31.7, 31.8, 31.9, 32.0, 32.1, 32.2],
    [32.3, 32.4, 32.5, 32.6, 32.7, 32.8, 32.9],
    [33.0, 33.1, 33.2, 33.3, 33.4, 33.5, 33.6],
    [33.7, 33.8, 33.9, 34.0, 34.1, 34.2, 34.3],
    [34.4, 34.5, 34.6, 34.7, 34.8, 34.9, 35.0]
]

# Corresponding outputs for training, a list of 50 values between 0 and 100
# For demonstration, we'll make them somewhat correlated with the input data, plus noise.
scores = [
    5.2, 8.5, 12.1, 15.3, 18.7, 22.0, 25.5, 28.9, 32.2, 35.7,
    39.0, 42.4, 45.8, 49.1, 52.6, 55.9, 59.3, 62.7, 66.0, 69.5,
    72.8, 76.2, 79.6, 82.9, 86.4, 89.7, 93.1, 96.5, 99.8, 103.3, # Values can exceed 100 for linear regression if not capped
    106.6, 110.0, 113.4, 116.7, 120.2, 123.5, 126.9, 130.3, 133.6, 137.1,
    140.4, 143.8, 147.2, 150.5, 154.0, 157.3, 160.7, 164.1, 167.4, 170.9
]

# The new input for which you want to generate a value
# This is a single list of 7 values.
new_model_input = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]

print("--- Data Defined ---")
print(f"Number of training samples: {len(model_training_data)}")
print(f"Number of features per sample: {len(model_training_data[0])}")
print(f"Number of scores: {len(scores)}")
print(f"New model input: {new_model_input}\n")

# --- 2. Convert Data to NumPy Arrays ---
# Scikit-learn works best with NumPy arrays.

# Convert model_training_data to a NumPy array (n_samples, n_features)
X_train_np = np.array(model_training_data)

# Convert scores to a NumPy array (n_samples,) or (n_samples, 1)
# Using .reshape(-1, 1) ensures it's a 2D array with 1 column, which is good practice
# though for y, a 1D array is often accepted by scikit-learn.
y_train_np = np.array(scores).reshape(-1, 1)

# Convert the new_model_input to a NumPy array and reshape it for prediction
# It needs to be a 2D array (1, n_features) because predict expects multiple samples
# even if you're only predicting for one.
new_model_input_np = np.array(new_model_input).reshape(1, -1)

print("--- Data Converted to NumPy Arrays ---")
print(f"Shape of X_train_np: {X_train_np.shape}")
print(f"Shape of y_train_np: {y_train_np.shape}")
print(f"Shape of new_model_input_np for prediction: {new_model_input_np.shape}\n")

# --- 3. Initialize and Train the Linear Regression Model ---

# Create an instance of the LinearRegression model
model = LinearRegression()

# Train the model using your training data
model.fit(X_train_np, y_train_np)

print("--- Model Training Complete ---")
# You can inspect the learned coefficients and intercept
# Note: For multiple features, coef_ will be an array of coefficients
print(f"Model coefficients: {model.coef_}")
print(f"Model intercept: {model.intercept_}\n")

# --- 4. Generate a Prediction for the new_model_input ---

# Use the trained model to predict the output for your new_model_input
predicted_value_raw = model.predict(new_model_input_np)

# The prediction will be a NumPy array, even for a single value.
# We extract the scalar value for easier use.
# It will be a 2D array, so we take the first element of the first (and only) row.
predicted_value = predicted_value_raw[0][0]

# --- 5. Cap the predicted value between 0 and 100 (as per your requirement) ---
# Linear Regression can predict values outside the training range.
# If you need the output strictly between 0 and 100, you need to cap it.
final_predicted_output = max(0, min(100, predicted_value))

# --- 6. Store the Output ---
# You can store this value in a variable, add it to a list, save to a file, etc.
# For this example, we'll just store it in a variable and print it.
stored_output = final_predicted_output

print("--- Prediction Generated ---")
print(f"Raw Predicted Value for {new_model_input}: {predicted_value:.2f}")
print(f"Final Predicted Output (capped between 0 and 100): {final_predicted_output:.2f}")
print(f"The output is stored in the 'stored_output' variable: {stored_output:.2f}\n")

# --- Optional: Evaluate the model on training data (since you don't have a test set explicitly) ---
# In a real scenario, it's highly recommended to split your data into
# training and testing sets to get an unbiased evaluation of performance on unseen data.
# However, if you only have 50 samples and need to use all for training,
# you can evaluate on the training data, but be aware this may overstate performance.

# Predictions on the training data itself
y_train_pred = model.predict(X_train_np)

mae = mean_absolute_error(y_train_np, y_train_pred)
mse = mean_squared_error(y_train_np, y_train_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_train_np, y_train_pred)

print("--- Model Evaluation on Training Data (for reference) ---")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R2): {r2:.2f}")

# Example of how you might further use the stored_output:
# results_log = []
# results_log.append({"input": new_model_input, "predicted_score": stored_output})
# print(results_log)
