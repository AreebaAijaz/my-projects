import streamlit as st
import random 
import time

st.title("Quiz Application")

questions = [
    {
        "question": "What is the capital of Pakistan?",
        "options": ["Karachi", "Lahore", "Islamabad", "Peshawar"],
        "answer": "Islamabad"
    },
    {
        "question": "Who is the founder of Pakistan?",
        "options": ["Allama Iqbal", "Quaid-e-Azam", "Liaquat Ali Khan", "Fatima Jinnah"],
        "answer": "Quaid-e-Azam"
    },
    {
        "question": "What is the national language of Pakistan?",
        "options": ["English", "Urdu", "Punjabi", "Sindhi"],
        "answer": "Urdu"
    },
    {
        "question": "When did Pakistan gain independence?",
        "options": ["1945", "1947", "1950", "1952"],
        "answer": "1947"
    },
    {
        "question": "What is the currency of Pakistan?",
        "options": ["Dollar", "Rupee", "Pound", "Yen"],
        "answer": "Rupee"
    },
    {
        "question": "What is the national animal of Pakistan?",
        "options": ["Lion", "Tiger", "Markhor", "Elephant"],
        "answer": "Markhor"
    },
    {
        "question": "What is the national flower of Pakistan?",
        "options": ["Rose", "Jasmine", "Lotus", "Sunflower"],
        "answer": "Jasmine"
    },
    {
        "question": "What is the highest mountain in Pakistan?",
        "options": ["K2", "Nanga Parbat", "Gasherbrum", "Karakoram"],
        "answer": "K2"
    }
]

# Initialize only once
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

# Always show the question and options
question = st.session_state.current_question
st.subheader(question["question"])
selected_option = st.selectbox("Choose an option from:", question["options"])

if st.button("Submit"):
    if selected_option == question["answer"]:
        st.success("✅ Correct answer!")
    else:
         st.error(f"❌ Wrong answer! The correct option is {question['answer']}")

if st.button("Next Question"):
    st.session_state.current_question = random.choice(questions)
    st.rerun()