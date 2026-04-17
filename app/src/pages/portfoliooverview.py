import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
aid = st.session_state.get('analyst_id', 1)
st.title('Portfolio Overview')
try:
    r = requests.get(f'{API}/a/portfolios/all')
    if r.status_code == 200 and r.json():
        portfolios = r.json()
        df = pd.DataFrame(portfolios)
        df['total_value'] = df['total_value'].apply(lambda x: f'${float(x):,.2f}')
        st.dataframe(df[['portfolio_id','portfolio_name','first_name','last_name','total_value']], use_container_width=True, hide_index=True)
        pid = st.selectbox('Select portfolio for details:', [p['portfolio_id'] for p in portfolios], format_func=lambda x: next(p['portfolio_name'] for p in portfolios if p['portfolio_id'] == x))
        r2 = requests.get(f'{API}/a/portfolios/{pid}')
        if r2.status_code == 200:
            pdata = r2.json()
            st.subheader(f"Holdings — {pdata['portfolio_name']}")
            if pdata.get('holdings'):
                hdf = pd.DataFrame(pdata['holdings'])
                hdf['current_value'] = hdf['current_value'].apply(lambda x: f'${float(x):,.2f}')
                st.dataframe(hdf, use_container_width=True, hide_index=True)
        st.subheader('Recent Transactions')
        r3 = requests.get(f'{API}/a/portfolios/{pid}/transactions')
        if r3.status_code == 200 and r3.json():
            tdf = pd.DataFrame(r3.json())
            tdf['amount'] = tdf['amount'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(tdf, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f'Error: {e}')
