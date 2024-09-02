import streamlit as st
import numpy as np
from model import generate_heatmap

def main():
    st.set_page_config(page_title="Black-Scholes Model Visualization")
    st.title("Black-Scholes Model Visualization")
    
    K = st.number_input("Strike Price", value=100.0)
    T = st.number_input("Time to Expiration (in years)", value=1.0)
    r = st.number_input("Risk-free Interest Rate", value=0.05)
    
    S_min = st.number_input("Minimum Spot Price", value=80.0)
    S_max = st.number_input("Maximum Spot Price", value=120.0)
    S_step = st.number_input("Spot Price Step", value=5.0)
    
    sigma_min = st.number_input("Minimum Volatility", value=0.1)
    sigma_max = st.number_input("Maximum Volatility", value=0.6)
    sigma_step = st.number_input("Volatility Step", value=0.05)
    
    option_type = st.selectbox("Option Type", ["call", "put"])
    
    S_range = np.arange(S_min, S_max + S_step, S_step)
    sigma_range = np.arange(sigma_min, sigma_max + sigma_step, sigma_step)
    
    if st.button("Generate Heatmap"):
        fig = generate_heatmap(S_range, sigma_range, K, T, r, option_type)
        st.pyplot(fig)

if __name__ == "__main__":
    main()