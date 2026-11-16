"""FoodBridge frontend (Streamlit).
1. Start the backend first:  uvicorn app.main:app --reload
2. Then start this page:     streamlit run frontend/streamlit_app.py
"""

import streamlit as st
import api_client
import ui_helpers
from views import dashboard_page, donation_page, recipient_page, distribution_page, report_page

st.set_page_config(page_title="FoodBridge", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")
ui_helpers.apply_page_style()

# Each menu item is a pair: (icon, page name).
PAGES = (("📊", "Dashboard"), ("🎁", "Donations"), ("🤝", "Recipients"), ("🚚", "Distributions"), ("📈", "Reports"))

# Remember the chosen page. The first time, show the Dashboard.
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# ---------- Top navigation bar ----------
with st.container(key="topbar"):
    columns = st.columns([1.6, 1, 1, 1, 1.1, 1, 1.4])
    columns[0].markdown('<div class="brand">🌿 Food<span>Bridge</span></div>', unsafe_allow_html=True)

    for number in range(len(PAGES)):
        icon, page_name = PAGES[number]
        button_type = "secondary"
        if page_name == st.session_state["current_page"]:
            button_type = "primary"  # the open page is highlighted
        if columns[number + 1].button(icon + " " + page_name, key="nav_" + page_name, type=button_type):
            st.session_state["current_page"] = page_name
            st.rerun()

    # Show whether the backend is running.
    try:
        api_client.get("/")
        columns[6].markdown('<span class="status-pill" style="color:#2E7D32">● API online</span>', unsafe_allow_html=True)
    except ValueError:
        columns[6].markdown('<span class="status-pill" style="color:#C62828">● API offline</span>', unsafe_allow_html=True)

# ---------- Show the chosen page ----------
page = st.session_state["current_page"]
if page == "Dashboard":
    dashboard_page.show_page()
elif page == "Donations":
    donation_page.show_page()
elif page == "Recipients":
    recipient_page.show_page()
elif page == "Distributions":
    distribution_page.show_page()
else:
    report_page.show_page()
