import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
uid = st.session_state.get('user_id', 1)
st.title('Savings Goals')
try:
    r = requests.get(f'{API}/s/students/{uid}/savings')
    if r.status_code == 200 and r.json():
        for goal in r.json():
            target = float(goal['targetAmount'])
            saved = float(goal['savedAmount'])
            pct = float(goal['pct_complete'])
            with st.container():
                c1, c2, c3, c4 = st.columns([3,2,2,1])
                c1.write(f"**{goal['goalName']}**")
                c2.write(f"${saved:,.2f} / ${target:,.2f}")
                c3.write(f"Due: {goal['targetDate']}")
                c4.write(f"{pct}%")
                st.progress(min(pct / 100, 1.0))
                col_a, col_b = st.columns(2)
                with col_a:
                    new_saved = st.number_input(f"Update saved for {goal['goalName']}", value=float(saved), key=f"save_{goal['goal_id']}", step=10.0)
                    if st.button('Update', key=f"btn_{goal['goal_id']}"):
                        resp = requests.put(f"{API}/s/savings/{goal['goal_id']}", json={'savedAmount': new_saved})
                        if resp.status_code == 200:
                            st.success('Updated!')
                            st.rerun()
                with col_b:
                    if st.button('Delete', key=f"del_{goal['goal_id']}"):
                        resp = requests.delete(f"{API}/s/savings/{goal['goal_id']}")
                        if resp.status_code == 200:
                            st.success('Deleted!')
                            st.rerun()
                st.divider()
except Exception as e:
    st.error(f'Error: {e}')
st.subheader('Add New Goal')
with st.form('new_goal'):
    name = st.text_input('Goal Name')
    target = st.number_input('Target Amount ($)', min_value=1.0, step=10.0)
    tdate = st.date_input('Target Date')
    if st.form_submit_button('Create Goal'):
        resp = requests.post(f'{API}/s/students/{uid}/savings', json={'goalName': name, 'targetAmount': target, 'targetDate': str(tdate)})
        if resp.status_code == 201:
            st.success('Goal created!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')

