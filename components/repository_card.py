import streamlit as st


def show_repository_card(repo_name, files, chunks):

    st.markdown(
        f"""
        <div class="card">

        <h3>📦 Connected Repository</h3>

        <hr>

        <h2 style="margin-bottom:5px;">
            {repo_name}
        </h2>

        <p style="color:#10B981;font-weight:600;">
            🟢 Repository Indexed Successfully
        </p>

        <br>

        <div style="display:flex;justify-content:space-between;">

            <div>
                <b>📂 Files</b><br>
                {files}
            </div>

            <div>
                <b>🧩 Chunks</b><br>
                {chunks}
            </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )