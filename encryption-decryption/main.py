import streamlit as st
from cryptography.fernet import Fernet
from data_manager import DataManager
import time
import os

# Initialize DataManager
data_manager = DataManager()

# Key file path
KEY_FILE = "encryption_key.key"

# Load or generate encryption key
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as key_file:
        KEY = key_file.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(KEY)

cipher = Fernet(KEY)

# Function to encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text):
    return cipher.decrypt(encrypted_text.encode()).decode()

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Session state for user authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Navigation
menu = ["Home", "Login", "Register", "Store Data", "Retrieve Data"]
if not st.session_state.authenticated:
    choice = st.sidebar.selectbox("Navigation", ["Home", "Login", "Register"])
else:
    choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    if st.session_state.authenticated:
        st.write(f"Logged in as: **{st.session_state.current_user}**")

elif choice == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if data_manager.is_locked_out(username):
            st.error("❌ Account is locked. Please try again after 15 minutes.")
        else:
            if data_manager.authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.current_user = username
                data_manager.reset_failed_attempts(username)
                st.success("✅ Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                data_manager.record_failed_attempt(username)
                st.error("❌ Invalid username or password!")

elif choice == "Register":
    st.subheader("📝 Register New User")
    new_username = st.text_input("Choose Username")
    new_password = st.text_input("Choose Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            if data_manager.register_user(new_username, new_password):
                st.success("✅ Registration successful! Please login.")
            else:
                st.error("❌ Username already exists!")

elif choice == "Store Data":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login to access this feature.")
    else:
        st.subheader("📂 Store Data Securely")
        
        # Show instructions
        with st.expander("ℹ️ How to use this feature"):
            st.write("""
            1. Enter the data you want to encrypt in the text area below
            2. Create a passkey (password) to protect this data
            3. Click 'Encrypt & Save'
            4. **IMPORTANT**: Save the encrypted data shown after encryption
            5. Remember your passkey - you'll need both to retrieve your data
            """)
        
        user_data = st.text_area("Enter Data:")
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Encrypt & Save"):
            if user_data and passkey:
                encrypted_text = encrypt_data(user_data)
                if st.session_state.current_user not in data_manager.stored_data:
                    data_manager.stored_data[st.session_state.current_user] = {}
                
                data_manager.stored_data[st.session_state.current_user][encrypted_text] = {
                    "encrypted_text": encrypted_text,
                    "passkey": passkey
                }
                data_manager.save_data()
                st.success("✅ Data stored securely!")
                
                # # Show encrypted data in a more prominent way
                # st.info("🔐 Your encrypted data is:")
                # st.code(encrypted_text)
                # st.warning("⚠️ Please save this encrypted data. You'll need it to retrieve your data later.")
                
                # # Show a copy button
                # if st.button("Copy Encrypted Data"):
                #     st.code(encrypted_text)
                #     st.success("✅ Copied to clipboard!")
            else:
                st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login to access this feature.")
    else:
        st.subheader("🔍 Retrieve Your Data")
        
        # Show instructions
        with st.expander("ℹ️ How to retrieve your data"):
            st.write("""
            1. Enter the encrypted data you saved earlier
            2. Enter the passkey you used when storing the data
            3. Click 'Decrypt' to view your original data
            """)
        
        # Show stored encrypted data for the current user
        if st.session_state.current_user in data_manager.stored_data:
            st.subheader("📋 Your Stored Encrypted Data")
            user_data = data_manager.stored_data[st.session_state.current_user]
            if user_data:
                for encrypted_text, data in user_data.items():
                    with st.expander(f"🔒 Encrypted Data {list(user_data.keys()).index(encrypted_text) + 1}"):
                        st.code(encrypted_text)
                        st.write("Passkey required to decrypt")
            else:
                st.info("ℹ️ No data stored yet. Use the Store Data feature to save your first encrypted data.")
        
        encrypted_text = st.text_area("Enter Encrypted Data:")
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Decrypt"):
            if encrypted_text and passkey:
                user_data = data_manager.stored_data[st.session_state.current_user]
                if encrypted_text in user_data and user_data[encrypted_text]["passkey"] == passkey:
                    decrypted_text = decrypt_data(encrypted_text)
                    st.success("✅ Decryption successful!")
                    st.info("📝 Your decrypted data:")
                    st.write(decrypted_text)
                else:
                    st.error("❌ Incorrect passkey or encrypted data!")
            else:
                st.error("⚠️ Both fields are required!")