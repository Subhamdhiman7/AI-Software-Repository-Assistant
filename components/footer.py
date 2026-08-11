import streamlit as st


def show_footer():

    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center;color:#6B7280;">

        <b>RepoMind AI</b><br>

        Built using

        ❤️ Gemini · LangChain · ChromaDB · Streamlit

        </div>
        """,
        unsafe_allow_html=True
    )