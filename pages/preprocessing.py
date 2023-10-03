import streamlit as st
import pandas as pd
from utils.preprocess import preprocess_raw_dataset


st.title("Data Preprocessing")
st.header("Update Dataset")

uploaded_file = st.file_uploader("Upload a file", type=["xlsx"])

if uploaded_file is not None:
    # save the uploaded file to "data/uploads"
    try:
        with open(f"data/uploads/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write("File uploaded successfully... 🎉")

        # read the uploaded file with try catch block for xls and xlsx and csv
        try:
            df = pd.read_excel(f"data/uploads/{uploaded_file.name}")
            # get uploaded file name
            file_name = uploaded_file.name
            # preprocess the uploaded file
            try:
                pc_sums, uc_sums = preprocess_raw_dataset(f"data/uploads/{uploaded_file.name}")
                st.success("Data Preprocessed Successfully.")

                st.write("Extracted PC Sums:")
                st.dataframe(pc_sums)

                st.write("Extracted UC Sums:")
                st.dataframe(uc_sums)

                # create buttons to download the preprocessed data
                st.write("Download the preprocessed data: ⬇")
                if st.button("Download PC Sums"):
                    st.markdown(f'<a href="data/processed/pc_sums.csv" download="{file_name}_pc_sums.csv">Download PC Sums</a>', unsafe_allow_html=True)

                if st.button("Download UC Sums"):
                    st.markdown(f'<a href="data/processed/uc_sums.csv" download="{file_name}_uc_sums.csv">Download UC Sums</a>', unsafe_allow_html=True)

            except:
                st.error("Error in preprocessing the uploaded file. Please try again.")

        except:
            st.write("File uploaded is not in the correct format. please upload an excel file. Please try again.")


    except FileNotFoundError:
        st.error("FileNotFoundError: File not found. Please try again.")

