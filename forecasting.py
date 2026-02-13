"""
Revenue Forecasting
Simple time series forecasting methods
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class SimpleForecaster:
    """Simple forecasting using moving averages and trends"""
    
    def __init__(self, data):
        self.df = data.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
    
    def prepare_monthly_data(self):
        """Prepare monthly aggregated data"""
        
        monthly = self.df.groupby(self.df['date'].dt.to_period('M')).agg({
            'revenue': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        monthly['date'] = monthly['date'].dt.to_timestamp()
        monthly = monthly.sort_values('date')
        
        return monthly
    
    def moving_average_forecast(self, periods=6, window=3):
        """
        Simple moving average forecast
        Uses last N months to predict next M months
        """
        
        monthly_data = self.prepare_monthly_data()
        
        # Calculate moving average
        monthly_data['revenue_ma'] = monthly_data['revenue'].rolling(window=window).mean()
        
        # Use last MA value for forecasts
        last_ma = monthly_data['revenue_ma'].iloc[-1]
        
        # Generate future dates
        last_date = monthly_data['date'].iloc[-1]
        future_dates = [last_date + timedelta(days=30*i) for i in range(1, periods+1)]
        
        # Simple forecast: use moving average with slight trend
        # Calculate recent trend
        recent_data = monthly_data.tail(6)
        trend = (recent_data['revenue'].iloc[-1] - recent_data['revenue'].iloc[0]) / 6
        
        forecasts = []
        for i in range(periods):
            forecast_value = last_ma + (trend * i)
            forecasts.append(forecast_value)
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'forecasted_revenue': forecasts
        })
        
        return forecast_df
    
    def trend_based_forecast(self, periods=6):
        """
        Simple linear trend forecast
        Fits a basic trend line and projects forward
        """
        
        monthly_data = self.prepare_monthly_data()
        
        # Calculate simple trend (slope)
        x = np.arange(len(monthly_data))
        y = monthly_data['revenue'].values
        
        # Simple linear regression (manual calculation)
        x_mean = x.mean()
        y_mean = y.mean()
        
        numerator = ((x - x_mean) * (y - y_mean)).sum()
        denominator = ((x - x_mean) ** 2).sum()
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Generate forecasts
        last_date = monthly_data['date'].iloc[-1]
        future_dates = [last_date + timedelta(days=30*i) for i in range(1, periods+1)]
        
        future_x = np.arange(len(monthly_data), len(monthly_data) + periods)
        forecasted_revenue = slope * future_x + intercept
        
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'forecasted_revenue': forecasted_revenue
        })
        
        return forecast_df
    
    def calculate_forecast_accuracy(self, test_months=3):
        """
        Calculate forecast accuracy using last N months as test
        Returns MAPE (Mean Absolute Percentage Error)
        """
        
        monthly_data = self.prepare_monthly_data()
        
        if len(monthly_data) < test_months + 6:
            return None
        
        # Split data
        train_data = monthly_data.iloc[:-test_months]
        test_data = monthly_data.iloc[-test_months:]
        
        # Use train data to forecast
        # Simple approach: use average of last 3 months
        forecasts = []
        for i in range(test_months):
            last_3_avg = train_data['revenue'].tail(3).mean()
            forecasts.append(last_3_avg)
        
        actual = test_data['revenue'].values
        predicted = np.array(forecasts)
        
        # Calculate MAPE
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        
        # Calculate other metrics
        mae = np.mean(np.abs(actual - predicted))
        
        return {
            'mape': round(mape, 2),
            'mae': round(mae, 2),
            'actual': actual.tolist(),
            'predicted': predicted.tolist()
        }
    
    def combined_forecast(self, periods=6):
        """
        Combine moving average and trend forecasts
        Simple average of both methods
        """
        
        ma_forecast = self.moving_average_forecast(periods)
        trend_forecast = self.trend_based_forecast(periods)
        
        # Average the two forecasts
        combined = pd.DataFrame({
            'date': ma_forecast['date'],
            'ma_forecast': ma_forecast['forecasted_revenue'],
            'trend_forecast': trend_forecast['forecasted_revenue']
        })
        
        combined['final_forecast'] = (combined['ma_forecast'] + 
                                      combined['trend_forecast']) / 2
        
        return combined
    
    def seasonal_adjustment(self):
        """Simple seasonal pattern detection"""
        
        monthly_data = self.prepare_monthly_data()
        monthly_data['month'] = monthly_data['date'].dt.month
        
        # Calculate average revenue by month
        seasonal_avg = monthly_data.groupby('month')['revenue'].mean()
        
        overall_avg = monthly_data['revenue'].mean()
        
        # Calculate seasonal factors
        seasonal_factors = (seasonal_avg / overall_avg).round(2)
        
        return seasonal_factors.to_dict()
    
    def forecast_with_confidence(self, periods=6):
        """
        Generate forecast with simple confidence intervals
        Using standard deviation of historical data
        """
        
        forecast = self.combined_forecast(periods)
        monthly_data = self.prepare_monthly_data()
        
        # Calculate standard deviation of monthly revenue
        std_dev = monthly_data['revenue'].std()
        
        # Simple confidence intervals (±1.96 * std for 95% confidence)
        forecast['lower_bound'] = forecast['final_forecast'] - (1.96 * std_dev)
        forecast['upper_bound'] = forecast['final_forecast'] + (1.96 * std_dev)
        
        return forecast
