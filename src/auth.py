import os
import hmac
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def require_access():
    expected = os.getenv("APP_PASSWORD", "")
    if not expected:
        st.error("Set APP_PASSWORD in your local .env file before running the app.")
        st.stop()
    if st.session_state.get("authenticated"):
        return
    st.subheader("Demo access")
    supplied = st.text_input("Demo application password", type="password")
    if st.button("Sign in"):
        if hmac.compare_digest(supplied, expected):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()
