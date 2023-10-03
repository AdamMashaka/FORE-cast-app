import streamlit as st
import pandas as pd

from utils.forecast import make_forecast


st.title("Forecast")
st.write("Welcome to the Forecast page! 📈")


try:
    pc_sums = pd.read_csv("data/processed/pc_sums.csv", index_col=0)
    uc_sums = pd.read_csv("data/processed/uc_sums.csv", index_col=0)

    st.sidebar.title("Forecast Options")
    st.sidebar.write("Select the type of forecast you want to make.")

    product_list = pc_sums.columns[1:-1].tolist()

    product = st.sidebar.selectbox("Select a Product", product_list)
    forecast_type = st.sidebar.selectbox("Select Forecast Type", ["Sum PC", "Sum UC"])

    # add a range slider to the sidebar for selecting the number of days to forecast
    days_to_forecast = st.sidebar.slider("Select the number of days to forecast", 1, 30)

    # add a button to the sidebar to make the forecast
    if st.sidebar.button("Make Forecast"):
        if product:
            if forecast_type:
                if days_to_forecast:
                    past_days = 90
                    try:
                        if forecast_type == "Sum PC":
                            forecast_values = make_forecast(pc_sums, product, days_to_forecast)
                            historical_values = pc_sums[product].values.tolist()[-past_days:]
                        else:
                            forecast_values = make_forecast(uc_sums, product, days_to_forecast)
                            historical_values = uc_sums[product].values.tolist()[-past_days:]

                        st.write(f"{product} {forecast_type} trend for past {past_days} days")
                        st.line_chart(historical_values)

                        st.success("Forecast generated successfully!")
                        st.subheader(f"{forecast_type} forecast Data for {product}")
                        st.line_chart(forecast_values[forecast_values.columns.tolist()])

                        # table to show the forecast values
                        forecasted_table_values = forecast_values.T

                        st.subheader(f"{forecast_type} forecast values for {product}")
                        st.table(forecasted_table_values)

                        try:
                            # download the forecast values as csv
                            csv = forecasted_table_values.to_csv(index=True)
                            st.download_button(
                                label="Download Forecast Values (CSV)",
                                data=csv,
                                file_name=f"{product}_{forecast_type}_forecast.csv",
                                mime="text/csv",
                            )
                        except:
                            st.error("Failed to generate CSV file download link.")

                        try:
                            # download the forecast values as excel
                            excel = forecasted_table_values.to_excel(index=True)
                            st.download_button(
                                label="Download Forecast Values (Excel)",
                                data=excel,
                                file_name=f"{product}_{forecast_type}_forecast.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                        except:
                            st.error("Failed to generate Excel file download link.")

                    except:
                        st.error("An error occurred while making the forecast.")

                else:
                    st.error("Please select the number of days to forecast.")
            else:
                st.error("Please select a forecast type.")
        else:
            st.error("Please select a product.")
except:
    st.error("Please upload and preprocess the data first.")


