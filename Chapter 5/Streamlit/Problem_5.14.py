import streamlit as st

 
def res_vol_from_stb_cond(api_gravity, res_pressure_psia, res_temp_f, gas_gravity, z_factor=0.83):
    R = 10.7316             # psia·ft³ / (lbmol·°R)
    STB_to_ft3 = 5.615      # 1 STB = 5.615 ft³
    H20_density = 62.4      # lb/ft³
    
    sg_cond = 141.5 / (api_gravity + 131.5)     # Convert API to SG
    MW_cond = 424 * sg_cond                     # Estimate MW of condensate vapor
    density_cond = sg_cond * H20_density        # Calculate density of 1 STB (lb/ft³)
    mass_cond = density_cond * STB_to_ft3       # Calculate mass of 1 STB (lb)
    n_moles = mass_cond / MW_cond               # Moles of condensate vapor
    temp_R = res_temp_f + 459.67                # Convert temperature to Rankine    
    
    vol_ft3 = (n_moles * R * temp_R) / (res_pressure_psia * z_factor)   # Apply Real Gas Law to find volume
    return round(vol_ft3, 3)

st.title("Condensate Reservoir Volume Calculator")

api = st.number_input("Condensate API Gravity", value = 55.0)
pressure = st.number_input("Reservoir Pressure (psia)", value = 2740.0)
temp = st.number_input("Reservoir Temperature (°F)", value = 215.0)
gas_gravity = st.number_input("Gas Gravity", value = 0.76)
z = st.number_input("Z-Factor", value = 0.83)

if st.button("Calculate Volume"):
    result = res_vol_from_stb_cond(api, pressure, temp, gas_gravity, z)
    st.success(f"Reservoir gas volume for 1 STB of condensate: {result} ft³")
