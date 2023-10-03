import pandas as pd
from prophet import Prophet

def make_forecast(dataframe, product, days_to_forecast):
    product_df = dataframe[product]
    product_df.index = pd.to_datetime(product_df.index)
    product_df = product_df.reset_index()
    product_df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(product_df)
    future = model.make_future_dataframe(periods=days_to_forecast)
    forecast = model.predict(future)
    forecast_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(days_to_forecast)
    forecast_values['yhat'] = forecast_values['yhat'].astype(int)
    forecast_values['yhat_lower'] = forecast_values['yhat_lower'].astype(int)
    forecast_values['yhat_upper'] = forecast_values['yhat_upper'].astype(int)
    forecast_values.set_index('ds', inplace=True)
    forecast_values.columns = ['Forecast', 'Lower Limit', 'Optimal Forecast']


    return forecast_values