import pandas as pd
from prophet import Prophet

def make_forecast(dataframe, product, days_to_forecast):
    stock_index = 5 # number of days
    forecast_index = days_to_forecast + stock_index

    product_df = dataframe[product]
    product_df.index = pd.to_datetime(product_df.index)
    product_df = product_df.reset_index()
    product_df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(product_df)
    future = model.make_future_dataframe(periods=forecast_index)
    forecast = model.predict(future)
    forecast_values = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast_values['yhat'] = forecast_values['yhat'].astype(int)
    forecast_values['yhat_lower'] = forecast_values['yhat_lower'].astype(int)
    forecast_values['yhat_upper'] = forecast_values['yhat_upper'].astype(int)
    forecast_values['stock_amount'] = forecast_values['yhat'].rolling(stock_index).sum()
    forecast_values['stock_amount'] = forecast_values['stock_amount'].fillna(0).astype(int)
    forecast_values.set_index('ds', inplace=True)

    # remove stock_index
    forecast_values = forecast_values[-(days_to_forecast+stock_index):-stock_index]
    forecast_values.columns = ['Forecast', 'Lower Limit', 'Upper Limit', 'Stock Amount']


    return forecast_values