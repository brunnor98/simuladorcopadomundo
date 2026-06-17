import os

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def _credencial(env_key: str, secrets_secao: str, secrets_chave: str) -> str:
    val = os.environ.get(env_key)
    if val:
        return val
    try:
        return st.secrets[secrets_secao][secrets_chave]
    except Exception:
        raise RuntimeError(
            f"Credencial '{env_key}' não encontrada. "
            f"Defina no .env (local) ou nos Secrets do Streamlit Cloud."
        )


@st.cache_resource
def get_supabase() -> Client:
    url = _credencial("SUPABASE_URL", "supabase", "url")
    key = _credencial("SUPABASE_KEY", "supabase", "key")
    return create_client(url, key)


def salvar_participante(nome: str, telefone: str, email: str) -> str:
    sb = get_supabase()
    resultado = sb.table("participantes").insert({
        "nome": nome,
        "telefone": telefone,
        "email": email,
    }).execute()
    return resultado.data[0]["id"]


def salvar_palpites(participante_id: str, palpites: dict, grupos_3_avancam: set) -> None:
    sb = get_supabase()
    linhas = [
        {
            "participante_id": participante_id,
            "grupo": grupo,
            "primeiro_lugar": dados["primeiro"],
            "segundo_lugar": dados["segundo"],
            "terceiro_lugar": dados["terceiro"],
            "terceiro_avanca": grupo in grupos_3_avancam,
        }
        for grupo, dados in palpites.items()
    ]
    sb.table("palpites").insert(linhas).execute()


def salvar_chaveamento(participante_id: str, picks: dict) -> None:
    sb = get_supabase()
    linhas = [
        {
            "participante_id": participante_id,
            "fase": fase,
            "jogo_num": jogo_num,
            "vencedor": vencedor,
        }
        for (fase, jogo_num), vencedor in picks.items()
    ]
    if linhas:
        sb.table("chaveamento").insert(linhas).execute()
