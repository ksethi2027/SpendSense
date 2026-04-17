import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

API = 'http://web-api:4000'

st.title('SpendSense')
st.write('### Smart financial management for every lifestyle')
st.write('Select a role and user below to get started.')

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader('🎓 Student')
    student_options = {
        'Jane Doe (user 1)': (1, 'Jane'),
        'Alice Nguyen (user 5)': (5, 'Alice'),
        'Brian Okafor (user 6)': (6, 'Brian'),
        'Carmen Reyes (user 7)': (7, 'Carmen'),
        'Derek Chan (user 8)': (8, 'Derek'),
    }
    student_choice = st.selectbox('Select student:', list(student_options.keys()), key='student_sel')
    if st.button('Login as Student', type='primary', use_container_width=True):
        uid, name = student_options[student_choice]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'student'
        st.session_state['first_name'] = name
        st.session_state['user_id'] = uid
        st.switch_page('pages/00_Student_Home.py')

with col2:
    st.subheader('💰 9-5 Employee')
    emp_options = {
        'Marcus Chen (user 2)': (2, 'Marcus'),
        'James Wilson (user 14)': (14, 'James'),
        'Karen Lopez (user 15)': (15, 'Karen'),
        'Liam Brown (user 16)': (16, 'Liam'),
        'Mia Davis (user 17)': (17, 'Mia'),
    }
    emp_choice = st.selectbox('Select employee:', list(emp_options.keys()), key='emp_sel')
    if st.button('Login as Employee', type='primary', use_container_width=True):
        uid, name = emp_options[emp_choice]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'employee'
        st.session_state['first_name'] = name
        st.session_state['user_id'] = uid
        st.switch_page('pages/30_Employee_Home.py')

col3, col4 = st.columns(2)

with col3:
    st.subheader('📈 Financial Analyst')
    analyst_options = {
        'John Smith (analyst 1)': (1, 'John', 3),
        'Tara White (analyst 2)': (2, 'Tara', 24),
        'Uma Harris (analyst 3)': (3, 'Uma', 25),
    }
    analyst_choice = st.selectbox('Select analyst:', list(analyst_options.keys()), key='analyst_sel')
    if st.button('Login as Analyst', type='primary', use_container_width=True):
        aid, name, uid = analyst_options[analyst_choice]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['first_name'] = name
        st.session_state['user_id'] = uid
        st.session_state['analyst_id'] = aid
        st.switch_page('pages/10_Analyst_Home.py')

with col4:
    st.subheader('🛡️ System Administrator')
    admin_options = {
        'Mary Johnson (user 4)': (4, 'Mary'),
        'Wendy Lewis (user 27)': (27, 'Wendy'),
        'Xavier Robinson (user 28)': (28, 'Xavier'),
    }
    admin_choice = st.selectbox('Select admin:', list(admin_options.keys()), key='admin_sel')
    if st.button('Login as Admin', type='primary', use_container_width=True):
        uid, name = admin_options[admin_choice]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = name
        st.session_state['user_id'] = uid
        st.switch_page('pages/20_Admin_Home.py')


