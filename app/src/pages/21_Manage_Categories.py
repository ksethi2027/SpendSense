import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
st.title('Manage Expense Categories')
try:
    r = requests.get(f'{API}/ad/categories')
    if r.status_code == 200:
        cats = r.json()
        st.subheader('Current Categories')
        for cat in cats:
            col1, col2, col3 = st.columns([3,4,1])
            col1.write(f"**{cat['categoryName']}**")
            col2.write(cat.get('description', ''))
            if col3.button('Delete', key=f"delcat_{cat['category_id']}"):
                resp = requests.delete(f"{API}/ad/categories/{cat['category_id']}")
                if resp.status_code == 200:
                    st.success('Deleted!')
                    st.rerun()
                else:
                    st.error(f'Error: {resp.text}')
except Exception as e:
    st.error(f'Error: {e}')
st.divider()
st.subheader('Add New Category')
with st.form('add_cat'):
    name = st.text_input('Category Name')
    desc = st.text_input('Description')
    if st.form_submit_button('Create Category'):
        resp = requests.post(f'{API}/ad/categories', json={'categoryName': name, 'description': desc})
        if resp.status_code == 201:
            st.success('Category created!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')
st.divider()
st.subheader('Update Category')
with st.form('update_cat'):
    cat_id = st.number_input('Category ID to update', min_value=1, step=1)
    new_name = st.text_input('New Name (leave blank to skip)')
    new_desc = st.text_input('New Description (leave blank to skip)')
    if st.form_submit_button('Update'):
        payload = {}
        if new_name: payload['categoryName'] = new_name
        if new_desc: payload['description'] = new_desc
        if payload:
            resp = requests.put(f'{API}/ad/categories/{cat_id}', json=payload)
            if resp.status_code == 200:
                st.success('Updated!')
                st.rerun()
            else:
                st.error(f'Error: {resp.text}')
