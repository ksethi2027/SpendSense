import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
name = st.session_state.get('first_name', 'Admin')
st.title(f'Welcome, {name}!')
st.write('### System Administrator Dashboard')
col1, col2, col3 = st.columns(3)
with col1:
    st.info('🏷️ **Manage Categories** — Create, update, and delete expense categories.')
with col2:
    st.info('👥 **User Management** — View and manage user accounts and roles.')
with col3:
    st.info('📋 **System Logs** — Monitor activity and validate data integrity.')
