import numpy as np
import pandas as pd
from keras import Sequential
from keras.src.layers import LSTM, Dropout, Dense
from keras.src.optimizers import Adam
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso, Ridge, ElasticNet



# def train_models(historical_data):
#
#     # Calculate Q1 (25th percentile) and Q3 (75th percentile)
#     Q1 = historical_data['reach'].quantile(0.25)
#     Q3 = historical_data['reach'].quantile(0.75)
#     IQR = Q3 - Q1
#
#     # Define outliers
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#
#     # Remove outliers
#     cleaned_data = historical_data[(historical_data['reach'] >= lower_bound) & (historical_data['reach'] <= upper_bound)]
#
#
#     # Prepare the feature matrix and target vectors
#     X = cleaned_data[['user_influence', 'network', 'metric_type', 'metric_value', 'readability', 'multimedia_presence']]
#     y_reach = cleaned_data['reach']
#     y_longevity = cleaned_data['longevity']
#
#     # Split the data into training and testing sets
#     X_train, X_test, y_reach_train, y_reach_test = train_test_split(X, y_reach, test_size=0.2, random_state=42)
#     _, _, y_longevity_train, y_longevity_test = train_test_split(X, y_longevity, test_size=0.2, random_state=42)
#
#     # Train reach prediction model
#     reach_model = Pipeline([
#         ('scaler', StandardScaler()),
#         ('regressor', RandomForestRegressor())
#     ])
#     reach_model.fit(X_train, y_reach_train)
#
#     # Train longevity prediction model
#     longevity_model = Pipeline([
#         ('scaler', StandardScaler()),
#         ('regressor', RandomForestRegressor())
#     ])
#     longevity_model.fit(X_train, y_longevity_train)
#
#     # Predict on test data
#     y_reach_pred = reach_model.predict(X_test)
#     y_longevity_pred = longevity_model.predict(X_test)
#
#     # Calculate validation metrics
#     reach_mape = mean_absolute_percentage_error(y_reach_test, y_reach_pred)
#     reach_rmse = np.sqrt(mean_squared_error(y_reach_test, y_reach_pred))
#     longevity_mape = mean_absolute_percentage_error(y_longevity_test, y_longevity_pred)
#     longevity_rmse = np.sqrt(mean_squared_error(y_longevity_test, y_longevity_pred))
#
#     # Print validation metrics
#     print(f"Reach Model - MAPE: {reach_mape:.4f}, RMSE: {reach_rmse:.4f}")
#     print(f"Longevity Model - MAPE: {longevity_mape:.4f}, RMSE: {longevity_rmse:.4f}")
#
#     return reach_model, longevity_model, X_test, y_reach_test, y_longevity_test

def preprocess_data_for_lstm(data, time_steps):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(len(scaled_data) - time_steps):
        X.append(scaled_data[i:(i + time_steps), :-2])
        y.append(scaled_data[i + time_steps, -2:])  # Assuming last two columns are targets (reach and longevity)

    X = np.array(X)
    y = np.array(y)

    return X, y, scaler


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(2))  # Assuming two outputs: reach and longevity

    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model
def train_models(historical_data):
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = historical_data['reach'].quantile(0.25)
    Q3 = historical_data['reach'].quantile(0.75)
    IQR = Q3 - Q1

    # Define outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    cleaned_data = historical_data[(historical_data['reach'] >= lower_bound) & (historical_data['reach'] <= upper_bound)]

    # Prepare the feature matrix and target vectors
    X = cleaned_data[['user_influence', 'network', 'metric_type', 'metric_value', 'readability', 'multimedia_presence']]
    y_reach = cleaned_data['reach']
    y_longevity = cleaned_data['longevity']

    # Combine X and y for LSTM preprocessing
    combined_data = pd.concat([X, y_reach, y_longevity], axis=1).values

    # Split the data into training and testing sets
    X_train, X_test, y_reach_train, y_reach_test = train_test_split(X, y_reach, test_size=0.2, random_state=42)
    _, _, y_longevity_train, y_longevity_test = train_test_split(X, y_longevity, test_size=0.2, random_state=42)

    # Define models
    models = {
        "RandomForest": RandomForestRegressor(),
        "SVR": SVR(),
        "GradientBoosting": GradientBoostingRegressor(),
        "XGBoost": XGBRegressor(),
        "Lasso": Lasso(),
        "Ridge": Ridge(),
        "ElasticNet": ElasticNet()
    }

    # Function to train and evaluate a model
    def train_and_evaluate(model, X_train, y_train, X_test, y_test):
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', model)
        ])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        return pipeline, mape, rmse

    results = {}

    # Train and evaluate models for reach prediction
    for name, model in models.items():
        reach_model, reach_mape, reach_rmse = train_and_evaluate(model, X_train, y_reach_train, X_test, y_reach_test)
        longevity_model, longevity_mape, longevity_rmse = train_and_evaluate(model, X_train, y_longevity_train, X_test, y_longevity_test)

        results[name] = {
            "reach_model": reach_model,
            "reach_mape": reach_mape,
            "reach_rmse": reach_rmse,
            "longevity_model": longevity_model,
            "longevity_mape": longevity_mape,
            "longevity_rmse": longevity_rmse
        }

        # Print validation metrics
        print(f"{name} Reach Model - MAPE: {reach_mape:.4f}, RMSE: {reach_rmse:.4f}")
        print(f"{name} Longevity Model - MAPE: {longevity_mape:.4f}, RMSE: {longevity_rmse:.4f}")

    time_steps = 10
    X_lstm, y_lstm, scaler = preprocess_data_for_lstm(combined_data, time_steps)

    # Split LSTM data into training and testing sets
    X_lstm_train, X_lstm_test, y_lstm_train, y_lstm_test = train_test_split(X_lstm, y_lstm, test_size=0.2, random_state=42)

    # Build and train LSTM model
    lstm_model = build_lstm_model((X_lstm_train.shape[1], X_lstm_train.shape[2]))
    lstm_model.fit(X_lstm_train, y_lstm_train, epochs=50, batch_size=32, validation_split=0.2)

    # Predict with LSTM model
    y_lstm_pred = lstm_model.predict(X_lstm_test)

    # Calculate validation metrics for LSTM model
    lstm_mape = mean_absolute_percentage_error(y_lstm_test, y_lstm_pred)
    lstm_rmse = np.sqrt(mean_squared_error(y_lstm_test, y_lstm_pred))

    results["LSTM"] = {
        "lstm_model": lstm_model,
        "lstm_mape": lstm_mape,
        "lstm_rmse": lstm_rmse
    }

    # Print LSTM validation metrics
    print(f"LSTM Model - MAPE: {lstm_mape:.4f}, RMSE: {lstm_rmse:.4f}")

    return results, X_test, y_reach_test, y_longevity_test


# Example usage with historical_data DataFrame
# reach_model, longevity_model, X_test, y_reach_test, y_longevity_test = train_models(historical_data)


historical_data = pd.read_csv('last.csv')
print("historical data loaded")
# reach_model, longevity_model = train_models(historical_data)
reach_model, longevity_model, X_test, y_reach_test, y_longevity_test = train_models(historical_data)
print("models trained")
print(reach_model)
