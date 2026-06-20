import streamlit as st
from data.times import CODIGOS, country_emoji
from data.bracket import R32, R16_PAIRS, QF_PAIRS, SF_PAIRS, pos_label
from services.supabase_client import salvar_participante, salvar_palpites, salvar_chaveamento


def _fmt(time: str | None) -> str:
    if not time:
        return "A definir"
    return f"{country_emoji(time)} {time}"


def _resolve_r32_teams() -> dict:
    selecoes = st.session_state.get("_selecoes") or {}
    avancam = st.session_state.get("_avancam") or []

    pos = {}
    team_to_group = {}
    for letra, s in selecoes.items():
        if s.get("primeiro"):
            pos[f"1{letra}"] = s["primeiro"]
        if s.get("segundo"):
            pos[f"2{letra}"] = s["segundo"]
        if s.get("terceiro"):
            team_to_group[s["terceiro"]] = letra

    thirds = sorted(avancam, key=lambda t: team_to_group.get(t, "Z"))
    third_iter = iter(thirds)

    teams = {}
    for m in R32:
        t1 = pos.get(m["t1"]) if m["t1"] != "3" else next(third_iter, None)
        t2 = pos.get(m["t2"]) if m["t2"] != "3" else next(third_iter, None)
        teams[m["id"]] = (t1, t2)
    return teams


def _next_round(prev_prefix: str, pairs: list) -> dict:
    teams = {}
    for num, (a, b) in enumerate(pairs, start=1):
        winner_a = st.session_state.get(f"bk_{prev_prefix}_{a}")
        winner_b = st.session_state.get(f"bk_{prev_prefix}_{b}")
        teams[num] = (winner_a, winner_b)
    return teams


def _match_card(key: str, t1, t2, titulo: str):
    with st.container(border=True):
        st.caption(titulo)
        if t1 and t2:
            current = st.session_state.get(key)
            if current is not None and current not in (t1, t2):
                del st.session_state[key]
                current = None
            col1, col2 = st.columns(2)
            for idx, (team, col) in enumerate([(t1, col1), (t2, col2)]):
                code = CODIGOS.get(team, "un")
                is_sel = current == team
                with col:
                    st.markdown(
                        f'<div style="text-align:center;padding:2px 0 4px">'
                        f'<img src="https://flagcdn.com/w40/{code}.png" '
                        f'style="height:28px;border-radius:2px"></div>',
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        ("✅ " if is_sel else "") + team,
                        key=f"{key}__t{idx}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state[key] = team
                        st.rerun()
        else:
            if key in st.session_state:
                del st.session_state[key]
            tbd1 = _fmt(t1) if t1 else "❓ A definir"
            tbd2 = _fmt(t2) if t2 else "❓ A definir"
            st.markdown(f"{tbd1} **vs** {tbd2}")
            st.caption("⏳ Preencha a fase anterior")


def _render_round(teams: dict, prefix: str, titles: dict):
    ids = sorted(teams.keys())
    for i in range(0, len(ids), 2):
        pair = ids[i : i + 2]
        cols = st.columns(len(pair))
        for j, mid in enumerate(pair):
            t1, t2 = teams[mid]
            with cols[j]:
                _match_card(f"bk_{prefix}_{mid}", t1, t2, titles.get(mid, f"Jogo {mid}"))


def render():
    participante = st.session_state.participante

    st.markdown(
        f"""
        <div class="bolao-hero">
            <div class="emoji">🏆</div>
            <h1>Chaveamento — Copa 2026</h1>
            <p>Olá, <strong>{participante['nome']}</strong>! Preencha o mata-mata completo até o campeão.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "As equipes são preenchidas automaticamente com base nos seus palpites da fase de grupos. "
        "Selecione o vencedor de cada confronto — as próximas fases se preenchem sozinhas.",
        icon="ℹ️",
    )

    # ── 16 Avos ──────────────────────────────────────────────────────────────
    r32_teams = _resolve_r32_teams()

    st.subheader("⚔️ 16 Avos de Final")
    r32_titles = {
        m["id"]: f"J{m['id']} · {pos_label(m['t1'])} × {pos_label(m['t2'])}"
        for m in R32
    }
    _render_round(r32_teams, "r32", r32_titles)

    # ── Oitavas ───────────────────────────────────────────────────────────────
    r16_teams = _next_round("r32", R16_PAIRS)

    st.divider()
    st.subheader("⚔️ Oitavas de Final")
    r16_titles = {i: f"Oitavas J{i}" for i in range(1, 9)}
    _render_round(r16_teams, "r16", r16_titles)

    # ── Quartas ───────────────────────────────────────────────────────────────
    qf_teams = _next_round("r16", QF_PAIRS)

    st.divider()
    st.subheader("⚔️ Quartas de Final")
    qf_titles = {i: f"Quartas J{i}" for i in range(1, 5)}
    _render_round(qf_teams, "qf", qf_titles)

    # ── Semifinais ────────────────────────────────────────────────────────────
    sf_teams = _next_round("qf", SF_PAIRS)

    st.divider()
    st.subheader("⚔️ Semifinais")
    sf_titles = {1: "Semifinal 1", 2: "Semifinal 2"}
    _render_round(sf_teams, "sf", sf_titles)

    # ── Final & 3º lugar ──────────────────────────────────────────────────────
    sf1_t1, sf1_t2 = sf_teams.get(1, (None, None))
    sf2_t1, sf2_t2 = sf_teams.get(2, (None, None))
    sf1_winner = st.session_state.get("bk_sf_1")
    sf2_winner = st.session_state.get("bk_sf_2")
    sf1_loser = (sf1_t2 if sf1_winner == sf1_t1 else sf1_t1) if sf1_winner else None
    sf2_loser = (sf2_t2 if sf2_winner == sf2_t1 else sf2_t1) if sf2_winner else None

    st.divider()
    st.subheader("🏆 Final & 3º Lugar")
    col_3p, col_f = st.columns(2)
    with col_3p:
        _match_card("bk_3p", sf1_loser, sf2_loser, "🥉 Disputa 3º Lugar")
    with col_f:
        _match_card("bk_final", sf1_winner, sf2_winner, "🏆 Grande Final")

    campeao = st.session_state.get("bk_final")
    if campeao:
        code = CODIGOS.get(campeao, "un")
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#F2B705 0%,#E08C00 100%);'
            f'border-radius:16px;padding:1.1rem 1rem;text-align:center;color:#fff;'
            f'box-shadow:0 8px 22px rgba(224,140,0,.32);margin:0.5rem 0">'
            f'<div style="font-size:0.78rem;letter-spacing:.08em;text-transform:uppercase;'
            f'opacity:.92;font-weight:700">🏆 Seu campeão</div>'
            f'<img src="https://flagcdn.com/w80/{code}.png" '
            f'style="height:40px;border-radius:4px;margin:0.5rem 0 0.25rem;'
            f'box-shadow:0 2px 6px rgba(0,0,0,.25)"><br>'
            f'<span style="font-size:1.4rem;font-weight:800;'
            f'text-shadow:0 1px 3px rgba(0,0,0,.2)">{campeao}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Botões ────────────────────────────────────────────────────────────────
    st.divider()
    col_v, col_s = st.columns([1, 3])
    with col_v:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.pagina = "palpites"
            st.rerun()
    with col_s:
        if st.button("✅ Confirmar tudo e salvar!", type="primary", use_container_width=True):
            _salvar_tudo(participante)


def _salvar_tudo(participante: dict):
    selecoes = st.session_state.get("_selecoes") or {}
    avancam = st.session_state.get("_avancam") or []

    incompletos = [g for g, s in selecoes.items() if not all(s.values())]
    if incompletos:
        st.error(f"Grupos com palpites incompletos: **{', '.join(incompletos)}**. Volte e complete.")
        return

    if len(avancam) != 8:
        st.error("Volte e selecione exatamente **8 terceiros colocados** que avançam.")
        return

    campeao = st.session_state.get("bk_final")
    if not campeao:
        st.error("Selecione o **campeão** na seção 🏆 Final & 3º antes de salvar.")
        return

    grupos_3_avancam = {
        letra for letra, s in selecoes.items()
        if s.get("terceiro") in avancam
    }

    picks = {}
    for i in range(1, 17):
        v = st.session_state.get(f"bk_r32_{i}")
        if v:
            picks[("r32", i)] = v
    for i in range(1, 9):
        v = st.session_state.get(f"bk_r16_{i}")
        if v:
            picks[("r16", i)] = v
    for i in range(1, 5):
        v = st.session_state.get(f"bk_qf_{i}")
        if v:
            picks[("qf", i)] = v
    for i in range(1, 3):
        v = st.session_state.get(f"bk_sf_{i}")
        if v:
            picks[("sf", i)] = v
    v3p = st.session_state.get("bk_3p")
    if v3p:
        picks[("3p", 1)] = v3p
    picks[("final", 1)] = campeao

    with st.spinner("Salvando seus palpites..."):
        try:
            pid = salvar_participante(
                participante["nome"],
                participante["telefone"],
                participante["email"],
            )
            salvar_palpites(pid, selecoes, grupos_3_avancam)
            salvar_chaveamento(pid, picks)

            st.success(f"🏆 Palpites salvos! Seu campeão: **{_fmt(campeao)}** — Boa sorte!")
            st.balloons()

            for k in [k for k in list(st.session_state.keys())
                      if k.startswith("bk_") or k in ("_selecoes", "_avancam", "terceiros_avancam")
                      or (k.startswith("g") and len(k) == 4 and k[1].isupper())]:
                del st.session_state[k]
            st.session_state.pagina = "cadastro"
            st.session_state.participante = {}

        except Exception as e:
            st.error(f"Erro ao salvar. Tente novamente. Detalhe: {e}")
