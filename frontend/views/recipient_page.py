import streamlit as st
import api_client
from ui_helpers import show_page_header, show_table, RECIPIENT_TYPE_CHOICES, RECIPIENT_COLUMNS


def show_page():
    show_page_header("Recipient Management", "Register shelters, charities and families that receive food.")
    tab_view, tab_add, tab_update, tab_delete = st.tabs(["View / Search", "Add", "Update", "Delete"])

    with tab_add:
        with st.form("add_recipient_form", clear_on_submit=True):
            st.write("Register a shelter, charity, family or community group that receives food.")
            recipient_id = st.text_input("Recipient ID (optional - leave empty to create one automatically)", key="add_rec_id")
            name = st.text_input("Name", key="add_rec_name")
            recipient_type = st.selectbox("Recipient type", RECIPIENT_TYPE_CHOICES, key="add_rec_type")
            contact = st.text_input("Contact (phone or email)", key="add_rec_contact")
            address = st.text_input("Address", key="add_rec_address")
            if st.form_submit_button("Add recipient"):
                data = {"recipient_id": recipient_id, "name": name, "contact": contact,
                        "address": address, "recipient_type": recipient_type}
                try:
                    st.success(api_client.post("/recipients", data)["message"])
                except ValueError as error:
                    st.error(str(error))

    with tab_update:
        try:
            ids = [r["recipient_id"] for r in api_client.get("/recipients")]
        except ValueError as error:
            ids = []
            st.error(str(error))
        if len(ids) > 0:
            chosen_id = st.selectbox("Choose recipient", ids, key="up_rec_id")
            old = api_client.get("/recipients/" + chosen_id)
            with st.form("update_recipient_form"):
                name = st.text_input("Name", value=old["name"], key="up_rec_name" + chosen_id)
                contact = st.text_input("Contact", value=old["contact"], key="up_rec_contact" + chosen_id)
                address = st.text_input("Address", value=old["address"], key="up_rec_address" + chosen_id)
                recipient_type = st.selectbox("Type", RECIPIENT_TYPE_CHOICES, index=RECIPIENT_TYPE_CHOICES.index(old["recipient_type"]), key="up_rec_type" + chosen_id)
                if st.form_submit_button("Update recipient"):
                    data = {"name": name, "contact": contact, "address": address, "recipient_type": recipient_type}
                    try:
                        st.success(api_client.put("/recipients/" + chosen_id, data)["message"])
                    except ValueError as error:
                        st.error(str(error))

    with tab_delete:
        try:
            ids = [r["recipient_id"] for r in api_client.get("/recipients")]
        except ValueError:
            ids = []
        if len(ids) > 0:
            chosen_id = st.selectbox("Choose recipient", ids, key="del_rec_id")
            sure = st.checkbox("I am sure", key="del_rec_sure")
            if st.button("Delete recipient", key="del_rec_button") and sure:
                try:
                    st.success(api_client.delete("/recipients/" + chosen_id)["message"])
                except ValueError as error:
                    st.error(str(error))

    with tab_view:
        search = st.text_input("Search by ID, name or address", key="rec_search")
        try:
            show_table(api_client.get("/recipients", {"search": search}), RECIPIENT_COLUMNS)
        except ValueError as error:
            st.error(str(error))
