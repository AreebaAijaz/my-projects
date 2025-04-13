import streamlit as st
import random
import time
import requests

st.title("Money Making Machine")
st.write("Welcome to the Money Making Machine! This app simulates a simple money-making game.")

def generate_money():
    return random.randint(1, 1000)

st.subheader("Instant cash generator")
if st.button("Generate Money!"):
    with st.spinner("Counting your money..."):
        time.sleep(2)  # Simulate a delay
        amount = generate_money()
        st.success(f"You generated ${amount}!")

def generate_side_hustle():
    try:
        response = requests.get("https://fast-api-xi-swart.vercel.app/side_hustles")
        if response.status_code == 200:
            side_hustle = response.json().get("side_hustle", "No side hustle available.")
            return side_hustle
        else:
            return "No side hustle available at the moment."
    except:
        return "Error fetching side hustle. Please try again later."

st.subheader("Side Hustle Generator")
if st.button("Get a Side Hustle"):
    side_hustle = generate_side_hustle()
    st.write(side_hustle)


def generate_money_quote():
    try:
        response = requests.get("https://fast-api-xi-swart.vercel.app/money_quotes")
        if response.status_code == 200:
            quote = response.json().get("money_quote", "No quote available.")
            return quote
        else:
            return "No quote available at the moment."
    except:
        return "Error fetching quote. Please try again later."

st.subheader("Money Quote Generator")
if st.button("Get a Money Quote"):
    quote = generate_money_quote()
    st.write(quote)






















