import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy_financial as npf

st.title("Mortgage Repayment Calculator")

# Create 2 columns so that user input will be shown in 2 columns
st.write("### Input Data")
col1, col2 = st.columns(2)

# Create the input columns and set minimum & default values
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest rate (in %)", min_value=0.0, value=6.5)
loan_term = col2.number_input("Loan Term", min_value=1, value=30)

# Calculate repayments
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    npf.pmt(monthly_interest_rate, number_of_payments, -loan_amount, 0)
)

# Display the repayments
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a dataframe with the payment schedule
## Step 1: Initialize an empty schedule and starting balance
schedule = []
remaining_balance = loan_amount

## Step 2: Loop over all months in the loan
for i in range(1, number_of_payments + 1): # range starts counting from 1 and end before number_of_payments + 1; for i in is a for loop (think of it as everytime it hits a number within the range, it will run once)
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment # This is the same as writing remaining_balance = remaining_balance - principal_payment
    year = math.ceil(i / 12) # Calculate the year into the loan; ceil function rounds up to the next nearest whole number
    schedule.append( # Save this month's info into the table
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

## Step 3: Turn the schedule into a DataFrame
df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

## Step 4: Format the numbers to insert comma separators
# Format numeric columns for readability
formatted_df = df.copy()

formatted_df["Payment"] = formatted_df["Payment"].map("${:,.2f}".format)
formatted_df["Principal"] = formatted_df["Principal"].map("${:,.2f}".format)
formatted_df["Interest"] = formatted_df["Interest"].map("${:,.2f}".format)
formatted_df["Remaining Balance"] = formatted_df["Remaining Balance"].map("${:,.2f}".format)

formatted_df["Month"] = formatted_df["Month"].astype(int)
formatted_df["Year"] = formatted_df["Year"].astype(int)

## Step 5: Drop DataFrame index and display amort table
formatted_df = formatted_df.reset_index(drop=True)

st.write("### Amortization Schedule")
st.dataframe(formatted_df)

## Step 6: Display the dataframe as a chart
st.write("### Principal Repaid Over Time")
payments_df = df[["Year", "Principal"]].groupby("Year").sum()
st.line_chart(payments_df)