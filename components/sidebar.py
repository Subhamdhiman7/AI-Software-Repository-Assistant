import streamlit as st


def show_sidebar():
    with st.sidebar:

        st.markdown("# 🧠 RepoMind")

        st.caption("AI Repository Assistant")

        st.divider()

        st.markdown("### ⚙ Settings")

        st.success("🟢 Gemini 3.6 Flash")

        st.info("🧠 Conversation Memory")

        st.info("📚 Repository Summary")

        st.divider()

        st.markdown("### 📈 Session")

        if "messages" in st.session_state:
            st.metric(
                "Messages",
                len(st.session_state.messages)
            )

        if "repository_summary" in st.session_state:
            st.metric(
                "Repository",
                "Loaded"
            )
        else:
            st.metric(
                "Repository",
                "Not Loaded"
            )

        st.divider()

        if st.button(
            "🗑 Clear Conversation",
            use_container_width=True
        ):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        st.caption("RepoMind AI v1.0")