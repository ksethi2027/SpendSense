import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
st.title('User Management')
role_filter = st.selectbox('Filter by role:', ['All','student','employee','analyst','admin'])
try:
    url = f'{API}/ad/users'
    if role_filter != 'All':
        url += f'?role={role_filter}'
    r = requests.get(url)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f'Error: {e}')
st.divider()
st.subheader('Update User Role')
with st.form('update_role'):
    uid = st.number_input('User ID', min_value=1, step=1)
    new_role = st.selectbox('New Role', ['student','employee','analyst','admin'])
    if st.form_submit_button('Update Role'):
        resp = requests.put(f'{API}/ad/users/{uid}', json={'role_type': new_role})
        if resp.status_code == 200:
            st.success('Role updated!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')
