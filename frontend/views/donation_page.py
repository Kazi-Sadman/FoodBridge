from datetime import date
import streamlit as st
import api_client
from ui_helpers import show_page_header, show_table, CATEGORY_CHOICES, UNIT_CHOICES, DONATION_COLUMNS


def show_page():
    show_page_header("Donation Management", "Record donated food and keep track of what is left.")
    tab_view, tab_add, tab_update, tab_delete = st.tabs(["View / Search", "Add", "Update", "Delete"])

    # The View tab is filled last, so it always shows the newest data.
    with tab_add:
        with st.form("add_donation_form", clear_on_submit=True):
            donation_id = st.text_input("Donation ID (leave empty for automatic)", key="add_don_id")
            donor = st.text_input("Donor name", key="add_don_donor")
            food = st.text_input("Food name", key="add_don_food")
            category = st.selectbox("Category", CATEGORY_CHOICES, key="add_don_category")
            quantity = st.number_input("Quantity", value=1.0, key="add_don_qty")
            unit = st.selectbox("Unit", UNIT_CHOICES, key="add_don_unit")
            expiry = st.date_input("Expiry date", value=date.today(), key="add_don_expiry")
            if st.form_submit_button("Add donation"):
                data = {"donation_id": donation_id, "donor_name": donor, "food_name": food, "category": category,
                        "quantity": quantity, "unit": unit, "expiry_date": str(expiry)}
                try:
                    st.success(api_client.post("/donations", data)["message"])
                except ValueError as error:
                    st.error(str(error))

    with tab_update:
        try:
            ids = [d["donation_id"] for d in api_client.get("/donations")]
        except ValueError as error:
            ids = []
            st.error(str(error))
        if len(ids) > 0:
            chosen_id = st.selectbox("Choose donation", ids, key="up_don_id")
            old = api_client.get("/donations/" + chosen_id)
            with st.form("update_donation_form"):
                donor = st.text_input("Donor name", value=old["donor_name"], key="up_don_donor" + chosen_id)
                food = st.text_input("Food name", value=old["food_name"], key="up_don_food" + chosen_id)
                category = st.selectbox("Category", CATEGORY_CHOICES, index=CATEGORY_CHOICES.index(old["category"]), key="up_don_cat" + chosen_id)
                quantity = st.number_input("Quantity", value=float(old["quantity"]), key="up_don_qty" + chosen_id)
                unit = st.selectbox("Unit", UNIT_CHOICES, index=UNIT_CHOICES.index(old["unit"]), key="up_don_unit" + chosen_id)
                expiry = st.date_input("Expiry date", value=date.fromisoformat(old["expiry_date"]), key="up_don_exp" + chosen_id)
                if st.form_submit_button("Update donation"):
                    data = {"donor_name": donor, "food_name": food, "category": category,
                            "quantity": quantity, "unit": unit, "expiry_date": str(expiry)}
                    try:
                        st.success(api_client.put("/donations/" + chosen_id, data)["message"])
                    except ValueError as error:
                        st.error(str(error))

    with tab_delete:
        try:
            ids = [d["donation_id"] for d in api_client.get("/donations")]
        except ValueError:
            ids = []
        if len(ids) > 0:
            chosen_id = st.selectbox("Choose donation", ids, key="del_don_id")
            sure = st.checkbox("I am sure", key="del_don_sure")
            if st.button("Delete donation", key="del_don_button") and sure:
                try:
                    st.success(api_client.delete("/donations/" + chosen_id)["message"])
                except ValueError as error:
                    st.error(str(error))

    with tab_view:
        col1, col2 = st.columns(2)
        search = col1.text_input("Search by ID, donor or food", key="don_search")
        category = col2.selectbox("Category", ["All"] + list(CATEGORY_CHOICES), key="don_category")
        try:
            show_table(api_client.get("/donations", {"search": search, "category": category}), DONATION_COLUMNS)
        except ValueError as error:
            st.error(str(error))
