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

    /* ── Responsividade Mobile ───────────────────────────── */

    /* Tablets */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 0.75rem !important;
            max-width: 100% !important;
        }
    }

    /* Smartphones */
    @media (max-width: 640px) {
        /* Empilha todas as colunas verticalmente */
        div[data-testid="stColumns"] {
            flex-direction: column !important;
            gap: 0.25rem !important;
        }
        div[data-testid="stColumn"] {
            width: 100% !important;
            flex: 0 0 100% !important;
            min-width: 0 !important;
        }

        /* Títulos menores */
        h1 { font-size: 1.4rem !important; line-height: 1.3 !important; }
        h2 { font-size: 1.2rem !important; }
        h3 { font-size: 1rem !important; }

        /* Emoji de cabeçalho */
        span[style*="font-size:3rem"] { font-size: 2rem !important; }

        /* Botões */
        .stButton > button {
            font-size: 0.82rem !important;
            padding: 0.4rem 0.5rem !important;
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.3 !important;
        }

        /* Inputs */
        .stTextInput input { font-size: 0.9rem !important; }
        .stTextInput label,
        .stSelectbox label,
        .stMultiSelect label { font-size: 0.85rem !important; }

        /* Selectbox e multiselect */
        [data-baseweb="select"] * { font-size: 0.85rem !important; }
        [data-baseweb="tag"] span { font-size: 0.75rem !important; }

        /* Caixas de alerta/info */
        [data-testid="stNotification"] p { font-size: 0.85rem !important; }

        /* Caption */
        [data-testid="stCaptionContainer"] { font-size: 0.8rem !important; }

        /* Padding interno dos containers com borda */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0.6rem 0.5rem !important;
        }
    }
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
elif _p == "resultados":
    import app_pages.resultados as _mod
else:
    import app_pages.cadastro as _mod

_mod.render()
