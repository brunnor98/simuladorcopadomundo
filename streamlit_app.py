import streamlit as st

st.set_page_config(
    page_title="Bolão da Copa 2026",
    page_icon="⚽",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* ── Tokens semânticos de design ─────────────────────── */
    :root {
        --brand: #009C3B;
        --brand-strong: #00802F;
        --brand-700: #006D29;
        --brand-light: #E8F5E9;
        --gold: #E6A817;
        --gold-light: #FBF1D8;
        --ink: #14241A;
        --muted: #5C6B60;
        --surface: #FFFFFF;
        --bg: #F3F8F4;
        --border: #E3EDE5;
        --radius: 14px;
        --shadow-sm: 0 1px 2px rgba(16,40,24,.06);
        --shadow-md: 0 6px 20px rgba(16,40,24,.09);
    }

    /* ── Webfont de bandeiras ────────────────────────────────
       Renderiza emojis de bandeira (regional indicators + flags
       de subdivisão como Escócia/Inglaterra) em TODOS os navegadores,
       inclusive Windows desktop, que não possui esses glifos.
       O unicode-range restringe a fonte aos codepoints de bandeira,
       então NÃO interfere nos ícones (Material Symbols) do Streamlit. */
    @font-face {
        font-family: "Twemoji Country Flags";
        unicode-range: U+1F1E6-1F1FF, U+1F3F4, U+E0062-E0063, U+E0065,
            U+E0067, U+E006C, U+E006E, U+E0073-E0074, U+E0077, U+E007F;
        /* Primário: arquivo hospedado no próprio repo (sem dependência de rede externa).
           Fallback: CDN, usado apenas se o arquivo local não for encontrado. */
        src: url('app/static/fonts/TwemojiCountryFlags.woff2') format('woff2'),
             url('https://cdn.jsdelivr.net/npm/country-flag-emoji-polyfill@0.1/dist/TwemojiCountryFlags.woff2') format('woff2');
        font-display: swap;
    }

    html, body, p, h1, h2, h3, h4, h5, h6, li, td, th, label,
    input, textarea, button, .stMarkdown,
    [data-baseweb="select"] *, [data-baseweb="popover"] *,
    [role="option"], [data-baseweb="tag"] * {
        font-family: "Twemoji Country Flags", "Source Sans Pro", "Segoe UI",
            "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
    }

    /* ── Base ────────────────────────────────────────────── */
    .stApp { background: var(--bg); }
    .block-container { max-width: 780px; padding-top: 1.25rem; }
    h1, h2, h3 { color: var(--ink); letter-spacing: -0.01em; }
    hr { margin: 1.1rem 0 !important; border-color: var(--border) !important; }

    /* ── Hero ────────────────────────────────────────────── */
    .bolao-hero {
        background: linear-gradient(135deg, #00B544 0%, #007A2E 100%);
        border-radius: 20px;
        padding: 1.6rem 1.25rem;
        text-align: center;
        color: #fff;
        box-shadow: 0 10px 28px rgba(0,122,46,.28);
        margin-bottom: 1.1rem;
        position: relative;
        overflow: hidden;
    }
    .bolao-hero::after {
        content: "";
        position: absolute; inset: 0;
        background:
            radial-gradient(circle at 88% 14%, rgba(255,255,255,.16) 0, transparent 38%),
            radial-gradient(circle at 8% 92%, rgba(255,255,255,.10) 0, transparent 42%);
        pointer-events: none;
    }
    .bolao-hero .emoji {
        font-size: 2.6rem; line-height: 1;
        display: inline-block;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,.18));
    }
    .bolao-hero h1 {
        color: #fff !important; margin: .35rem 0 0;
        font-size: 1.65rem; font-weight: 800; line-height: 1.2;
        position: relative;
    }
    .bolao-hero p {
        color: rgba(255,255,255,.92) !important;
        margin: .45rem 0 0; font-size: .96rem; line-height: 1.4;
        position: relative;
    }
    .bolao-hero strong { color: var(--gold-light); font-weight: 700; }

    /* ── Cards / containers com borda ────────────────────── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        background: var(--surface) !important;
        box-shadow: var(--shadow-sm);
    }

    /* ── Botões ──────────────────────────────────────────── */
    .stButton > button {
        border-radius: 11px !important;
        font-weight: 600 !important;
        border: 1px solid var(--border) !important;
        transition: transform .12s ease, box-shadow .15s ease,
            background .15s ease, border-color .15s ease !important;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: var(--shadow-md); }
    .stButton > button:active { transform: translateY(0) scale(.99); }
    .stButton > button:focus-visible {
        outline: 3px solid rgba(0,156,59,.35) !important; outline-offset: 2px !important;
    }

    /* Primário — gradiente da marca */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #00B544 0%, #008834 100%) !important;
        border: none !important;
        color: #fff !important;
        box-shadow: 0 4px 14px rgba(0,136,52,.30) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        box-shadow: 0 7px 22px rgba(0,136,52,.42) !important;
    }

    /* Secundário — contorno suave da marca */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: #fff !important;
        color: var(--brand-700) !important;
        border: 1px solid var(--border) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background: var(--brand-light) !important;
        border-color: var(--brand) !important;
    }

    /* ── Inputs / selects ────────────────────────────────── */
    .stTextInput input, [data-baseweb="select"] > div {
        border-radius: 11px !important;
    }
    .stTextInput input:focus, [data-baseweb="select"] > div:focus-within {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 3px rgba(0,156,59,.15) !important;
    }

    /* ── Métrica ─────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid var(--border);
        border-radius: var(--radius); padding: .75rem 1rem;
        box-shadow: var(--shadow-sm);
    }

    /* ── Expanders ───────────────────────────────────────── */
    [data-testid="stExpander"] {
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        overflow: hidden;
    }

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
            gap: 0.5rem !important;
        }
        div[data-testid="stColumn"] {
            width: 100% !important;
            flex: 0 0 100% !important;
            min-width: 0 !important;
        }

        /* Hero compacto */
        .bolao-hero { padding: 1.25rem 1rem; border-radius: 16px; }
        .bolao-hero .emoji { font-size: 2.1rem; }
        .bolao-hero h1 { font-size: 1.3rem !important; }
        .bolao-hero p { font-size: 0.9rem; }

        /* Títulos menores */
        h1 { font-size: 1.35rem !important; line-height: 1.3 !important; }
        h2 { font-size: 1.15rem !important; }
        h3 { font-size: 1rem !important; }

        /* Botões — alvo mínimo de toque 44 px (Apple HIG / Material) */
        .stButton > button {
            min-height: 44px !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 0.75rem !important;
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.3 !important;
            touch-action: manipulation !important;
        }

        /* Inputs — 16 px (1 rem) previne zoom automático no iOS */
        .stTextInput input {
            font-size: 1rem !important;
            min-height: 44px !important;
        }
        .stTextInput label,
        .stSelectbox label,
        .stMultiSelect label { font-size: 0.9rem !important; }

        /* Selectbox e multiselect — 16 px previne zoom iOS */
        [data-baseweb="select"] * { font-size: 1rem !important; }
        [data-baseweb="tag"] span { font-size: 0.8rem !important; }

        /* Caixas de alerta/info */
        [data-testid="stNotification"] p { font-size: 0.875rem !important; }

        /* Caption */
        [data-testid="stCaptionContainer"] { font-size: 0.8rem !important; }

        /* Padding interno dos containers com borda */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 0.75rem 0.625rem !important;
        }

        /* Safe area inferior — iOS Home Indicator / gestos de sistema */
        .block-container {
            padding-bottom: max(1.5rem, env(safe-area-inset-bottom)) !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _step_indicator(step: int) -> None:
    """Indicador de progresso de 3 passos do fluxo de palpites."""
    labels = ["Dados", "Grupos", "Chaveamento"]
    dots = ""
    for i, label in enumerate(labels, start=1):
        done = i < step
        active = i == step
        if active:
            bg, fg = "#009C3B", "#fff"
        elif done:
            bg, fg = "#4CAF50", "#fff"
        else:
            bg, fg = "#E8F5E9", "#9E9E9E"
        text_color = "#00802F" if (active or done) else "#A8B5AC"
        weight = "700" if active else "600" if done else "500"
        mark = "✓" if done else str(i)
        ring = "box-shadow:0 0 0 4px rgba(0,156,59,.15);" if active else ""
        dots += (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">'
            f'<div style="width:30px;height:30px;border-radius:50%;background:{bg};'
            f'color:{fg};display:flex;align-items:center;justify-content:center;'
            f'font-size:0.82rem;font-weight:{weight};{ring}">{mark}</div>'
            f'<span style="font-size:0.64rem;color:{text_color};font-weight:{weight};'
            f'text-align:center;white-space:nowrap">{label}</span>'
            f'</div>'
        )
        if i < len(labels):
            line_color = "#4CAF50" if done else "#DCEBDE"
            dots += (
                f'<div style="flex:1;max-width:56px;min-width:18px;height:3px;'
                f'background:{line_color};margin-top:14px;border-radius:2px"></div>'
            )
    st.markdown(
        f'<div style="display:flex;justify-content:center;align-items:flex-start;'
        f'gap:6px;margin:0.25rem auto 0.9rem;max-width:280px">{dots}</div>',
        unsafe_allow_html=True,
    )


st.session_state.setdefault("pagina", "cadastro")
st.session_state.setdefault("participante", {})

_p = st.session_state.pagina
if _p == "palpites":
    import app_pages.palpites as _mod
    _step_indicator(2)
elif _p == "chaveamento":
    import app_pages.chaveamento as _mod
    _step_indicator(3)
elif _p == "resultados":
    import app_pages.resultados as _mod
else:
    import app_pages.cadastro as _mod
    _step_indicator(1)

_mod.render()
