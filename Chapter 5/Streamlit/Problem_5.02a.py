"Sample file in Dataset - 5.2a_well_data_template.csv"

import streamlit as st
import pandas as pd

# Title
st.title("🛢️ GOR Calculator App")

# Description
st.markdown("""
This app calculates the **Dry GOR** and **Wet GOR** (SCF/STB) from well production data.  
You can either enter values manually or upload a CSV file with multiple wells.
""")

# GOR Calculation Function
def calculate_gor(condensate_rate_stb, gas_rate_scf, mw_condensate=121.2, z_factor=1.0):
    dry_gor = gas_rate_scf / condensate_rate_stb
    scf_per_stb_condensate = (379.4 * z_factor) / mw_condensate
    vaporized_condensate_scf = scf_per_stb_condensate * condensate_rate_stb
    wet_gor = (gas_rate_scf + vaporized_condensate_scf) / condensate_rate_stb
    return dry_gor, wet_gor

# Sidebar Inputs
st.sidebar.header("🧮 Manual Input")

condensate = st.sidebar.number_input("Condensate Rate (STB/day)", value=45.3)
gas_rate = st.sidebar.number_input("Sales Gas Rate (SCF/day)", value=742000)
mw = st.sidebar.number_input("Condensate Molecular Weight", value=121.2)
z = st.sidebar.number_input("Gas Compressibility Factor (z)", value=1.0)

if st.sidebar.button("Calculate GOR"):
    dry, wet = calculate_gor(condensate, gas_rate, mw, z)
    st.success(f"Dry GOR: {dry:,.0f} SCF/STB")
    st.success(f"Wet GOR: {wet:,.0f} SCF/STB")

# File Upload Section
st.markdown("### 📤 Upload CSV for Batch Calculation")
uploaded_file = st.file_uploader("Upload CSV (columns: Condensate_STB, Gas_SCF, MW, Z)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Dry_GOR'], df['Wet_GOR'] = zip(*df.apply(
        lambda row: calculate_gor(row['Condensate_STB'], row['Gas_SCF'], row['MW'], row['Z']), axis=1)
    )
    st.dataframe(df)

    # Downloadable result
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="gor_results.csv", mime="text/csv")
