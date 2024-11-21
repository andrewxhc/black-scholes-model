import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def black_scholes_merton(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes-Merton price for European options.
    """
    d1 = (np.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price


def main():
    st.title("Option Pricing Heatmap using Black-Scholes-Merton Model")

    st.sidebar.header("Input Parameters")
    K = st.sidebar.number_input("Strike Price (K):", value=100.0, step=1.0)
    T = st.sidebar.number_input("Time to Maturity (T, in years):", value=1.0, step=0.1, min_value=0.01)
    r = st.sidebar.number_input("Risk-Free Rate (r, as decimal):", value=0.05, step=0.01)
    option_type = st.sidebar.selectbox("Option Type:", options=["call", "put"])

    spot_price_min = st.sidebar.number_input("Minimum Spot Price (S):", value=50.0, step=1.0)
    spot_price_max = st.sidebar.number_input("Maximum Spot Price (S):", value=150.0, step=1.0)
    volatility_min = st.sidebar.number_input("Minimum Volatility (σ):", value=0.1, step=0.01, min_value=0.01)
    volatility_max = st.sidebar.number_input("Maximum Volatility (σ):", value=0.5, step=0.01)

    spot_price_input = st.sidebar.number_input("Spot Price for Individual Calculation:", value=100.0, step=1.0)
    volatility_input = st.sidebar.number_input("Volatility for Individual Calculation (σ):", value=0.2, step=0.01, min_value=0.01)

    individual_price = black_scholes_merton(spot_price_input, K, T, r, volatility_input, option_type)

    st.markdown(
        f"""
        <div style="
            border: 2px solid #4CAF50; 
            border-radius: 10px; 
            padding: 20px; 
            background-color: #f9f9f9; 
            text-align: center; 
            width: 80%;
            margin: auto; 
            margin-bottom: 40px;">
            <h3 style="color: #4CAF50; margin-bottom: 10px;">Calculated {option_type.capitalize()} Option Price</h3>
            <p style="font-size: 24px; font-weight: bold; color: #333;">${individual_price:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("Generate Heatmap"):
        spot_prices = np.linspace(spot_price_min, spot_price_max, 11)
        volatilities = np.linspace(volatility_min, volatility_max, 11)

        option_prices = np.zeros((len(volatilities) - 1, len(spot_prices) - 1))
        for i in range(len(volatilities) - 1):
            for j in range(len(spot_prices) - 1):
                sigma = (volatilities[i] + volatilities[i + 1]) / 2
                S = (spot_prices[j] + spot_prices[j + 1]) / 2
                option_prices[i, j] = black_scholes_merton(S, K, T, r, sigma, option_type)

        fig, ax = plt.subplots(figsize=(8, 6))
        c = ax.pcolormesh(
            spot_prices,
            volatilities,
            option_prices,
            cmap="viridis",
            shading="flat",
        )

        fig.colorbar(c, ax=ax, label="Option Price")
        ax.set_title(f"{option_type.capitalize()} Option Price Heatmap (Discrete)")
        ax.set_xlabel("Spot Price (S)")
        ax.set_ylabel("Volatility (σ)")

        for i in range(option_prices.shape[0]):
            for j in range(option_prices.shape[1]):
                x_center = (spot_prices[j] + spot_prices[j + 1]) / 2
                y_center = (volatilities[i] + volatilities[i + 1]) / 2
                ax.text(
                    x_center,
                    y_center,
                    f"{option_prices[i, j]:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="black" if option_prices[i, j] > np.mean(option_prices) else "white",
                )

        st.pyplot(fig)


if __name__ == "__main__":
    main()