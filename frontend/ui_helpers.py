"""Helpers used by every page: the page style (CSS), banner, cards and tables."""

import streamlit as st

# Choices for the select boxes (the backend checks every value again).
CATEGORY_CHOICES = ("Cooked Meal", "Bakery", "Fruits & Vegetables", "Grains & Staples",
                    "Dairy", "Beverages", "Packaged Food", "Other")
UNIT_CHOICES = ("kg", "liter", "piece", "packet", "box")
RECIPIENT_TYPE_CHOICES = ("Shelter", "Charity", "Family", "Community Group")

# Table columns: {name in the data: title shown to the user}
DONATION_COLUMNS = {"donation_id": "ID", "food_name": "Food", "donor_name": "Donor", "category": "Category",
                    "quantity": "Quantity", "unit": "Unit", "remaining": "Remaining",
                    "expiry_date": "Expiry Date", "status": "Status"}
RECIPIENT_COLUMNS = {"recipient_id": "ID", "name": "Name", "recipient_type": "Type",
                     "contact": "Contact", "address": "Address"}
DISTRIBUTION_COLUMNS = {"distribution_id": "ID", "donation_id": "Donation", "food_name": "Food",
                        "recipient_name": "Recipient", "quantity": "Quantity", "unit": "Unit",
                        "distribution_date": "Date"}

# CSS (the language that styles web pages): a light green and white look.
PAGE_STYLE = """
<style>
/* Page: light green background, no sidebar, no footer */
.stApp { background: #F4F8F4; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], [data-testid="stToolbar"], footer { display: none; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 3.5rem; max-width: 1200px; }

/* Readable text: dark green-black on the light page, even when Streamlit uses its dark theme */
.stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp [data-testid="stMarkdown"] p, .stApp [data-testid="stMarkdown"] li,
.stApp [data-testid="stWidgetLabel"] p, .stApp [data-testid="stCheckbox"] p,
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stExpander"] summary p,
.stApp [data-testid="stAlert"] p, .stApp [data-testid="stFileUploaderDropzone"] span,
.stApp [data-testid="stFileUploaderDropzone"] small { color: #1B2A1E; }
.stApp [data-testid="stCaptionContainer"] { color: #5F7A64; }
.stApp button p { color: inherit; }

/* Tabs: Add / Update / Delete ... */
.stApp button[role="tab"] p { color: #3C5A40; font-weight: 600; font-size: 1rem; }
.stApp button[role="tab"][aria-selected="true"] p { color: #1B7F46; }
[data-baseweb="tab-highlight"] { background: #2E7D32; }
[data-baseweb="tab-border"] { background: #DCEBDD; }

/* Inputs, dropdowns and date pickers: white box, dark text */
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] > div, .stApp [data-baseweb="base-input"] {
    background: #FFFFFF; color: #1B2A1E; border-color: #CFE3D1;
}
.stApp [data-baseweb="select"] div { color: #1B2A1E; }
.stApp ::placeholder { color: #8FA394; }
.stApp [data-testid="stNumberInput"] button { background: #EAF4EB; color: #1B2A1E; }
[role="listbox"], [role="option"] { background: #FFFFFF; color: #1B2A1E; }

/* Normal (secondary) buttons: white with dark text */
.stApp button[kind="secondary"], .stApp button[data-testid="stBaseButton-secondary"],
.stApp [data-testid="stFileUploaderDropzone"] button {
    background: #FFFFFF; color: #1B2A1E; border: 1px solid #BFD8C2;
}
.stApp [data-testid="stFileUploaderDropzone"] { background: #FFFFFF; border: 1px dashed #BFD8C2; }

/* Top navigation bar */
.st-key-topbar {
    background: white; border: 1px solid #DCEBDD; border-radius: 18px;
    padding: 0.4rem 1rem; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.st-key-topbar [data-testid="stHorizontalBlock"] { align-items: center; }
.brand { font-size: 1.25rem; font-weight: 800; color: #1B2A1E; }
.brand span { color: #2E7D32; }
.status-pill {
    float: right; border: 1px solid #DCEBDD; border-radius: 20px;
    padding: 0.2rem 0.8rem; font-size: 0.8rem; font-weight: 600;
}
.stApp [class*="st-key-nav_"] button {
    width: 100%; min-height: 2.4rem; border: none; box-shadow: none; transform: none;
    background: transparent; color: #3C5A40; border-radius: 12px;
}
[class*="st-key-nav_"] button p { white-space: nowrap; margin: 0; font-size: 0.95rem; }
.stApp [class*="st-key-nav_"] button:hover { background: #EAF4EB; color: #1B5E20; transform: none; box-shadow: none; }
.stApp [class*="st-key-nav_"] button[kind="primary"],
.stApp [class*="st-key-nav_"] button[data-testid="stBaseButton-primary"] { background: #DDEFDF; color: #1B5E20 !important; }

/* Green banner at the top of every page */
.page-header {
    position: relative; overflow: hidden; color: white; margin-bottom: 1.2rem;
    background: linear-gradient(120deg, #14693A, #2E7D32 55%, #66BB6A);
    padding: 1.8rem 2rem; border-radius: 22px; box-shadow: 0 6px 16px rgba(46, 125, 50, 0.25);
}
.page-header::after {
    content: ""; position: absolute; right: -60px; top: -60px;
    width: 240px; height: 240px; border-radius: 50%; background: rgba(255, 255, 255, 0.12);
}
.page-badge {
    display: inline-block; background: rgba(255, 255, 255, 0.2); border-radius: 20px;
    padding: 0.2rem 0.8rem; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em;
}
.page-header h1 { color: white !important; margin: 0.6rem 0 0.2rem 0; padding: 0; font-size: 2.2rem; }
.page-header p { margin: 0; opacity: 0.92; color: white !important; }

/* White rounded cards */
.metric-card, [data-testid="stVerticalBlockBorderWrapper"] {
    background: white; border: 1px solid #DCEBDD; border-radius: 18px;
}
.metric-card { padding: 1.1rem 1.3rem; margin-bottom: 1rem; min-height: 110px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); }
.metric-value { color: #1B7F46; font-size: 1.7rem; font-weight: 800; line-height: 1.3; }
.metric-title { color: #5F7A64; font-size: 0.85rem; margin-top: 0.2rem; }
.metric-note { color: #8FA394; font-size: 0.75rem; }

/* Buttons: same size and shape everywhere, main buttons are green */
.stButton button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button {
    min-height: 2.8rem; padding: 0.5rem 1.5rem; border-radius: 12px; font-weight: 600;
}
button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
    background: linear-gradient(90deg, #2E7D32, #43A047); border: none; color: white !important;
}
</style>
"""


def apply_page_style():
    st.markdown(PAGE_STYLE, unsafe_allow_html=True)


def show_page_header(title, subtitle):
    """The green banner at the top of every page."""
    st.markdown('<div class="page-header"><span class="page-badge">🌿 COMMUNITY FOOD DONATION</span>'
                "<h1>" + title + "</h1><p>" + subtitle + "</p></div>", unsafe_allow_html=True)


def show_metric_card(title, value, note=""):
    """One rounded card: a big number with a small title under it."""
    st.markdown('<div class="metric-card"><div class="metric-value">' + str(value) + "</div>"
                '<div class="metric-title">' + title + '</div><div class="metric-note">' + note + "</div></div>",
                unsafe_allow_html=True)


def format_number(value):
    """Show 40.0 as '40' and 2.5 as '2.5'."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 2))


def format_units(totals, field):
    """Turn the totals list into text like '190 kg<br>225 piece' (units are never added together)."""
    if len(totals) == 0:
        return "0"
    lines = []
    for row in totals:
        lines.append(format_number(row[field]) + " " + row["unit"])
    return "<br>".join(lines)


def show_table(records, column_labels):
    """Show a list of dictionaries as a table with the given column titles."""
    if len(records) == 0:
        st.info("No records to show.")
        return
    rows = []
    for record in records:
        row = {}
        for field, label in column_labels.items():
            row[label] = record[field]
        rows.append(row)
    st.dataframe(rows, hide_index=True)
