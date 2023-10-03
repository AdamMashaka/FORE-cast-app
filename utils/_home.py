import streamlit as st

def show():
    st.header("Welcome to the Sales Forecast")

    # App Description
    st.markdown(
        """
        This app allows you to forecast sales for various products using time series analysis.
        You can upload your sales dataset, preprocess the data, make forecasts, and generate reports.

        **How to Use:**

        - Use the navigation sidebar on the left to access different sections of the app.
        - Click on the "Data Preprocessing" page to upload and preprocess your sales data.
        - On the "Forecast" page, you can make predictions for a single product and view prediction charts and tables.
        - The "Report" page enables you to generate predictions for the entire dataset and download the final dataset.

        Feel free to explore and make informed sales forecasts for your products!

        For any questions or issues, please contact our support team.
        """
    )

    # Important Information
    st.subheader("Important Information")

    st.markdown(
        """
        - Ensure your sales data is in excel format and follows the required format for uploading.
        - Data preprocessing may take some time depending on the size of your dataset.
        - Please make sure to save and download your forecasts and reports for future reference.
        """
    )
    #  add images to specify the format of the data
    st.subheader("Data Format")

    st.markdown(
        """
        - The sales data should contain the following columns: `products`, `sum_pc`, `sum_uc` for each product.
        - The `date` column should be in `YYYY-MM-DD` format.
        - The `units_sold` column should contain integer values.
        - The sales sheets should have year as the sheet name.
        """
    )