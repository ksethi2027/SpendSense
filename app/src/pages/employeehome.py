import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
name = st.session_state.get('first_name', 'Employee')
st.title(f'Welcome, {name}!')
st.write('### Employee Financial Dashboard')
col1, col2, col3 = st.columns(3)
with col1:
    st.info('🧾 **My Expenses** — Track spending by category and add new expenses.')
with col2:
    st.info('🏠 **Income & Bills** — Log income and manage housing bills.')
with col3:
    st.info('📊 **Investments** — View and update your portfolio holdings.')
