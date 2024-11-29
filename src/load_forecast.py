from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from preprocess import load_and_preprocess_data

def validate_data(data):

    required_columns = ['Load (kW)', 'Timestamp']
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"Data must contain columns: {required_columns}")
    
    df = data.copy()
    
    df = df.dropna(subset=['Load (kW)', 'Timestamp'])
    
    df = df.sort_values('Timestamp')
    
    df = df.reset_index(drop=True)
    
    return df

def calculate_metrics(y_true, y_pred):

    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true = y_true[mask]
    y_pred = y_pred[mask]
    
    if len(y_true) == 0:
        raise ValueError("No valid pairs of true and predicted values found")
    
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_true - y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape
    }

def train_and_forecast(data):

    cleaned_data = validate_data(data)
    
    prophet_data = pd.DataFrame()
    prophet_data['ds'] = cleaned_data['Timestamp']
    prophet_data['y'] = cleaned_data['Load (kW)']
    
    print(prophet_data.head())
    
    train_size = int(0.8 * len(prophet_data))
    train_data = prophet_data[:train_size]
    test_data = prophet_data[train_size:]
    
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=True,
        interval_width=0.95
    )
    
    model.fit(train_data)

    future = model.make_future_dataframe(periods=48, freq='h')  
    
    forecast = model.predict(future)
    
    try:
        fig1 = model.plot(forecast)
        plt.title('Load Forecast')
        plt.savefig('/home/saiikishen/development/projects/ldc/outputs/forecast_plot.png')
        plt.close()
        
        fig2 = model.plot_components(forecast)
        plt.savefig('/home/saiikishen/development/projects/ldc/outputs/components_plot.png')
        plt.close()
        
    except Exception as e:
        print(f"Warning: Could not create plots: {str(e)}")

    try:
        merged = pd.merge(
            test_data,
            forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
            on='ds',
            how='left'
        )
        
        metrics = calculate_metrics(merged['y'], merged['yhat'])
        
        print("\nPerformance Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.2f}")
            
        merged.to_csv('/home/saiikishen/development/projects/ldc/outputs/detailed_results.csv', index=False)
        
    except Exception as e:
        print(f"\nWarning: Error calculating metrics: {str(e)}")
        metrics = None

    # Save forecast with only the Timestamp and predicted values (yhat)
    forecast_results = forecast[['ds', 'yhat']]
    forecast_results.columns = ['Timestamp', 'Predicted Load (kW)']
    forecast_results.to_csv('/home/saiikishen/development/projects/ldc/outputs/forecast_results.csv', index=False)
    print("\nForecast saved to forecast_results.csv")

    return forecast, metrics

def main():
    try:
        filepath = '/home/saiikishen/development/projects/ldc/data/load_data.xlsx'
        data = load_and_preprocess_data(filepath)
        
        forecast, metrics = train_and_forecast(data)
        
        # Forecast already saved in train_and_forecast
        print("\nForecast has been saved")
        
    except Exception as e:
        print(f"\nError in main execution: {str(e)}")
        raise

if __name__ == '__main__':
    main()
