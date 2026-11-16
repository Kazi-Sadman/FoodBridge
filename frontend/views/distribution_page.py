from datetime import date
import streamlit as st
import api_client
from ui_helpers import show_page_header, show_table, DISTRIBUTION_COLUMNS


def show_page():
    show_page_header("Distribution Management", "Give donated food to recipients and keep the history.")
    tab_view, tab_add, tab_delete = st.tabs(["History", "Give food", "Delete"])

    with tab_add:
        donation_options = []
        recipient_options = []
        try:
            for donation in api_client.get("/donations"):
                if donation["status"] == "Available":
                    donation_options.append(donation["donation_id"] + " - " + donation["food_name"]
                                            + " (" + str(donation["remaining"]) + " " + donation["unit"] + " left)")
            for recipient in api_client.get("/recipients"):
                recipient_options.append(recipient["recipient_id"] + " - " + recipient["name"])
        except ValueError as error:
            st.error(str(error))

        if len(donation_options) == 0 or len(recipient_options) == 0:
            st.info("You need at least one available donation and one recipient.")
        else:
            with st.form("add_distribution_form", clear_on_submit=True):
                donation_choice = st.selectbox("Donation", donation_options, key="add_dis_donation")
                recipient_choice = st.selectbox("Recipient", recipient_options, key="add_dis_recipient")
                quantity = st.number_input("Quantity", value=1.0, key="add_dis_qty")
                distribution_date = st.date_input("Date", value=date.today(), key="add_dis_date")
                if st.form_submit_button("Give food"):
                    data = {"donation_id": donation_choice.split(" ")[0],  # the ID is the first word
                            "recipient_id": recipient_choice.split(" ")[0],
                            "quantity": quantity, "distribution_date": str(distribution_date)}
                    try:
                        st.success(api_client.post("/distributions", data)["message"])
                    except ValueError as error:
                        st.error(str(error))

    with tab_delete:
        try:
            ids = [d["distribution_id"] for d in api_client.get("/distributions")]
        except ValueError:
            ids = []
        if len(ids) > 0:
            chosen_id = st.selectbox("Choose distribution", ids, key="del_dis_id")
            sure = st.checkbox("I am sure", key="del_dis_sure")
            if st.button("Delete distribution", key="del_dis_button") and sure:
                try:
                    st.success(api_client.delete("/distributions/" + chosen_id)["message"])
                except ValueError as error:
                    st.error(str(error))

    with tab_view:
        try:
            show_table(api_client.get("/distributions"), DISTRIBUTION_COLUMNS)
        except ValueError as error:
            st.error(str(error))
