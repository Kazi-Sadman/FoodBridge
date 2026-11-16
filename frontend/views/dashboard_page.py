import streamlit as st
import api_client
import ui_helpers


def show_page():
    ui_helpers.show_page_header("Dashboard", "A quick look at donations, distributions and what is left.")
    try:
        summary = api_client.get("/reports/summary")
        totals = api_client.get("/reports/totals")
        categories = api_client.get("/reports/categories")
        expired = api_client.get("/reports/expired")
        donations = api_client.get("/donations")
        distributions = api_client.get("/distributions")
    except ValueError as error:
        st.error(str(error))
        return

    # Six summary cards in two rows of three.
    row1 = st.columns(3)
    with row1[0]:
        ui_helpers.show_metric_card("Total Donations", summary["donations"], "donation records")
    with row1[1]:
        ui_helpers.show_metric_card("Total Food Donated", ui_helpers.format_units(totals, "donated"))
    with row1[2]:
        ui_helpers.show_metric_card("Total Food Distributed", ui_helpers.format_units(totals, "distributed"))
    row2 = st.columns(3)
    with row2[0]:
        ui_helpers.show_metric_card("Remaining Food", ui_helpers.format_units(totals, "remaining"))
    with row2[1]:
        ui_helpers.show_metric_card("Total Recipients", summary["recipients"], "registered recipients")
    with row2[2]:
        ui_helpers.show_metric_card("Unique Donors", summary["donors"], "different donors")

    if summary["expired"] > 0:
        st.warning(str(summary["expired"]) + " donation(s) have expired. Expired food cannot be distributed.")
        ui_helpers.show_table(expired, ui_helpers.DONATION_COLUMNS)

    st.subheader("Donations by Category")
    st.bar_chart({"Category": list(categories.keys()), "Donations": list(categories.values())}, x="Category", y="Donations")

    left, right = st.columns(2)
    with left:
        st.subheader("Recent Donations")
        ui_helpers.show_table(list(reversed(donations))[:5], ui_helpers.DONATION_COLUMNS)
    with right:
        st.subheader("Recent Distributions")
        ui_helpers.show_table(list(reversed(distributions))[:5], ui_helpers.DISTRIBUTION_COLUMNS)
