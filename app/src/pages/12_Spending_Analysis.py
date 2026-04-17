import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
aid = st.session_state.get('analyst_id', 1)
st.title('Spending Analysis')
try:
    r = requests.get(f'{API}/a/analyst/{aid}/spending')
    if r.status_code == 200 and r.json():
        data = r.json()
        df = pd.DataFrame(data)
        df['total_spent'] = df['total_spent'].apply(lambda x: float(x))
        st.subheader('Spending by User')
        chart_df = df.groupby(['first_name','last_name'])['total_spent'].sum().reset_index()
        chart_df['user'] = chart_df['first_name'] + ' ' + chart_df['last_name']
        st.bar_chart(chart_df.set_index('user')['total_spent'])
        st.subheader('Detailed Data')
        display_df = df.copy()
        display_df['total_spent'] = display_df['total_spent'].apply(lambda x: f'${x:,.2f}')
        display_df['avg_spending'] = display_df['avg_spending'].apply(lambda x: f'${float(x):,.2f}')
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info('No spending data found for this analyst.')
except Exception as e:
    st.error(f'Error: {e}')
