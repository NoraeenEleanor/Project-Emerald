import streamlit as st

def calc_tot_gas_equiv(sep_gas_mmscf, cond_stb, freshwater_bbl,
                       cond_gas_equiv_mscf_per_stb = 6,
                       water_vapor_content_bbl_per_mmscf = 0.86,
                       stock_tank_gas_mscf = 0):
    
    # Convert condensate to gas equivalnt (MMSCF)
    cond_gas_equiv = (cond_stb * cond_gas_equiv_mscf_per_stb) / 1000 # to MMSCF
    
    # Convert water to gas equivalent (MMSCF)
    water_gas_equiv = freshwater_bbl / water_vapor_content_bbl_per_mmscf
    
    # Convert stock tank gas from MSCF to MMSCF
    stock_tank_gas_mmscf = stock_tank_gas_mscf / 1000
    
    # Total gas production
    total_gas_equiv = sep_gas_mmscf + cond_gas_equiv + water_gas_equiv + stock_tank_gas_mmscf
    
    return {
        "Separator Gas (MMSCF)": sep_gas_mmscf,
        "Condensate Gas Equivalent (MMSCF)": cond_gas_equiv,
        "Water Gas Equivalent (MMSCF)": water_gas_equiv,
        "Stock Tank Gas (MMSCF)": stock_tank_gas_mmscf,
        "Total Daily Gas Equivalent (MMSCF)": total_gas_equiv  
    }
    
# Streamlit UI
st.set_page_config(page_title = "Daily Gas Equivalent Calcualtor", layout = "centered")
st.title("🌟 Daily Gas Production Equivalent Calculator")

st.sidebar.header("Input Production Data")

separator_gas = st.sidebar.number_input("Separator Gas Production (MMSCF)", value = 6.0, step = 0.1)
condensate = st.sidebar.number_input("Condensate Production (STB)", value = 100, step = 10)
freshwater = st.sidebar.number_input("Freshwater Production (STB)", value = 10.0, step = 1.0)
stock_tank_gas = st.sidebar.number_input("Stock Tank Gas (MSCF)", value = 21.0, step = 1.0)

st.sidebar.header ("Adcanced Settings")
condensate_gas_equiv_factor = st.sidebar.number_input("Condensate Gas Equivalent (MSCF/STB)", value = 6.0, step = 0.1)
water_vapor_content = st.sidebar.number_input("Water Vapor Content (bbl/MMSCF)", value = 0.86, step = 0.01)

# Results
results = calc_tot_gas_equiv(
    sep_gas_mmscf = separator_gas,
    cond_stb = condensate,
    freshwater_bbl = freshwater,
    cond_gas_equiv_mscf_per_stb = condensate_gas_equiv_factor,
    water_vapor_content_bbl_per_mmscf = water_vapor_content,
    stock_tank_gas_mscf = stock_tank_gas
)

st.subheader("📊 Results")    
for key, value in results.items():
    st.metric(label = key, value = f"{value:.3f} MMSCF") 

st.caption("Prepared by Noraeen 👷‍♀️🔥")
