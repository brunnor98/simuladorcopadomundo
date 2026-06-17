import streamlit as st

st.set_page_config(
    page_title="Bolão da Copa 2026",
    page_icon="⚽",
    layout="centered",
)

st.markdown(
    """
    <style>
    * { font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji",
        "Twemoji Mozilla", sans-serif !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("pagina", "cadastro")
st.session_state.setdefault("participante", {})

_p = st.session_state.pagina
if _p == "palpites":
    import app_pages.palpites as _mod
elif _p == "chaveamento":
    import app_pages.chaveamento as _mod
else:
    import app_pages.cadastro as _mod

_mod.render()
