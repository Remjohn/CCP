# Page 1: Dashboard (redirect to main)
import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="📋", layout="wide")
st.switch_page("app.py")
