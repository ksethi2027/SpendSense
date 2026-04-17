import streamlit as st
import requests
import pandas as pd
from datetime import date
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 2)
st.title('My Expenses')
try:
    r = requests.get(f'{API}/e/employee/{uid}/expenses')
    if r.status_code == 200 and r.json():
        data = r.json()
        df = pd.DataFrame(data)
        st.subheader('Spending by Category')
        chart_df = df.copy()
        chart_df['total_spent'] = chart_df['total_spent'].apply(lambda x: float(x))
        st.bar_chart(chart_df.set_index('categoryName')['total_spent'])
        st.subheader('Details')
        display = df.copy()
        display['total_spent'] = display['total_spent'].apply(lambda x: f'${float(x):,.2f}')
        st.dataframe(display, use_container_width=True, hide_index=True)
    else:
        st.info('No expenses found.')
except Exception as e:
    st.error(f'Error: {e}')
st.divider()
st.subheader('Add New Expense')
with st.form('add_emp_expense'):
    cats_r = requests.get(f'{API}/ad/categories')
    cat_options = {}
    if cats_r.status_code == 200:
        for c in cats_r.json():
            cat_options[c['categoryName']] = c['category_id']
    cat = st.selectbox('Category', list(cat_options.keys()) if cat_options else ['Food & Dining'])
    amount = st.number_input('Amount ($)', min_value=0.01, step=0.01)
    desc = st.text_input('Description')
    exp_date = st.date_input('Date', value=date.today())
    if st.form_submit_button('Add Expense'):
        resp = requests.post(f'{API}/e/employee/{uid}/expenses', json={'category_id': cat_options.get(cat, 1), 'amount': amount, 'description': desc, 'expenseDate': str(exp_date)})
        if resp.status_code == 201:
            st.success('Expense added!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')
