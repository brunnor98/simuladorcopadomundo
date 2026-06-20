import streamlit as st
from collections import Counter

from data.times import GRUPOS, CODIGOS
from services.supabase_client import (
    buscar_total_participantes,
    buscar_palpites_grupos,
    buscar_chaveamento_todos,
)

FLAG_BASE = "https://flagcdn.com/w40"


@st.cache_data(ttl=120)
def _carregar_dados():
    total = buscar_total_participantes()
    palpites = buscar_palpites_grupos()
    chaveamento = buscar_chaveamento_todos()
    return total, palpites, chaveamento


def _pct(n: int, total: int) -> float:
    return round(n / total * 100, 1) if total else 0.0


def _barra(time: str, n: int, total: int, cor: str = "#009C3B") -> str:
    pct = _pct(n, total)
    code = CODIGOS.get(time, "un")
    bar_w = min(pct, 100)
    return (
        f'<div style="display:flex;align-items:center;gap:6px;padding:5px 2px;'
        f'border-bottom:1px solid #f0f4f0">'
        f'<img src="{FLAG_BASE}/{code}.png" alt="" '
        f'style="width:22px;height:15px;object-fit:cover;border-radius:2px;'
        f'flex-shrink:0;box-shadow:0 0 0 1px rgba(0,0,0,.05)">'
        f'<span style="flex:1;font-size:0.85rem;overflow:hidden;'
        f'text-overflow:ellipsis;white-space:nowrap;min-width:0">{time}</span>'
        f'<div style="flex:0 0 80px;background:#e8f5e9;border-radius:4px;height:10px">'
        f'<div style="width:{bar_w}%;background:{cor};height:10px;'
        f'border-radius:4px;min-width:2px"></div></div>'
        f'<span style="flex:0 0 38px;text-align:right;font-size:0.82rem;'
        f'font-weight:700;color:{cor}">{pct}%</span>'
        f'<span style="flex:0 0 28px;text-align:right;font-size:0.78rem;'
        f'color:#aaa">({n})</span>'
        f'</div>'
    )


def _secao_campeo(bracket_stats: dict, total: int):
    st.subheader("🏆 Campeão mais votado")
    final_picks = bracket_stats.get(("final", 1), Counter())
    if not final_picks:
        st.caption("Nenhum campeão escolhido ainda.")
        return
    top = final_picks.most_common(10)

    # Destaque do líder em card de pódio
    lider, n_lider = top[0]
    code = CODIGOS.get(lider, "un")
    pct = _pct(n_lider, total)
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#FBF1D8 0%,#F7E3A8 100%);'
        f'border:1px solid #EBD58A;border-radius:16px;padding:1rem 1.1rem;'
        f'display:flex;align-items:center;gap:14px;margin-bottom:12px">'
        f'<img src="{FLAG_BASE.replace("w40","w80")}/{code}.png" '
        f'style="height:42px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.18)">'
        f'<div style="flex:1;min-width:0">'
        f'<div style="font-size:0.72rem;letter-spacing:.06em;text-transform:uppercase;'
        f'color:#A07A00;font-weight:700">Favorito ao título</div>'
        f'<div style="font-size:1.25rem;font-weight:800;color:#5C4500;'
        f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{lider}</div>'
        f'</div>'
        f'<div style="text-align:right;flex-shrink:0">'
        f'<div style="font-size:1.5rem;font-weight:800;color:#C8860B;line-height:1">{pct}%</div>'
        f'<div style="font-size:0.72rem;color:#A07A00">{n_lider} voto(s)</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    if len(top) > 1:
        html = "".join(_barra(t, n, total, "#e6a817") for t, n in top[1:])
        st.markdown(f'<div>{html}</div>', unsafe_allow_html=True)


def _secao_grupos(group_stats: dict, total: int):
    st.subheader("📋 Fase de Grupos")
    for letra, times in GRUPOS.items():
        stats = group_stats.get(letra, {})
        with st.expander(f"Grupo {letra}", expanded=False):
            for pos_key, label, cor in [
                ("primeiro", "🥇 1º lugar", "#e6a817"),
                ("segundo", "🥈 2º lugar", "#9e9e9e"),
                ("terceiro", "🥉 3º lugar", "#cd7f32"),
            ]:
                st.markdown(f"**{label}**")
                counter = stats.get(pos_key, Counter())
                sorted_times = sorted(
                    times, key=lambda t: counter.get(t, 0), reverse=True
                )
                html = "".join(
                    _barra(t, counter.get(t, 0), total, cor) for t in sorted_times
                )
                st.markdown(
                    f'<div style="margin-bottom:14px">{html}</div>',
                    unsafe_allow_html=True,
                )


def _secao_mata_mata(bracket_stats: dict, total: int):
    st.subheader("⚔️ Mata-Mata")
    fases = [
        ("sf", "Semifinais", 2),
        ("qf", "Quartas de Final", 4),
        ("r16", "Oitavas de Final", 8),
        ("r32", "16 Avos de Final", 16),
        ("3p", "Disputa 3º Lugar", 1),
    ]
    for fase_key, fase_nome, n_jogos in fases:
        picks_fase = [bracket_stats.get((fase_key, j), Counter()) for j in range(1, n_jogos + 1)]
        if not any(picks_fase):
            continue
        with st.expander(fase_nome, expanded=False):
            for j, picks in enumerate(picks_fase, start=1):
                if not picks:
                    continue
                if n_jogos > 1:
                    st.caption(f"Jogo {j}")
                top = picks.most_common(5)
                html = "".join(_barra(t, n, total, "#009C3B") for t, n in top)
                st.markdown(
                    f'<div style="margin-bottom:10px">{html}</div>',
                    unsafe_allow_html=True,
                )


def render():
    st.markdown(
        """
        <div class="bolao-hero">
            <div class="emoji">📊</div>
            <h1>Resultados do Bolão</h1>
            <p>Consolidado de todos os palpites registrados</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_v, col_r = st.columns([1, 1])
    with col_v:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.pagina = "cadastro"
            st.rerun()
    with col_r:
        if st.button("🔄 Atualizar", use_container_width=True):
            _carregar_dados.clear()
            st.rerun()

    st.divider()

    with st.spinner("Carregando resultados..."):
        total, palpites, chaveamento = _carregar_dados()

    st.metric("👥 Total de participantes", total)

    if total == 0:
        st.info("Nenhum palpite registrado ainda. Seja o primeiro!")
        return

    # Agrega palpites de grupo
    group_stats: dict = {}
    for row in palpites:
        g = row["grupo"]
        if g not in group_stats:
            group_stats[g] = {
                "primeiro": Counter(),
                "segundo": Counter(),
                "terceiro": Counter(),
            }
        if row.get("primeiro_lugar"):
            group_stats[g]["primeiro"][row["primeiro_lugar"]] += 1
        if row.get("segundo_lugar"):
            group_stats[g]["segundo"][row["segundo_lugar"]] += 1
        if row.get("terceiro_lugar"):
            group_stats[g]["terceiro"][row["terceiro_lugar"]] += 1

    # Agrega palpites do chaveamento
    bracket_stats: dict = {}
    for row in chaveamento:
        key = (row["fase"], int(row["jogo_num"]))
        if key not in bracket_stats:
            bracket_stats[key] = Counter()
        if row.get("vencedor"):
            bracket_stats[key][row["vencedor"]] += 1

    st.divider()
    _secao_campeo(bracket_stats, total)

    st.divider()
    _secao_grupos(group_stats, total)

    st.divider()
    _secao_mata_mata(bracket_stats, total)
