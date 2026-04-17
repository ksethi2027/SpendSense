import streamlit as st


def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")



# Student
def student_home_nav():
    st.sidebar.page_link("pages/00_Student_Home.py", label="Student Home", icon="🎓")
def semester_budget_nav():
    st.sidebar.page_link("pages/01_Semester_Budget.py", label="Semester Budget", icon="📊")
def track_expenses_nav():
    st.sidebar.page_link("pages/02_Track_Expenses.py", label="Track Expenses", icon="💸")
def savings_goals_nav():
    st.sidebar.page_link("pages/03_Savings_Goals.py", label="Savings Goals", icon="🎯")

# Analyst
def analyst_home_nav():
    st.sidebar.page_link("pages/10_Analyst_Home.py", label="Analyst Home", icon="📈")
def portfolio_overview_nav():
    st.sidebar.page_link("pages/11_Portfolio_Overview.py", label="Portfolio Overview", icon="💼")
def spending_analysis_nav():
    st.sidebar.page_link("pages/12_Spending_Analysis.py", label="Spending Analysis", icon="📉")
def risk_returns_nav():
    st.sidebar.page_link("pages/13_Risk_Returns.py", label="Risk & Returns", icon="⚖️")

# Admin
def admin_home_nav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="Admin Home", icon="🛡️")
def manage_categories_nav():
    st.sidebar.page_link("pages/21_Manage_Categories.py", label="Manage Categories", icon="🏷️")
def user_management_nav():
    st.sidebar.page_link("pages/22_User_Management.py", label="User Management", icon="👥")
def system_logs_nav():
    st.sidebar.page_link("pages/23_System_Logs.py", label="System Logs", icon="📋")

# Employee
def employee_home_nav():
    st.sidebar.page_link("pages/30_Employee_Home.py", label="Employee Home", icon="💰")
def my_expenses_nav():
    st.sidebar.page_link("pages/31_My_Expenses.py", label="My Expenses", icon="🧾")
def income_bills_nav():
    st.sidebar.page_link("pages/32_Income_Bills.py", label="Income & Bills", icon="🏠")
def investments_nav():
    st.sidebar.page_link("pages/33_Investments.py", label="Investments", icon="📊")


def SideBarLinks(show_home=False):
    import os
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", width=150)
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")
    if show_home:
        home_nav()
    if st.session_state["authenticated"]:
        role = st.session_state["role"]
        if role == "student":
            student_home_nav(); semester_budget_nav(); track_expenses_nav(); savings_goals_nav()
        elif role == "analyst":
            analyst_home_nav(); portfolio_overview_nav(); spending_analysis_nav(); risk_returns_nav()
        elif role == "admin":
            admin_home_nav(); manage_categories_nav(); user_management_nav(); system_logs_nav()
        elif role == "employee":
            employee_home_nav(); my_expenses_nav(); income_bills_nav(); investments_nav()
    
    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
