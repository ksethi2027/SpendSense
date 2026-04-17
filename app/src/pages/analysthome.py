import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
name = st.session_state.get('first_name', 'Analyst')
st.title(f'Welcome, {name}!')
st.write('### Financial Analyst Dashboard')
col1, col2, col3 = st.columns(3)
with col1:
    st.info('💼 **Portfolio Overview** — View portfolio details, holdings, and transactions.')
with col2:
    st.info('📉 **Spending Analysis** — Analyze user spending trends and patterns.')
with col3:
    st.info('⚖️ **Risk & Returns** — Compare risk levels against return rates.')
