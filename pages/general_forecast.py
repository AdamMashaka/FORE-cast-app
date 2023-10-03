import streamlit as st
import pandas as pd

from utils.forecast import make_forecast


st.title("General Forecast")
st.write("Forecast for the entire dataset📈")

try:
    pc_sums = pd.read_csv("data/processed/pc_sums.csv", index_col=0)
    uc_sums = pd.read_csv("data/processed/uc_sums.csv", index_col=0)
    product_list = pc_sums.columns[1:-1].tolist()

    st.sidebar.title("Forecast Options")
    days_to_forecast = st.sidebar.slider("Select the number of days to forecast", 1, 30)

    # empty dataframe to store the forecast
    sum_pc_df = pd.DataFrame()
    sum_uc_df = pd.DataFrame()


    # add a button to the sidebar to make the forecast
    if st.sidebar.button("Make Forecast"):
        # create a progress bar
        progress_bar = st.progress(0)
        # progress bar label
        progress_text = st.empty()

        # iterate over each product and make the forecast
        for product in product_list:
            # make the forecast for the product
            pc_forecast = make_forecast(pc_sums, product, days_to_forecast)
            uc_forecast = make_forecast(uc_sums, product, days_to_forecast)

            # add the forecast to the dataframe
            sum_pc_df[product] = pc_forecast['Forecast'].values
            sum_uc_df[product] = uc_forecast['Forecast'].values

            # set index to date
            sum_pc_df.index = pc_forecast.index
            sum_uc_df.index = uc_forecast.index

            # update the progress bar
            _progress = int((product_list.index(product) + 1) / len(product_list) * 100)
            progress_bar.progress(_progress)
            progress_text.text(f"Forecasting for {product}...  {_progress}%")

        # display the forecast
        st.subheader("Sum PC Forecast")
        st.dataframe(sum_pc_df)

        st.subheader("Sum UC Forecast")
        st.dataframe(sum_uc_df)

        # plot the forecast
        st.subheader("Sum PC Forecast Plot")
        st.line_chart(sum_pc_df)

        st.subheader("Sum UC Forecast Plot")
        st.line_chart(sum_uc_df)

        # download the forecast values as csv
        csv = sum_pc_df.T.to_csv(index=True)
        st.download_button(
            label="Download Sum Pc Values (CSV)",
            data=csv,
            file_name="Sum_pc_general_forecast.csv",
            mime="text/csv",
        )

        csv_ = sum_uc_df.T.to_csv(index=True)
        st.download_button(
            label="Download Sum Uc Values (CSV)",
            data=csv_,
            file_name="Sum_uc_general_forecast.csv",
            mime="text/csv",
        )

        progress_text.text("Data ready to download 🎉!")

except FileNotFoundError:
    st.error("Please upload the sales data first!")
    st.stop()