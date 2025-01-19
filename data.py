import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = st.secrets["url"]
conn = st.experimental_connection("gsheets", type = GSheetsConnection)
data = conn.read(spreadsheet = url, worksheet=0)

