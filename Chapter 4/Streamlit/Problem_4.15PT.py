import streamlit as st

def estimate_water_vapor_content(P_res, T_res_f):
    """
    Estimate water vapor content (bbl/MMscf) at given pressure.
    This is a simplified linear interpolation based on 0.86 bbl/MMscf at 6000 psia.
    """    
    
    return 0.86 * (P_res / 6000)

def calc_tot_gas_equiv(sep_gas_mmscf, cond_stb, freshwater_bbl,
                       cond_gas_equiv_mscf_per_stb,
                       water_vapor_content_bbl_per_mmscf,
                       stock_tank_gas_mscf):
    
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
st.set_page_config(page_title = "PT-Aware Gas Equivalent Calculator", layout = "centered")
st.title("🧪 Daily Gas Production Equivalent Calculator")

st.sidebar.header("Input Production Data")

separator_gas = st.sidebar.number_input("Separator Gas Production (MMSCF)", value = 6.0, step = 0.1)
condensate = st.sidebar.number_input("Condensate Production (STB)", value = 100, step = 10)
freshwater = st.sidebar.number_input("Freshwater Production (bbl)", value = 10.0, step = 1.0)
stock_tank_gas = st.sidebar.number_input("Stock Tank Gas (MSCF)", value = 21.0, step = 1.0)

st.sidebar.header ("Reservoir Conditions")
initial_pressure = st.sidebar.number_input("Initial Reservoir Pressure (psia)", value = 6000, step = 100)
current_pressure = st.sidebar.number_input("Current Reservoir Pressure (psia)", value = 2000, step = 100)
temperature = st.sidebar.number_input("Reservoir Temperature (°F)", value = 225.0, step = 1.0)

st.sidebar.header("Other Setting")
condensate_gas_equiv_factor = st.sidebar.number_input("Condensate Gas Equivalent (MSCF/STB)", value = 6.0, step = 0.1)

# Estimated water vapor content dynamically
estimated_H20_vapor_content = estimate_water_vapor_content(current_pressure, temperature)

st.markdown(f"💧 **Estimated Water Vapor Content** at {current_pressure} psia and {temperature} °F:"
            f"**{estimated_H20_vapor_content:.3f} bbl/MMSCF**")

# Results
results = calc_tot_gas_equiv(
    sep_gas_mmscf = separator_gas,
    cond_stb = condensate,
    freshwater_bbl = freshwater,
    cond_gas_equiv_mscf_per_stb = condensate_gas_equiv_factor,
    water_vapor_content_bbl_per_mmscf = estimated_H20_vapor_content,
    stock_tank_gas_mscf = stock_tank_gas
)

st.subheader("📊 Results")    
for key, value in results.items():
    st.metric(label = key, value = f"{value:.3f} MMSCF") 

st.caption("Now even more fancy with PT! Prepared by Noraeen 👷‍♀️🔥")
