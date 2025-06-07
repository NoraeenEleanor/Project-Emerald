import streamlit as st 
import pandas as pd
import plotly.graph_objects as go 

# Title
st.markdown("## 📈 Z-Factor & Gas Formation Volume Factor (Bg) vs Pressure")

uploaded_file = st.file_uploader("📂 Upload your Z-Factor & Bg Data CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    expected_cols = ['Pressure (psia)', 'Z-Factor', 'Bg (ft³/SCF)']
    if all(col in df.columns for col in expected_cols):
        # Expected columns
        pressures = df['Pressure (psia)']
        z_factors = df['Z-Factor']
        bg_values = df[ 'Bg (ft³/SCF)']
        
        # -- Dual Axis Plot: Z-Factor and Bg --
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x = pressures, y = z_factors,
            name = 'Z-Factor',
            mode = 'lines+markers',
            line = dict(color = 'blue'),
            yaxis = 'y1'
        ))
        
        fig.add_trace(go.Scatter(
            x = pressures, y = bg_values,
            name = 'Bg (ft³/SCF)',
            mode = 'lines+markers',
            line = dict(color = 'green', dash = 'dash'),
            yaxis = 'y2' 
        ))
        
        fig.update_layout(
            xaxis = dict(title = 'Pressure (psia)'),
            yaxis = dict(title = 'Z-Factor', color = 'blue'),
            yaxis2 = dict(title = 'Bg (ft³/SCF)', overlaying = 'y', side = 'right', color = 'green'),
            legend = dict(x = 0.05, y = 1.05, orientation = 'h'),
            height = 500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- Compressiibility Factor Calculation (Cg) (Optional)
        st.markdown("### Gas Compressibility (Cg) vs Pressure")
        df['Cg (1/psi)'] = -df['Z-Factor'].diff() / df['Pressure (psia)'].diff()
        
        fig_cg = go.Figure()
        fig_cg.add_trace(go.Scatter(
            x = df['Pressure (psia)'],
            y = df['Cg (1/psi)'],
            mode = 'lines+markers',
            line = dict(color = 'purple')
        ))
        
        fig_cg.update_layout(
            xaxis_title = 'Pressure (psia)',
            yaxis_title = 'Cg (1/psi)',
            height = 400
        )
        
        st.plotly_chart(fig_cg, use_container_width=True)
        
        # --- Show Final Table with Cg ---
        with st.expander("📊 Show Full Table with Cg"):
            st.dataframe(df, use_container_width=True)
            
        # --- Download Button ---
        csv_download = df.to_csv(index = False).encode('utf-8')
        st.download_button(
            label = "📥 Download Full Table as CSV",
            data = csv_download,
            file_name = "zfactor_bg_cg_data.csv",
            mime = "text/csv"
        )
    else:
        st.warning("⚠️ CSV must contain: 'Pressure (psia)', 'Z-Factor', 'Bg (ft³/SCF)'")
else:
    st.info("👈 Upload your CSV to begin visualizing PVT results!")