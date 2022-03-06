import streamlit as st
from datetime import datetime
from pages import home_page, rec_page, pred_page, analytics_page


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():

    st.set_page_config(
        page_title="Savergy",
        page_icon="⚡",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    local_css("style.css")

    pages = {
        "Home": home_page,
        "Preds": pred_page,
        "Analytics": analytics_page,
        "Recs": rec_page,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
            }
        )

    with st.sidebar:
        st.caption("""Navigate the app 👇""")

        if st.button("🏠 Home "):
            st.session_state.page = "Home"
        if st.button("🔮 Predictions"):
            st.session_state.page = "Preds"
        if st.button("ℹ️ Resources"):
            st.session_state.page = "Recs"

    pages[st.session_state.page]()


if __name__ == "__main__":
    main()
