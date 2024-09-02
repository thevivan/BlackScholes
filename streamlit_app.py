import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from model import PricingModel  # Import the PricingModel class from model.py

# Page setup
st.set_page_config(
    page_title="Option Pricing Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .metric-box {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            font-size: 30px;
            font-weight: bold;
            color: #333;
        }
        .metric-call {
            background-color: #c2ccff;
            color: #5670f5;
        }
        .metric-put {
            background-color: #ffd191;
            color: #663c00;
        }
        .metric-label {
            font-size: 20px;
            font-weight: normal;
            margin-bottom: 5px;
        }
        .designer-tag {
            font-size: 16px;
            color: #888;
            text-align: right;
            margin-top: -20px;
            margin-bottom: 10px;
        }
        .subtle-metric {
            font-size: 16px;
            color: #555;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Designer tag
st.markdown('<div class="designer-tag">Designed by Vivan Vasudeva</div>', unsafe_allow_html=True)

# Sidebar input
with st.sidebar:
    st.title("Parameters")
    spot_price = st.number_input("Spot Price", value=100.0, step=0.05)
    strike_price = st.number_input("Strike Price", value=100.0, step=0.05)
    time_to_expiry = st.number_input("Time to Expiry (Years)", value=1.0)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    risk_free_rate = st.number_input("Risk-Free Rate", value=0.05)
    
    # Perspective toggle
    perspective = st.radio("Perspective", ["Buy", "Sell"])

    st.markdown("---")
    st.subheader("Heatmap Settings")
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=spot_price * 0.8, step=0.01)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=spot_price * 1.2, step=0.01)
    vol_min = st.slider('Min Volatility', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)
    vol_max = st.slider('Max Volatility', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)

    spot_range = np.linspace(spot_min, spot_max, 10)
    vol_range = np.linspace(vol_min, vol_max, 10)

# Heatmap generation
def generate_heatmaps(model, spot_range, vol_range, strike_price, perspective):
    call_data = np.zeros((len(vol_range), len(spot_range)))
    put_data = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            temp_model = PricingModel(time=model.time, strike=strike_price, spot=spot, vol=vol, rate=model.rate)
            temp_model.calculate()
            call_data[i, j] = temp_model.call_price
            put_data[i, j] = temp_model.put_price

    if perspective == "Buy":
        cmap_call = "RdYlGn"
        cmap_put = "RdYlGn"
    else:
        cmap_call = "RdYlGn_r"
        cmap_put = "RdYlGn_r"

    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_data, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=cmap_call, ax=ax_call)
    ax_call.set_title('Call Option Prices')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_data, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=cmap_put, ax=ax_put)
    ax_put.set_title('Put Option Prices')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put

# Main content
st.title("Black-Scholes Option Pricing")

# Calculate prices and Greeks
option_model = PricingModel(time_to_expiry, strike_price, spot_price, volatility, risk_free_rate)
call_price, put_price = option_model.calculate()

# Display prices prominently
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="metric-box metric-call">
            <div>
                <div class="metric-label">Call Price</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box metric-put">
            <div>
                <div class="metric-label">Put Price</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Display Vega, Vanna, and Volga less prominently
st.markdown(f"""
    <table style="width:100%; margin-top: 10px; border-collapse: collapse; border: none;">
        <tr style="border: none;">
            <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Vega:</strong> {option_model.vega:.2f}</td>
            <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Vanna:</strong> {option_model.vanna:.2f}</td>
            <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Volga:</strong> {option_model.volga:.2f}</td>
        </tr>
    </table>
""", unsafe_allow_html=True)



# Display heatmaps
st.markdown("""
    <h5 style="margin-top: 0px;">&nbsp;</h5>
""", unsafe_allow_html=True)
st.info("Analyse how the prices change with varying spot prices and volatilities.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Option Heatmap")
    fig_call, _ = generate_heatmaps(option_model, spot_range, vol_range, strike_price, perspective)
    st.pyplot(fig_call)

with col2:
    st.subheader("Put Option Heatmap")
    _, fig_put = generate_heatmaps(option_model, spot_range, vol_range, strike_price, perspective)
    st.pyplot(fig_put)
