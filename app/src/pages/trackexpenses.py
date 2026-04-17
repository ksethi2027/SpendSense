import streamlit as st
import requests
import pandas as pd
from datetime import date
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 1)
st.title('Track & Split Expenses')
tab1, tab2, tab3 = st.tabs(['My Expenses', 'Add Expense', 'Textbook Prices'])
with tab1:
    try:
        r = requests.get(f'{API}/s/students/{uid}/expenses')
        if r.status_code == 200 and r.json():
            df = pd.DataFrame(r.json())
            df['amount'] = df['amount'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info('No expenses found.')
    except Exception as e:
        st.error(f'Error: {e}')
with tab2:
    with st.form('add_expense'):
        cats_r = requests.get(f'{API}/ad/categories')
        cat_options = {}
        if cats_r.status_code == 200:
            for c in cats_r.json():
                cat_options[c['categoryName']] = c['category_id']
        cat_name = st.selectbox('Category', list(cat_options.keys()) if cat_options else ['Food & Dining'])
        amount = st.number_input('Amount ($)', min_value=0.01, step=0.01)
        desc = st.text_input('Description')
        exp_date = st.date_input('Date', value=date.today())
        is_acad = st.checkbox('Academic expense?')
        submitted = st.form_submit_button('Add Expense')
        if submitted:
            payload = {
                'category_id': cat_options.get(cat_name, 1),
                'amount': amount, 'description': desc,
                'expenseDate': str(exp_date),
                'is_academic': 1 if is_acad else 0, 'is_shared': 0
            }
            resp = requests.post(f'{API}/s/students/{uid}/expenses', json=payload)
            if resp.status_code == 201:
                st.success('Expense added!')
                st.rerun()
            else:
                st.error(f'Error: {resp.text}')
with tab3:
    try:
        r = requests.get(f'{API}/s/students/{uid}/textbooks')
        if r.status_code == 200 and r.json():
            df = pd.DataFrame(r.json())
            df['price'] = df['price'].apply(lambda x: f'${float(x):,.2f}')
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info('No textbooks found.')
    except Exception as e:
        st.error(f'Error: {e}')
