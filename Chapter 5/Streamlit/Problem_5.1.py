import streamlit as st 

st.set_page_config(page_title="Reservoir Economic Value per Acre-Foot", layout = "centered")

st.title("💵 Reservoir Economic Value Calculator")
st.markdown("Estimate Gas & Condensate Revenue per Acre-foot using Recovery Factors and Prices.")

# Inputs
gas_in_place = st.number_input("Gas in pace (Mscf/ac-ft)", value = 1300.0)
gas_recovery = st.slider("Gas recovery factor", 0.0, 1.0, 0.85)
gas_price = st.number_input("Gas price ($/STB)", value = 6.0)

cond_in_place = st.number_input("Condensate in place (STB/ac-ft)", value = 115.0)
cond_recovery = st.slider("Condensate recovery factor", 0.0, 1.0, 0.58)
cond_price = st.number_input("Condensate price ($/STB)", value = 95.0)

# Calculation
recovered_gas = gas_in_place * gas_recovery
recovered_cond = cond_in_place * cond_recovery

gas_revenue = recovered_gas * gas_price
cond_revenue = recovered_cond * cond_price
total_revenue = gas_revenue + cond_revenue

# Output
st.subheader("📈 Results")
st.write(f"**Recovered Gas:** {recovered_gas:.2f} Mscf")
st.write(f"**Gas Revenue:** ${gas_revenue:,.2f}")
st.write(f"**Recovered Condensate:** {recovered_cond:.2f} STB")
st.write(f"**Condensate Revenue:** ${cond_revenue:,.2f}")
st.success(f"**Total Reserve Value per ac-ft: ${total_revenue:,.2f}**")