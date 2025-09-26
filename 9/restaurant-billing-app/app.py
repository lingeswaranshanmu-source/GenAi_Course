# app.py
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from fpdf import FPDF

from utils.menu import MENU

st.set_page_config(page_title="Restaurant Billing", page_icon="🍔", layout="wide")

# --- Helpers ---
def get_menu_item(item_id):
    for it in MENU:
        if it["id"] == item_id:
            return it
    return None

def cart_to_dataframe(cart):
    if not cart:
        return pd.DataFrame(columns=["Item", "Qty", "Price", "Subtotal"])
    rows = []
    for item_id, qty in cart.items():
        it = get_menu_item(item_id)
        subtotal = qty * it["price"]
        rows.append({"Item": it["name"], "Qty": qty, "Price": it["price"], "Subtotal": subtotal})
    df = pd.DataFrame(rows)
    return df

def compute_bill(df, tax_rate_percent):
    subtotal = float(df["Subtotal"].sum()) if not df.empty else 0.0
    tax = round(subtotal * (tax_rate_percent / 100.0), 2)
    total = round(subtotal + tax, 2)
    return round(subtotal, 2), tax, total

def generate_csv_bytes(df, subtotal, tax, total, meta):
    out = BytesIO()
    header_lines = [
        f"Invoice for:,{meta.get('restaurant_name','')}",
        f"Date:,{meta.get('date','')}",
        "",
    ]
    out.write("\n".join(header_lines).encode("utf-8"))
    df_out = df.copy()
    df_out["Price"] = df_out["Price"].map(lambda v: f"{v:.2f}")
    df_out["Subtotal"] = df_out["Subtotal"].map(lambda v: f"{v:.2f}")
    df_out.to_csv(out, index=False)
    out.write(b"\n")
    summary_lines = [
        f"Subtotal:,,{subtotal:.2f}",
        f"Tax ({meta.get('tax_rate',0)}%):,,{tax:.2f}",
        f"Total:,,{total:.2f}",
    ]
    out.write("\n".join(summary_lines).encode("utf-8"))
    out.seek(0)
    return out

def generate_pdf_bytes(df, subtotal, tax, total, meta):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 8, meta.get("restaurant_name", "Restaurant"), ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, meta.get("restaurant_address", ""), ln=True)
    pdf.ln(4)
    pdf.cell(0, 6, f"Invoice Date: {meta.get('date')}", ln=True)
    pdf.cell(0, 6, f"Invoice No: {meta.get('invoice_no')}", ln=True)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(80, 8, "Item", border=1)
    pdf.cell(25, 8, "Qty", border=1, align="R")
    pdf.cell(30, 8, "Price", border=1, align="R")
    pdf.cell(35, 8, "Subtotal", border=1, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", size=10)
    for _, row in df.iterrows():
        pdf.cell(80, 8, str(row["Item"]), border=1)
        pdf.cell(25, 8, str(int(row["Qty"])), border=1, align="R")
        pdf.cell(30, 8, f"{row['Price']:.2f}", border=1, align="R")
        pdf.cell(35, 8, f"{row['Subtotal']:.2f}", border=1, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(135, 8, "Subtotal", border=0)
    pdf.cell(35, 8, f"{subtotal:.2f}", border=1, align="R")
    pdf.ln()
    pdf.cell(135, 8, f"Tax ({meta.get('tax_rate')}%)", border=0)
    pdf.cell(35, 8, f"{tax:.2f}", border=1, align="R")
    pdf.ln()
    pdf.cell(135, 8, "Total", border=0)
    pdf.cell(35, 8, f"{total:.2f}", border=1, align="R")
    pdf.ln(12)
    pdf.set_font("Helvetica", size=9)
    pdf.multi_cell(0, 5, meta.get("footer_note", "Thank you for your order!"))

    out = BytesIO()
    pdf.output(out)
    out.seek(0)
    return out

# --- Init session state ---
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "tax_rate" not in st.session_state:
    st.session_state.tax_rate = 5.0
if "restaurant_name" not in st.session_state:
    st.session_state.restaurant_name = "My Restaurant"
if "restaurant_address" not in st.session_state:
    st.session_state.restaurant_address = "123, Example Street"

# --- Layout ---
st.title("🍔 Restaurant Order & Billing")

left, right = st.columns([2, 1])

with left:
    st.header("Menu")
    for item in MENU:
        cols = st.columns([6, 1, 1])
        with cols[0]:
            st.markdown(f"**{item['name']}**  \nPrice: {item['price']:.2f}")
        with cols[1]:
            if st.button("+", key=f"add_{item['id']}"):
                st.session_state.cart[item["id"]] = st.session_state.cart.get(item["id"], 0) + 1
        with cols[2]:
            if st.button("-", key=f"sub_{item['id']}"):
                if st.session_state.cart.get(item["id"], 0) > 0:
                    st.session_state.cart[item["id"]] -= 1
                    if st.session_state.cart[item["id"]] <= 0:
                        del st.session_state.cart[item["id"]]

with right:
    st.header("Order Cart")
    cart_df = cart_to_dataframe(st.session_state.cart)
    if cart_df.empty:
        st.info("Cart is empty. Add items from the menu.")
    else:
        for idx, row in cart_df.iterrows():
            item_name = row["Item"]
            item_id = next((it["id"] for it in MENU if it["name"] == item_name), None)
            cols = st.columns([3, 2, 1])
            with cols[0]:
                st.write(f"**{item_name}**")
            with cols[1]:
                new_qty = st.number_input(
                    f"Qty_{item_id}",
                    min_value=0,
                    value=int(st.session_state.cart[item_id]),
                    step=1,
                    key=f"qty_{item_id}",
                )
                if new_qty != st.session_state.cart[item_id]:
                    if new_qty <= 0:
                        del st.session_state.cart[item_id]
                    else:
                        st.session_state.cart[item_id] = int(new_qty)
                    st.rerun()
            with cols[2]:
                if st.button("Remove", key=f"rem_{item_id}"):
                    if item_id in st.session_state.cart:
                        del st.session_state.cart[item_id]
                        st.rerun()

    st.markdown("---")
    st.number_input("Tax rate (%)", min_value=0.0, value=float(st.session_state.tax_rate), step=0.1, key="tax_rate_input")
    st.session_state.tax_rate = float(st.session_state.tax_rate_input)

    st.subheader("Bill Summary")
    df = cart_df.copy()
    subtotal, tax, total = compute_bill(df, st.session_state.tax_rate)
    st.write(f"Subtotal: **{subtotal:.2f}**")
    st.write(f"Tax ({st.session_state.tax_rate:.2f}%): **{tax:.2f}**")
    st.write(f"Total: **{total:.2f}**")

    st.markdown("### Export Invoice")
    meta = {
        "restaurant_name": st.session_state.restaurant_name,
        "restaurant_address": st.session_state.restaurant_address,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "invoice_no": datetime.now().strftime("%Y%m%d%H%M%S"),
        "tax_rate": st.session_state.tax_rate,
        "footer_note": "Thank you for dining with us!",
    }

    if not df.empty:
        csv_buf = generate_csv_bytes(df, subtotal, tax, total, meta)
        st.download_button(
            label="Download CSV Invoice",
            data=csv_buf,
            file_name=f"invoice_{meta['invoice_no']}.csv",
            mime="text/csv",
        )
        pdf_buf = generate_pdf_bytes(df, subtotal, tax, total, meta)
        st.download_button(
            label="Download PDF Invoice",
            data=pdf_buf,
            file_name=f"invoice_{meta['invoice_no']}.pdf",
            mime="application/pdf",
        )

    if st.button("Clear Cart"):
        st.session_state.cart = {}
        st.rerun()
