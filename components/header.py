import streamlit as st


def show_header():
    st.markdown(
        "<div style='text-align:center; padding:20px 0 10px;'>"
        "<h1 style='color:#1F2937; margin-bottom:5px;'>🧠 RepoMind AI</h1>"
        "<p style='color:#6B7280; font-size:18px; margin:0;'>"
        "AI Software Repository Assistant"
        "</p>"
        "<p style='color:#6B7280;'>"
        "Understand any GitHub repository using RAG, Gemini and ChromaDB."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )