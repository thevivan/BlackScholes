import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from model import PricingModel

# Page setup
im = Image.open("data/favicon.ico")
st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        .designer-tag a {
            text-decoration: none;
            color: #888;
        }
        .designer-tag a:hover {
            color: #333;
        }
        .subtle-metric {
            font-size: 16px;
            color: #555;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar input
with st.sidebar:
    st.write("`Created by:`")
    linkedin_url = "https://www.linkedin.com/in/vivan-v/"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Vivan Vasudeva`</a>', unsafe_allow_html=True)

    st.title("Parameters")
    spot_price = st.number_input("Spot Price (£)", value=10.0, step=0.5)
    strike_price = st.number_input("Strike Price (£)", value=10.0, step=0.5)
    time_to_expiry = st.number_input("Time to Expiry (Years)", value=1.5, format="%.2g", step=0.1)
    volatility = st.number_input("Volatility (σ)", value=0.2, format="%.2g")
    risk_free_rate_percentage = st.number_input("Risk-Free Rate (%)", value=5.0, step=0.1, format="%.2g")
    risk_free_rate = risk_free_rate_percentage / 100
    
    # Perspective toggle
    perspective = st.radio("Perspective", ["Buy", "Sell"])

    st.markdown("---")
    st.subheader("Heatmap Settings")
    spot_min = st.number_input('Min Spot Price', min_value=0.01, value=spot_price * 0.8, step=0.50)
    spot_max = st.number_input('Max Spot Price', min_value=0.01, value=spot_price * 1.2, step=0.50)
    vol_min = st.slider('Min Volatility', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)
    vol_max = st.slider('Max Volatility', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)

    spot_range = np.linspace(max(spot_price * 0.8, spot_price - 5), min(spot_price * 1.2, spot_price + 5), 9)
    vol_range = np.linspace(max(volatility * 0.5, volatility - 0.1), min(volatility * 1.5, volatility + 0.1), 9)

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
        cmap_call = "RdYlGn_r"
        cmap_put = "RdYlGn_r"
    else:
        cmap_call = "RdYlGn"
        cmap_put = "RdYlGn"

    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_data, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=cmap_call, ax=ax_call)
    ax_call.set_xlabel('Spot Price (£)')
    ax_call.set_ylabel('Volatility (σ)')

    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_data, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap=cmap_put, ax=ax_put)
    ax_put.set_xlabel('Spot Price (£)')
    ax_put.set_ylabel('Volatility (σ)')

    return fig_call, fig_put

# Main content
st.title("**The** Black-Scholes **Model**")
st.markdown('<p style="font-style: italic; font-size: 15px;color: #777;">An option-pricing tool to visualise the values of put and call options for various parameters.</p>', unsafe_allow_html=True)

# Calculate prices and Greeks
st.markdown('<p style="font-size: 15px;color: #eee;"></p>', unsafe_allow_html=True)
option_model = PricingModel(time_to_expiry, strike_price, spot_price, volatility, risk_free_rate)
call_price, put_price = option_model.calculate()

st.markdown(f'<p style="font-size: 15px;">If we assume a derivative has a <i><b>strike price</b></i> of £{strike_price:.2f} in {time_to_expiry:.2g} year(s), a <i><b>volatility</b></i> of {volatility:.2g}, and that the <i><b>current risk-free rate</i></b> is {risk_free_rate_percentage:.2g}%...</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size: 15px;">...then while the underlying stock trades at a <i><b>spot price</i></b> of £{spot_price:.2f}, its derivative should cost&thinsp;:</p>', unsafe_allow_html=True)

# Display prices
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="metric-box metric-call">
            <div>
                <div class="metric-value">£{call_price:.2f}</div>
                <div class="metric-label"><i>for a call</i></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box metric-put">
            <div>
                <div class="metric-value">£{put_price:.2f}</div>
                <div class="metric-label"><i>for a put</i></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Displaying Greeks

# st.markdown(f"""
#     <table style="width:100%; margin-top: 10px; border-collapse: collapse; border: none;">
#         <tr style="border: none;">
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Delta (Call):</strong> {option_model.call_delta:.2f}</td>
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Delta (Put):</strong> {option_model.put_delta:.2f}</td>
#         </tr>
#         <tr style="border: none;">
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Theta (Call):</strong> {option_model.call_theta:.2f}</td>
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Theta (Put):</strong> {option_model.put_theta:.2f}</td>
#         </tr>
#         <tr style="border: none;">
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Gamma:</strong> {option_model.gamma:.2f}</td>
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Vega:</strong> {option_model.vega:.2f}</td>
#         </tr>
#         <tr style="border: none;">
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Rho (Call):</strong> {option_model.call_rho:.2f}</td>
#             <td style="text-align: center; font-style: italic; font-size: 20px; border: none;"><strong>Rho (Put):</strong> {option_model.put_rho:.2f}</td>
#         </tr>
#     </table>
# """, unsafe_allow_html=True)


# Display heatmaps
st.markdown("""
    <h5 style="margin-top: 0px;">&nbsp;</h5>
""", unsafe_allow_html=True)
st.info("You can change the parameters on the left to see how this changes across different volatilities and spot prices")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Values (£)")
    fig_call, _ = generate_heatmaps(option_model, spot_range, vol_range, strike_price, perspective)
    st.pyplot(fig_call)

with col2:
    st.subheader("Put Values (£)")
    _, fig_put = generate_heatmaps(option_model, spot_range, vol_range, strike_price, perspective)
    st.pyplot(fig_put)
