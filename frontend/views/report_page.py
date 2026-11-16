import streamlit as st
import api_client
from ui_helpers import show_page_header, show_table, DONATION_COLUMNS


def show_page():
    show_page_header("Reports", "Totals, summaries and food that needs attention.")
    try:
        totals = api_client.get("/reports/totals")
        categories = api_client.get("/reports/categories")
        recipients = api_client.get("/reports/recipients")
        donors = api_client.get("/reports/donors")
        expired = api_client.get("/reports/expired")
    except ValueError as error:
        st.error(str(error))
        return

    st.subheader("Totals by unit")
    show_table(totals, {"unit": "Unit", "donated": "Donated", "distributed": "Distributed", "remaining": "Remaining"})

    st.subheader("Donations by category")
    show_table([{"category": name, "donations": number} for name, number in categories.items()],
               {"category": "Category", "donations": "Donations"})

    st.subheader("Distributions per recipient")
    show_table(recipients, {"recipient": "Recipient", "distributions": "Distributions", "total_quantity": "Total Quantity"})

    st.subheader("Donors (" + str(len(donors)) + " different donors)")
    st.write(", ".join(donors))

    st.subheader("Expired donations")
    show_table(expired, DONATION_COLUMNS)
