import streamlit as st
import app1, app2

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Community Detection", "Social Network Analysis"])

if selection == "Community Detection":
    app1.app()
elif selection == "Social Network Analysis":
    app2.app()
