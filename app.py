import streamlit as st
from utils import _home

st.set_page_config(
    page_title="SKU Sales Forecast",
    page_icon="assets/favicon.png",
)

def main():
    st.title("SKU Sales Forecast")
    _home.show()

if __name__ == "__main__":
    main()
