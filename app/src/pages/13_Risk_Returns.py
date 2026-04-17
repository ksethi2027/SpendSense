import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
API = 'http://web-api:4000'
aid = st.session_state.get('analyst_id', 1)
st.title('Risk vs Returns Analysis')
try:
    r = requests.get(f'{API}/a/analyst/{aid}/reports')
    if r.status_code == 200 and r.json():
        reports = r.json()
        pids = list(set(r2.get('portfolio_name') for r2 in reports))
        st.subheader('Performance Reports')
        rdf = pd.DataFrame(reports)
        st.dataframe(rdf[['portfolio_name','report_type','start_date','end_date','summary_text']], use_container_width=True, hide_index=True)
    portfolios_r = requests.get(f'{API}/a/portfolios/all')
    if portfolios_r.status_code == 200:
        portfolios = portfolios_r.json()
        pid = st.selectbox('Select portfolio for risk analysis:', [p['portfolio_id'] for p in portfolios], format_func=lambda x: next(p['portfolio_name'] for p in portfolios if p['portfolio_id'] == x))
        risk_r = requests.get(f'{API}/a/portfolios/{pid}/risk')
        if risk_r.status_code == 200 and risk_r.json():
            st.subheader('Risk-Return Profile')
            risk_data = risk_r.json()
            rdf = pd.DataFrame(risk_data)
            st.dataframe(rdf, use_container_width=True, hide_index=True)
        else:
            st.info('No risk data for this portfolio.')
except Exception as e:
    st.error(f'Error: {e}')
st.subheader('Generate New Report')
with st.form('new_report'):
    port_id = st.number_input('Portfolio ID', min_value=1, step=1)
    period_id = st.number_input('Period ID', min_value=1, step=1, value=10)
    rtype = st.selectbox('Report Type', ['Monthly Review','Quarterly Review','Annual Review'])
    summary = st.text_area('Summary')
    if st.form_submit_button('Generate Report'):
        resp = requests.post(f'{API}/a/analyst/{aid}/reports', json={'portfolio_id': port_id, 'period_id': period_id, 'report_type': rtype, 'summary_text': summary})
        if resp.status_code == 201:
            st.success('Report generated!')
            st.rerun()
        else:
            st.error(f'Error: {resp.text}')
