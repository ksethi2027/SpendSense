import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
st.title('System Logs & Data Validation')
tab1, tab2 = st.tabs(['Activity Logs', 'Data Validation'])
with tab1:
    limit = st.slider('Number of log entries', 10, 100, 50)
    try:
        r = requests.get(f'{API}/ad/logs?limit={limit}')
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f'Error: {e}')
with tab2:
    if st.button('Run Validation Checks'):
        try:
            r = requests.get(f'{API}/ad/validation')
            if r.status_code == 200:
                result = r.json()
                if result['count'] == 0:
                    st.success('All data validation checks passed!')
                else:
                    st.warning(f"Found {result['count']} issues:")
                    df = pd.DataFrame(result['issues'])
                    st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f'Error: {e}')
