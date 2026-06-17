import streamlit as st


def render():
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 0.5rem;'>
            <span style='font-size:3rem'>⚽</span>
            <h1 style='margin:0; color:#009C3B'>Bolão da Copa do Mundo 2026</h1>
            <p style='color:#555; margin-top:0.25rem'>Faça seus palpites e concorra a prêmios!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    col_esq, col_form, col_dir = st.columns([1, 2, 1])
    with col_form:
        st.subheader("Seus dados")
        st.caption("Preencha para participar do bolão.")

        with st.form("form_cadastro"):
            nome = st.text_input("Nome completo", placeholder="Ex: João da Silva")
            telefone = st.text_input("Telefone (WhatsApp)", placeholder="Ex: (11) 99999-9999")
            email = st.text_input("E-mail", placeholder="Ex: joao@email.com")

            enviado = st.form_submit_button(
                "Próximo: fazer palpites →",
                type="primary",
                use_container_width=True,
            )

        if enviado:
            if not nome.strip() or not telefone.strip() or not email.strip():
                st.error("Preencha todos os campos para continuar.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Digite um e-mail válido.")
            else:
                st.session_state.participante = {
                    "nome": nome.strip(),
                    "telefone": telefone.strip(),
                    "email": email.strip(),
                }
                st.session_state.pagina = "palpites"
                st.rerun()
