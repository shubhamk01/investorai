import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def prepare_data(df, feature_col='Close', look_back=60):
    data = df[feature_col].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])
        y.append(scaled_data[i, 0])
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler

def train_lstm(df, feature_col='Close', look_back=60, epochs=20, batch_size=32):
    X, y, scaler = prepare_data(df, feature_col, look_back)
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
    return model, scaler

def predict_trend(df, feature_col='Close', look_back=60):
    # Train the model on historical data
    model, scaler = train_lstm(df, feature_col, look_back)
    # Prepare the latest data for prediction
    data = df[feature_col].values.reshape(-1, 1)
    scaled_data = scaler.transform(data)
    last_sequence = scaled_data[-look_back:]
    X_pred = np.reshape(last_sequence, (1, look_back, 1))
    predicted_price = model.predict(X_pred)[0][0]
    predicted_price = scaler.inverse_transform([[predicted_price]])[0][0]
    last_price = df[feature_col].values[-1]
    # Simple logic: if predicted price > last price, uptrend; else downtrend
    if predicted_price > last_price:
        return 'uptrend'
    elif predicted_price < last_price:
        return 'downtrend'
    else:
        return 'neutral'
