import streamlit as st

import random
import string

def password_generator(length, use_digits, use_special):
    """Generate a random password based on the specified criteria."""
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    return ''.join(random.choice(characters) for i in range(length))

st.title("Password Generator")
st.write("Generate a secure password based on your criteria.")

length = st.slider("Select Password length" , min_value=6, max_value=32, value=12)
use_digits = st.checkbox("Include digits (0-9)", value=False)
use_special = st.checkbox("Include special characters (!@#$%^&*)", value=False)

if st.button("Generate Password"):
    password = password_generator(length, use_digits, use_special)
    st.write(f"Generated Password: {password} <h4 style='cursor: pointer;'>{password}</h4>", unsafe_allow_html=True)

st.write("Built with ❤️ by Areeba Aijaz")

