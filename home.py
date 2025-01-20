import streamlit as st
import uuid
import extra_streamlit_components as stx
import pandas as pd
import gspread
import datetime
import time

st.header("Rate Your Class")

controller = stx.CookieManager()

u = controller.get('uuid')
datetime.time.sleep(2)
date = datetime.datetime(2199, 10, 25)

if u is None:
    u = str(uuid.uuid4())
    controller.set('uuid', u, expires_at = date)

#do this in a st.popover

grade = st.selectbox('Enter your grade:', options = [9, 10, 11, 12])
major = st.selectbox('Enter the major/field you are most interested in:', options = ['Math', 'Science', 'Comp-Sci', 'Med'])

classes = pd.read_csv('ryc.csv')

type = st.selectbox("What type of class would you like to rate?", options = ['English', 'Social Studies', 'Math', 'Science', 'World Languages', 'Tech, Comp Sci, & Robotics', 'Visual/Performing Arts', 'Physical & Health Education', 'Catalyst', 'Quest', 'Learning Support'])

classes = classes.where(classes["Category"] == type).dropna(how='all')["Classname"]

gc = gspread.service_account_from_dict(st.secrets.goog)
sh = gc.open(st.secrets.goog.spreadsheet)
ws = sh.sheet1

wsU = sh.get_worksheet(1)
contain = wsU.find(query=u,in_column=0)

if(contain is not None):
    contain = wsU.get('B'+str(contain.row)).first()
    #filter = classes['Classname'].str.contains(contain)
    #classes = classes[~filter]

c = st.selectbox("What class would you like to rate?", options=classes)

rating = st.slider("How do you rate " + c, 1, 10)

ls = [u, major, grade, c, rating]

send = st.button("Send Rating")

if send:
    ws.append_row(values=ls, table_range="A2:E2")
    st.success("Submitted Rating!")