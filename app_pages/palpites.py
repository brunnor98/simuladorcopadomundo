import streamlit as st
from data.times import GRUPOS, CODIGOS, country_emoji

FLAG_BASE = "https://flagcdn.com/w40"


def _lista_times(times: list) -> str:
    linhas = ""
    for t in times:
        code = CODIGOS.get(t, "un")
        linhas += (
            f'<div style="display:flex;align-items:center;padding:4px 0;border-bottom:1px solid #f0f0f0">'
            f'<img src="{FLAG_BASE}/{code}.png" '
            f'style="width:28px;height:19px;object-fit:cover;border-radius:2px;'
            f'flex-shrink:0;margin-right:8px;">'
            f'<span style="font-size:0.9rem;line-height:1.25">{t}</span>'
            f'</div>'
        )
    return f'<div style="margin:4px 0 10px 0">{linhas}</div>'


def _fmt(time: str | None) -> str:
    if not time:
        return ""
    return f"{country_emoji(time)} {time}"


def _opcoes_filtradas(times: list, *excluir) -> list:
    """Retorna times excluindo os já selecionados em outras posições."""
    excluidos = {t for t in excluir if t}
    return [t for t in times if t not in excluidos]


def _resetar_se_invalido(key: str, opcoes: list) -> None:
    """Limpa session_state se o valor atual não está mais nas opções."""
    if st.session_state.get(key) not in opcoes:
        st.session_state[key] = None


def render():
    participante = st.session_state.participante

    st.markdown(
        f"""
        <div class="bolao-hero">
            <div class="emoji">⚽</div>
            <h1>Fase de Grupos</h1>
            <p>Olá, <strong>{participante['nome']}</strong>! Selecione 1º, 2º e 3º de cada grupo.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Selecione **1º, 2º e 3º** de cada grupo. "
        "Depois, escolha **8 dos 12 terceiros colocados** que avançarão para o mata-mata.",
        icon="ℹ️",
    )

    st.divider()

    selecoes = {}
    grupos = list(GRUPOS.items())

    for i in range(0, len(grupos), 2):
        col1, col2 = st.columns(2)
        for j, col in enumerate([col1, col2]):
            if i + j >= len(grupos):
                break
            letra, times = grupos[i + j]
            k1, k2, k3 = f"g{letra}_1", f"g{letra}_2", f"g{letra}_3"

            # Lê seleções atuais para filtrar as próximas
            p1 = st.session_state.get(k1)
            p2 = st.session_state.get(k2)

            opcoes_2 = _opcoes_filtradas(times, p1)
            opcoes_3 = _opcoes_filtradas(times, p1, p2)

            # Reseta se a seleção ficou inválida após mudança em outra posição
            _resetar_se_invalido(k2, opcoes_2)
            _resetar_se_invalido(k3, opcoes_3)

            with col:
                with st.container(border=True):
                    st.markdown(f"**Grupo {letra}**")
                    st.markdown(_lista_times(times), unsafe_allow_html=True)

                    primeiro = st.selectbox(
                        "🥇 1º lugar", times,
                        key=k1, index=None,
                        format_func=_fmt,
                        placeholder="Selecione o 1º colocado...",
                    )
                    segundo = st.selectbox(
                        "🥈 2º lugar", opcoes_2,
                        key=k2, index=None,
                        format_func=_fmt,
                        placeholder="Selecione o 2º colocado...",
                    )
                    terceiro = st.selectbox(
                        "🥉 3º lugar", opcoes_3,
                        key=k3, index=None,
                        format_func=_fmt,
                        placeholder="Selecione o 3º colocado...",
                    )
                    selecoes[letra] = {
                        "primeiro": primeiro,
                        "segundo": segundo,
                        "terceiro": terceiro,
                    }

    # --- Seção: quais 3ºs colocados avançam ---
    st.divider()
    st.subheader("🏆 Quais 3ºs colocados avançam?")
    st.caption("Selecione exatamente 8 dos 12 terceiros colocados que passarão para o mata-mata.")

    terceiros_por_grupo = {
        letra: s["terceiro"]
        for letra, s in selecoes.items()
        if s["terceiro"]
    }
    n_terceiros = len(terceiros_por_grupo)

    if n_terceiros < 12:
        st.warning(
            f"Preencha o **3º lugar de todos os grupos** para liberar esta seleção. "
            f"({n_terceiros}/12 grupos preenchidos)"
        )
        avancam = []
    else:
        avancam = st.multiselect(
            "3ºs colocados que avançam",
            options=list(terceiros_por_grupo.values()),
            max_selections=8,
            format_func=_fmt,
            key="terceiros_avancam",
            placeholder="Selecione 8 times...",
        )
        n_sel = len(avancam)
        if n_sel == 8:
            st.success(f"✅ {n_sel}/8 selecionados")
        else:
            st.caption(f"⚠️ {n_sel}/8 selecionados")

    st.divider()

    col_voltar, col_enviar = st.columns([1, 3])
    with col_voltar:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.pagina = "cadastro"
            st.rerun()
    with col_enviar:
        if st.button(
            "Avançar para o Chaveamento →",
            type="primary",
            use_container_width=True,
        ):
            _validar_e_avancar(selecoes, avancam)


def _validar_e_avancar(selecoes, avancam):
    incompletos = [
        g for g, p in selecoes.items()
        if not p["primeiro"] or not p["segundo"] or not p["terceiro"]
    ]
    if incompletos:
        st.error(f"Preencha 1º, 2º e 3º lugar dos grupos: **{', '.join(incompletos)}**")
        return

    if len(avancam) != 8:
        st.error(f"Selecione exatamente **8 terceiros colocados** que avançam. ({len(avancam)}/8 selecionados)")
        return

    # Armazena explicitamente para não depender dos widget-keys no próximo render
    st.session_state["_selecoes"] = selecoes
    st.session_state["_avancam"] = list(avancam)
    st.session_state.pagina = "chaveamento"
    st.rerun()
