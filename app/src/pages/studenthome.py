import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
name = st.session_state.get('first_name', 'Student')
st.title(f'Welcome, {name}!')
st.write('### Student Dashboard')
st.write('Use the sidebar to navigate to your financial tools:')
col1, col2, col3 = st.columns(3)
with col1:
    st.info('📊 **Semester Budget** — Track spending by semester and compare against your budget.')
with col2:
    st.info('💸 **Track Expenses** — Log expenses, compare textbook prices, and manage split costs.')
with col3:
    st.info('🎯 **Savings Goals** — Set and monitor your savings targets.')
