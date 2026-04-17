import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 1)
st.title('Semester Budget Dashboard')
try:
    r = requests.get(f'{API}/s/students/{uid}/semesters')
    if r.status_code == 200 and r.json():
        data = r.json()
        for sem in data:
            with st.expander(f"**{sem['semName']}** — {sem['startDate']} to {sem['endDate']}", expanded=True):
                c1, c2, c3 = st.columns(3)
                budget = float(sem['totalBudget'])
                spent = float(sem['total_spent'])
                remaining = float(sem['remaining_budget'])
                c1.metric('Total Budget', f'${budget:,.2f}')
                c2.metric('Total Spent', f'${spent:,.2f}')
                c3.metric('Remaining', f'${remaining:,.2f}', delta=f'{remaining/budget*100:.0f}% left' if budget > 0 else '')
                if budget > 0:
                    st.progress(min(spent / budget, 1.0))
    else:
        st.info('No semester data found.')
except Exception as e:
    st.error(f'Could not connect to API: {e}')
st.divider()
st.subheader('Tuition Payments')
try:
    r2 = requests.get(f'{API}/s/students/{uid}/tuition')
    if r2.status_code == 200 and r2.json():
        df = pd.DataFrame(r2.json())
        for col in ['amountDue','amountPaid','balance_remaining']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f'${float(x):,.2f}')
        st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f'Error: {e}')
