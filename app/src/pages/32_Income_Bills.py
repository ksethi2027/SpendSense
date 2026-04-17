import streamlit as st
import requests
import pandas as pd
from datetime import date
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 2)
st.title('Income & Bills')
tab1, tab2, tab3 = st.tabs(['Income', 'Housing Bills', 'Insurance'])
with tab1:
    try:
        r = requests.get(f'{API}/e/employee/{uid}/income')
        if r.status_code == 200 and r.json():
            df = pd.DataFrame(r.json())
            df['amount_income'] = df['amount_income'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f'Error: {e}')
    st.subheader('Log Income')
    with st.form('add_income'):
        cat = st.selectbox('Category', ['Salary','Bonus','Freelance','Side Gig','Dividend','Other'])
        amt = st.number_input('Amount ($)', min_value=0.01, step=10.0)
        d = st.date_input('Date', value=date.today())
        if st.form_submit_button('Log Income'):
            resp = requests.post(f'{API}/e/employee/{uid}/income', json={'category_income': cat, 'amount_income': amt, 'date_income': str(d)})
            if resp.status_code == 201:
                st.success('Income logged!')
                st.rerun()
with tab2:
    try:
        r = requests.get(f'{API}/e/employee/{uid}/housing-bills')
        if r.status_code == 200 and r.json():
            bills = r.json()
            for b in bills:
                c1, c2, c3, c4 = st.columns([2,2,2,2])
                c1.write(f"**{b['bill_type']}**")
                c2.write(f"${float(b['amount_hb']):,.2f}")
                c3.write(f"Due: {b['due_date_hb']}")
                status = b['payment_status']
                if status == 'Paid':
                    c4.success(status)
                elif status == 'Overdue':
                    c4.error(status)
                else:
                    c4.warning(status)
                    if st.button(f"Mark Paid", key=f"pay_{b['bill_id']}"):
                        resp = requests.put(f"{API}/e/housing-bills/{b['bill_id']}", json={'paid_date': str(date.today())})
                        if resp.status_code == 200:
                            st.rerun()
    except Exception as e:
        st.error(f'Error: {e}')
with tab3:
    try:
        r = requests.get(f'{API}/e/employee/{uid}/insurance')
        if r.status_code == 200 and r.json():
            df = pd.DataFrame(r.json())
            df['monthly_premium'] = df['monthly_premium'].apply(lambda x: f'${float(x):,.2f}')
            df['annual_cost'] = df['annual_cost'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f'Error: {e}')
