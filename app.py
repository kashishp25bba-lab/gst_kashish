
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="GST Rate Finder & Calculator",
    page_icon="🧾",
    layout="wide"
)

# ---------------- CSS DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f5f9fc;
}
.main-title {
    color: #155e75;
    font-size: 34px;
    font-weight: bold;
}
.subtitle {
    color: #526777;
}
div.stButton > button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------
DB_PATH = Path(__file__).parent / "gst_data.csv"

def load_data():
    try:
        data = pd.read_csv(DB_PATH)
        required = [
            "product_name", "gst_rate",
            "applicability_status", "hsn_code",
            "source_name", "source_url", "last_verified"
        ]
        if not all(col in data.columns for col in required):
            st.error("GST database has an incorrect format.")
            return pd.DataFrame()
        return data
    except Exception:
        st.error("Unable to load GST database.")
        return pd.DataFrame()

data = load_data()

# ---------------- SESSION STATE ----------------
if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if "searched_product" not in st.session_state:
    st.session_state.searched_product = ""

if "calc_rate" not in st.session_state:
    st.session_state.calc_rate = 18.0

def clear_search():
    st.session_state.search_text = ""
    st.session_state.searched_product = ""

def reset_app():
    st.session_state.search_text = ""
    st.session_state.searched_product = ""
    st.session_state.calc_rate = 18.0

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">GST Rate Finder & GST Calculator</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Find GST information and calculate GST easily.</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "🔍 GST Rate Finder",
    "🧮 GST Calculator",
    "ℹ️ About & Sources"
])

# ============================================================
# TAB 1: GST RATE FINDER
# ============================================================
with tab1:

    st.subheader("Find GST Rate")

    product = st.text_input(
        "Enter Product Name",
        key="search_text",
        placeholder="Example: Mobile Phone"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        search_clicked = st.button(
            "🔍 Search",
            use_container_width=True
        )

    with col2:
        st.button(
            "Clear",
            on_click=clear_search,
            use_container_width=True
        )

    with col3:
        st.button(
            "Reset",
            on_click=reset_app,
            use_container_width=True
        )

    if search_clicked:
        if not product.strip():
            st.warning("Please enter a product name.")
            st.session_state.searched_product = ""
        else:
            st.session_state.searched_product = product.strip()

    if st.session_state.searched_product:

        search_name = st.session_state.searched_product

        if not data.empty:
            matches = data[
                data["product_name"].astype(str).str.contains(
                    search_name, case=False, na=False, regex=False
                )
            ]

            if not matches.empty:
                st.success("Product information found!")

                for _, item in matches.iterrows():

                    try:
                        rate = float(item["gst_rate"])
                        valid_rate = 0 <= rate <= 100
                    except (ValueError, TypeError):
                        valid_rate = False
                        rate = None

                    st.markdown("### Product Details")
                    st.write("**Product Name:**", item["product_name"])

                    if valid_rate:
                        st.write(f"**GST Rate:** {rate:g}%")
                        if st.button(
                            "Use this rate in GST Calculator",
                            key=f"use_{item.name}"
                        ):
                            st.session_state.calc_rate = rate
                            st.success("Rate selected. Open the Calculator tab.")
                    else:
                        st.warning("GST rate is not verified or valid.")

                    st.write(
                        "**GST Applicability:**",
                        item["applicability_status"]
                    )
                    st.write("**HSN Code:**", item["hsn_code"])
                    st.write("**Source:**", item["source_name"])

                    if pd.notna(item["source_url"]) and str(item["source_url"]).startswith("https://"):
                        st.markdown(
                            f"[View Official Source]({item['source_url']})"
                        )

                    st.write(
                        "**Last Verified:**",
                        item["last_verified"]
                    )
                    st.divider()

            else:
                st.error(
                    "Product not found in our verified database. "
                    "Please check the product name or consult the official GST sources."
                )
        else:
            st.warning(
                "The GST database is currently empty. "
                "Add verified product records to gst_data.csv."
            )

# ============================================================
# TAB 2: GST CALCULATOR
# ============================================================
with tab2:

    st.subheader("Calculate GST")

    st.write("Enter the price and applicable GST rate.")

    price = st.number_input(
        "Product Price (₹)",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )

    gst_rate = st.number_input(
        "GST Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(st.session_state.calc_rate),
        step=0.5,
        key="calc_rate"
    )

    transaction = st.radio(
        "Select Transaction Type",
        ["Intra-State", "Inter-State"],
        horizontal=True
    )

    if st.button("Calculate GST", type="primary"):

        gst_amount = price * gst_rate / 100
        final_price = price + gst_amount

        st.markdown("### Calculation Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Product Price", f"₹{price:,.2f}")

        with col2:
            st.metric("Total GST", f"₹{gst_amount:,.2f}")

        if transaction == "Intra-State":

            cgst = gst_amount / 2
            sgst = gst_amount / 2

            st.write(f"**CGST ({gst_rate/2:g}%):** ₹{cgst:,.2f}")
            st.write(f"**SGST ({gst_rate/2:g}%):** ₹{sgst:,.2f}")

        else:
            st.write(f"**IGST ({gst_rate:g}%):** ₹{gst_amount:,.2f}")

        st.success(f"Final Price Including GST: ₹{final_price:,.2f}")

        st.caption(
            "Calculation assumes the entered price is exclusive of GST. "
            "Confirm the applicable rate and tax treatment before invoicing."
        )

# ============================================================
# TAB 3: ABOUT AND OFFICIAL SOURCES
# ============================================================
with tab3:

    st.subheader("About This Application")

    st.write("""
    GST Rate Finder & GST Calculator is an application designed
    to help Indian businesses and consumers:

    - Search for GST rates of products.
    - Check GST applicability.
    - Find HSN codes.
    - View official government sources.
    - Calculate CGST, SGST and IGST.
    - Calculate the final price including GST.
    """)

    st.subheader("Official GST Sources")

    st.markdown(
        "- [CBIC GST Rate Schedule](https://cbic-gst.gov.in/hindi/gst-goods-services-rates.html)"
    )
    st.markdown(
        "- [CBIC Tax Information Portal](https://taxinformation.cbic.gov.in/)"
    )
    st.markdown(
        "- [GST Portal HSN/SAC Search Guide](https://tutorial.gst.gov.in/userguide/taxpayersdashboard/Search_HSN_SAC_Tax_Rates.htm)"
    )

    st.info(
        "GST rates and HSN classifications can depend on the exact "
        "product description, classification and applicable notifications. "
        "Always verify the latest official notification."
    )

st.divider()
st.caption("GST Rate Finder & GST Calculator | India")
