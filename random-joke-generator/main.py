import streamlit as st 
import requests

def get_random_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            return joke
        else:
            st.error("Failed to fetch a joke. Please try again later.")

    except:
        st.error("An error occurred while fetching the joke.")

        
st.title("Random Joke Generator")
st.write("Get a random joke from the JokeAPI!")
st.info("Click the button below to fetch a random joke.")

if st.button("Get a Joke"):
    visible_joke = get_random_joke()
    st.success(f"{visible_joke['setup']} \n \n {visible_joke['punchline']}")
