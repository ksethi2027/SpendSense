import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout='wide')
SideBarLinks()
st.title('About SpendSense')
st.write("""
**SpendSense** is a financial management application designed to help users better manage,
understand, and optimize their spending habits. Unlike traditional budgeting apps, SpendSense
analyzes user-specific data to provide personalized insights tailored to every lifestyle.

### Team Members
- **Rashi** — Backend & Database
- **Jake** — API Development
- **Sophia** — Frontend & UI
- **Kashish** — Data & Analysis

### Course
CS 3200 — Database Design · Spring 2026 · Northeastern University
""")
