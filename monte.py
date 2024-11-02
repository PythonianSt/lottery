import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lottery Prediction App", layout="wide")

# Load the historical lottery data from CSV
@st.cache_data
def load_data():
    data = pd.read_csv('Lottery.csv')
    return data

# Function to calculate frequencies of digits
def calculate_frequencies(data):
    frequencies = {i: 0 for i in range(10)}
    for index, row in data.iterrows():
        for i in range(1, 7):  # From FirstD to SixthD
            frequencies[row[i]] += 1
    return frequencies

# Monte Carlo simulation
def monte_carlo_simulation(frequencies, simulations=10000):
    total_counts = {i: 0 for i in range(10)}
    total_weight = sum(frequencies.values())
    
    for _ in range(simulations):
        weighted_numbers = np.random.choice(
            list(frequencies.keys()),
            size=6,
            p=[frequencies[i] / total_weight for i in range(10)]
        )
        for number in weighted_numbers:
            total_counts[number] += 1
            
    return total_counts

# Main Streamlit app
def main():
    st.title("DHV AI Lottery Number Prediction via Monte Carlo Simulation")

    # Display the lottery image
    st.image("lottery.jpg", caption="Lottery Prediction", use_column_width=True)

    data = load_data()
    st.write("Historical Lottery Data:")
    st.dataframe(data)

    # Calculate frequencies of digits 0-9
    frequencies = calculate_frequencies(data)
    st.write("Digit Frequencies:")
    st.bar_chart(frequencies)

    # User input for number of simulations
    simulations = st.number_input("Number of Simulations", min_value=1000, max_value=100000, value=10000, step=1000)

    # User input for a 6-digit number
    user_input = st.text_input("Enter a 6-digit number (e.g., 123456):", max_chars=6)

    if st.button("Predict Numbers"):
        results = monte_carlo_simulation(frequencies, simulations)
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        
        # Extract the top predicted numbers without displaying them
        top_predicted_numbers = {number for number, count in sorted_results[:6]}
        
        # Check how many digits match
        if user_input.isdigit() and len(user_input) == 6:
            user_digits = set(int(digit) for digit in user_input)
            matches = len(user_digits.intersection(top_predicted_numbers))
            #st.write(f"You have {matches} matching digits with the top predicted numbers!")
            st.markdown(f"<h2 style='color:red;'><strong>You have {matches} matching digits with the top predicted numbers!</strong></h2>", unsafe_allow_html=True)
        else:
            st.write("Please enter a valid 6-digit number.")

if __name__ == "__main__":
    main()