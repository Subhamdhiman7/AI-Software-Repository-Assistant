import streamlit as st


def show_dashboard(repo_info):

    if not repo_info:
        return

    st.markdown("## 📊 Repository Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📂 Files</h4>
            <h2>{}</h2>
        </div>
        """.format(repo_info.get("files", 0)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🧩 Chunks</h4>
            <h2>{}</h2>
        </div>
        """.format(repo_info.get("chunks", 0)), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>💻 Language</h4>
            <h3>{}</h3>
        </div>
        """.format(
            ", ".join(repo_info.get("languages", [])) or "Unknown"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>⚙ Framework</h4>
            <h3>{}</h3>
        </div>
        """.format(
            ", ".join(repo_info.get("frameworks", [])) or "None"
        ), unsafe_allow_html=True)

    st.markdown("")

    left, right = st.columns(2)

    with left:

        st.markdown("""
        <div class="card">
            <h4>📦 Project Information</h4>
        """, unsafe_allow_html=True)

        st.write("**Project Type:**", repo_info.get("project_type", "Unknown"))
        st.write("**Database:**", repo_info.get("database", "Not Detected"))
        st.write("**AI Model:**", repo_info.get("ai", "Not Detected"))

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown("""
        <div class="card">
            <h4>🚀 Entry Points</h4>
        """, unsafe_allow_html=True)

        entries = repo_info.get("entry_points", [])

        if entries:
            for item in entries:
                st.code(item)
        else:
            st.info("No entry points detected.")

        st.markdown("</div>", unsafe_allow_html=True)

    important = repo_info.get("important_files", [])

    if important:

        st.markdown("### 📁 Important Files")

        cols = st.columns(3)

        for i, file in enumerate(important):
            cols[i % 3].success(file)