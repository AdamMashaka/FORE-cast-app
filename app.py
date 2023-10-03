import streamlit as st
from utils import _home

st.set_page_config(
    page_title="SKU Level Predictive Analytics Model",
    page_icon="assets/favicon.png",
)

def main():
    st.title("RTM - SKU Level Predictive Analytics Model")
    _home.show()

if __name__ == "__main__":
    main()
