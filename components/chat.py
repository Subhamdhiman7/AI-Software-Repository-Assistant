import streamlit as st


def render_chat(messages):
    """
    Beautiful chat interface for RepoMind.
    """

    if not messages:
        st.info("👋 Ask anything about the loaded repository.")
        return

    for message in messages:

        role = message.get("role", "assistant")
        content = message.get("content", "")

        if role == "user":

            st.markdown(
                f"""
                <div class="user-msg">
                    <b>👤 You</b><br><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="ai-msg">
                    <b>🤖 RepoMind</b><br><br>
                    {content}
                </div>
                """,
                unsafe_allow_html=True
            )

            sources = message.get("sources", [])

            if sources:

                st.markdown("##### 📄 Sources")

                cols = st.columns(min(3, len(sources)))

                for i, src in enumerate(sources):
                    cols[i % len(cols)].success(src)