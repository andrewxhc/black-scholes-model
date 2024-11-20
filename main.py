from black_scholes import black_scholes_merton

def main():
    print("Black-Scholes-Merton Option Pricing Model")
    print("==========================================")
    
    # User input
    S = float(input("Enter current stock price (S): "))
    K = float(input("Enter strike price (K): "))
    T = float(input("Enter time to maturity in years (T): "))
    r = float(input("Enter risk-free interest rate (r) in decimal (e.g., 0.05 for 5%): "))
    sigma = float(input("Enter volatility (sigma) in decimal (e.g., 0.2 for 20%): "))
    option_type = input("Enter option type ('call' or 'put'): ").lower()
    
    try:
        # Calculate option price
        price = black_scholes_merton(S, K, T, r, sigma, option_type)
        print(f"\nThe {option_type} option price is: ${price:.2f}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
