import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 2)
st.title('My Investments')
try:
    r = requests.get(f'{API}/e/employee/{uid}/investments')
    if r.status_code == 200 and r.json():
        data = r.json()
        df = pd.DataFrame(data)
        portfolios = df['portfolio_name'].unique()
        for pname in portfolios:
            st.subheader(pname)
            pdf = df[df['portfolio_name'] == pname]
            display = pdf[['asset_name','asset_type','quantity','current_value','allocation_pct']].copy()
            display['current_value'] = display['current_value'].apply(lambda x: f'${float(x):,.2f}')
            display['allocation_pct'] = display['allocation_pct'].apply(lambda x: f'{float(x):.1f}%')
            st.dataframe(display, use_container_width=True, hide_index=True)
    else:
        st.info('No investments found.')
except Exception as e:
    st.error(f'Error: {e}')
st.divider()
st.subheader('Update Holding Value')
with st.form('update_holding'):
    hid = st.number_input('Holding ID', min_value=1, step=1)
    new_val = st.number_input('New Value ($)', min_value=0.0, step=100.0)
    if st.form_submit_button('Update'):
        resp = requests.put(f'{API}/e/investments/{hid}', json={'current_value': new_val})
        if resp.status_code == 200:
            st.success('Updated!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')
