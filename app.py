import streamlit as st
import requests

# URL of your backend pod (we'll replace this later with your real IP)
BACKEND_URL = "http://your-pod-ip:5000/generate"

st.set_page_config(page_title="VIRAM", layout="centered")
st.title("VIRAM")

# Input box
user_input = st.text_area("Ask your question below:")

# Store original question + response
if "original_prompt" not in st.session_state:
    st.session_state.original_prompt = ""
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "depth" not in st.session_state:
    st.session_state.depth = 1
if "show_roles" not in st.session_state:
    st.session_state.show_roles = False

# Get Answer button
if st.button("Get Answer"):
    st.session_state.original_prompt = user_input
    st.session_state.depth = 1
    try:
        response = requests.post(BACKEND_URL, json={"prompt": user_input})
        result = response.json()
        st.session_state.last_response = result.get("answer", "Error: No response.")
    except:
        st.session_state.last_response = "Error: Could not connect to backend."

# Display Answer
if st.session_state.last_response:
    st.subheader("Answer")
    st.write(st.session_state.last_response)

    # Want more depth
    if st.button("🔍 Want more depth?"):
        st.session_state.depth += 1
        try:
            response = requests.post(BACKEND_URL, json={
                "prompt": st.session_state.original_prompt,
                "depth": st.session_state.depth
            })
            result = response.json()
            st.session_state.last_response = result.get("answer", "Error: No deeper response.")
        except:
            st.session_state.last_response = "Error: Could not reach backend for deeper answer."

    # Show Perspectives toggle
    if st.button("🧠 Show Perspectives" if not st.session_state.show_roles else "🧠 Hide Perspectives"):
        st.session_state.show_roles = not st.session_state.show_roles

    if st.session_state.show_roles:
        st.markdown("**Want a different perspective? Click one:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Mentor"):
                st.session_state.last_response = f"[Mentor tone] {st.session_state.original_prompt}"
        with col2:
            if st.button("Evaluator"):
                st.session_state.last_response = f"[Evaluator tone] {st.session_state.original_prompt}"
        with col3:
            if st.button("Peer"):
                st.session_state.last_response = f"[Peer tone] {st.session_state.original_prompt}"
        with col4:
            if st.button("Advisor"):
                st.session_state.last_response = f"[Advisor tone] {st.session_state.original_prompt}"
