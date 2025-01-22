import streamlit as st
import uuid
import extra_streamlit_components as stx
import pandas as pd
import gspread
import datetime
import time
import numpy as np


controller = stx.CookieManager()

u = controller.get('uuid')
grade = controller.get('grade')
major = controller.get('major')

if major is None or u is None or grade is None:
    time.sleep(3)

date = datetime.datetime(2199, 10, 25)

holder = st.empty()

if 'reset' not in st.session_state:
    st.session_state.reset = False

if "page" not in st.session_state:
    st.session_state.page = 2

if major is None or u is None or grade is None or st.session_state.reset == True:
    st.session_state.page = 0
else:
    st.session_state.page = 1

if st.session_state.page == 0:
    with holder.container():
        st.header("Welcome to Rate Your Class📊!")
        st.subheader("Give us some information about you before you start.")
        u = str(uuid.uuid4())
        grade = st.selectbox('Enter your grade:', options = [9, 10, 11, 12])
        major = st.selectbox('Enter the major/field you are most interested in:', options = ['Visual/Performing Arts', 'Buisness/Econ', 'Comp-Sci', 'Med', 'Engineering', 'Education', 'Social Sciences', 'Psychology', 'Communications', 'Law', 'Accounting', 'Physics'])
        send = st.button("Send Data")
        if(send):
            controller.set('uuid', u, expires_at = date, key = 'set')
            controller.set('grade',  grade, expires_at = date, key='set2')
            controller.set('major',  major, expires_at = date, key='set3')
            st.session_state.reset = False
            st.session_state.page = 1

if st.session_state.page == 1:
    with holder.container():
        tab1, tab2, tab3 = st.tabs(['🏠Home', '📊Rate', '📈Stats'])
        
        with tab1:
            st.session_state.reset = False
            st.header("Rate Your Class📊")
            st.subheader("Welcome to Rate Your Class!")
            st.write("The Rate Your Class™© (not trademarked or copyrighted) system aims to solve one massive question that students across SAS face almost yearly: what classes do I take, and what classes are meant to be avoided at all costs? Every year, students scramble to ask their friends if the classes they will take are completely undoable and actual horror shows and, realistically, should never be taken. But finally, that issue is being solved for good by Rate Your Class™©, which allows you and your peers to rate the classes you have taken in the past and see data from other student ratings, allowing you to determine whether taking ATDS is the right decision for you (it 100% is trust me). Rate Your Class™© takes in basic knowledge about the user, including a user’s grade and major they plan to pursue in college, and then allows the user to provide ratings of the courses that they have taken in the past, with the options of courses to rate being all of the courses that SAS currently offers to the student body in the 2024-2025 school year. These ratings and user data are then compiled and formatted into data that users can search thro.ugh to find which courses are best suited for them, with statistics returned showing what type of major and what grade they felt about the difficulty of the class.This information that Rate Your Class™© is providing to the student body should hopefully allow students to make much more informed decisions about what courses to take, allowing them to manage their workloads more effectively and efficiently, removing stress (or adding if someone wants to for some reason) from their already very hectic lives and schedules.")
            st.subheader("So what does all that yap above mean?")
            st.write("Rate your class let's you rate your classes at SAS and see what other people rated classes as, letting you know how hard or easy a class is!")
            st.subheader("Want to change your major/grade?")
            st.write("Warning: This will reset your progress of what courses you have rated so far! The reviews are still held, but you will no longer be able to know what classes you rated.")
            reset = st.button("Reset")
            if reset:
                st.header("RESETTED")
                time.sleep(5)
                st.session_state.reset = True
                

        with tab2:
            
            if 'category' not in st.session_state:
                st.session_state.category = pd.read_csv('ryc.csv')

            st.header("Rate")

            st.subheader("DISCLAIMER: The thing for getting classes and posting reviews is kinda sensitive so like please be gentle and slow with it. Thank you!")

            type = st.selectbox("What type of class would you like to rate?", options = ['English', 'Social Studies', 'Math', 'Science', 'World Languages', 'Tech, Comp Sci, & Robotics', 'Visual/Performing Arts', 'Physical & Health Education', 'Catalyst', 'Quest', 'Learning Support'])

            gc = gspread.service_account_from_dict(st.secrets.goog)
            sh = gc.open(st.secrets.goog.spreadsheet)

            vals = sh.get_worksheet(1).get_all_values()

            vals = pd.DataFrame(vals)

            vals = vals.T.set_index(0).T
            vals = vals.head(-1)
            vals = vals.tail(-1)
            vals = vals.style.hide(axis="index").data

            topic = vals["Class"]

            topic = np.array(topic)

            add = list()

            for x in topic:
                obj = st.session_state.category.where(st.session_state.category["Classname"] == x).dropna(how='all')["Category"]
                obj = obj.tolist()
                add.insert(0, obj.pop(0))
            

            ws = sh.sheet1

            wsU = sh.get_worksheet(2)
            contain = wsU.find(query=u,in_column=0)

            st.session_state.classes = st.session_state.category.where(st.session_state.category["Category"] == type).dropna(how='all')["Classname"]

            if(contain is not None):
                contain = list(set(wsU.get('B'+str(contain.row)).first().split(", "))) 
                st.session_state.classes = pd.DataFrame(st.session_state.classes)
                st.session_state.classes = st.session_state.classes[~st.session_state.classes['Classname'].isin(contain)]

            c = st.selectbox("What class would you like to rate?", options=st.session_state.classes)

            rating = st.slider("How do you rate " + c +" from easy to hard (1 = easy, 10 = hard).", 1, 10)

            ls = [u, major, grade, c, rating-1]

            send = st.button("Send Rating")

            if send:
                ws.append_row(values=ls, table_range="A2:E2")
                st.session_state.classes = st.session_state.classes[st.session_state.classes!=c]
                st.success("Submitted Rating!")
                st.rerun()


        with tab3:
            st.dataframe(vals)

            st.line_chart(x= 'Class', data = vals[['Class', 'MEDIAN of Rating', 'AVERAGE of Rating']],  y_label= 'Rating')