"""
dashboard.py — the *Streamlit* (web app) interface for the Bill Splitter.

Widgets collect the subtotal, tip %, and party size; the functions in bill.py do
the math; and the results are shown below along with a chart.
"""

import pandas as pd
import streamlit as st

from bill import tip_amount, grand_total, split_evenly, is_generous

st.title("💵 Bill Splitter")

subtotal = st.number_input("Bill subtotal ($)", min_value=0.0, value=50.0, step=1.0)
pct = st.slider("Tip %", min_value=0, max_value=30, value=18)
people = st.number_input("Number of people", min_value=1, value=2, step=1)

tip = tip_amount(subtotal, pct)
total = grand_total(subtotal, pct)
per_person = split_evenly(total, people)

st.write(f"Tip: ${tip:.2f}")
st.write(f"Grand total: ${total:.2f}")
st.write(f"Per person: ${per_person:.2f}")

if is_generous(pct):
    st.success("That's a generous tip! 🎉")
else:
    st.info("Tip 20% or more to be considered generous.")

st.subheader("Per-person cost by tip %")
percents = [10, 15, 18, 20, 25]
chart = pd.DataFrame(
    {"per person": [split_evenly(grand_total(subtotal, p), people) for p in percents]},
    index=[f"{p}%" for p in percents],
)
st.bar_chart(chart)
