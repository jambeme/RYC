import streamlit as st
import uuid
import extra_streamlit_components as stx


st.header("Rate Your Class")

controller = stx.CookieManager()

u = controller.get('uuid')

st.header(u)

if u is None:
    st.write(u)
    u = str (uuid.uuid4())
    controller.set('uuid', value = u, expires_at = 0)

grade = st.selectbox('Enter your grade:', options = [9, 10, 11, 12])
major = st.selectbox('Enter the major/field you are most interested in:', options = ['Math', 'Science', 'Comp-Sci', 'Med'])
