# Estrutura oficial do mata-mata da Copa do Mundo 2026 (32 seleções),
# conforme table/chaveamento_copa.pdf (página "FASES FINAIS").
#
# As 16 partidas dos 16-avos estão ordenadas por METADE da chave:
#   - ids 1–8  → caminho da SEMIFINAL 1 (metade de cima)
#   - ids 9–16 → caminho da SEMIFINAL 2 (metade de baixo)
# Confrontos consecutivos (1×2, 3×4, ...) se cruzam nas oitavas; o
# aninhamento segue para quartas e semifinais. Assim, dois 1ºs colocados
# de metades opostas só podem se enfrentar na FINAL — exatamente como no
# documento oficial (ex.: 1º C e 1º I).
#
# Vagas marcadas com "3" recebem um dos oito melhores terceiros colocados.
# "t3_groups" lista os grupos cujo 3º colocado pode ocupar aquela vaga,
# conforme a tabela oficial da FIFA.

R32 = [
    # ── Metade de cima → Semifinal 1 ──────────────────────────────────
    {"id": 1,  "t1": "1E", "t2": "3", "t3_groups": ["A", "B", "C", "D", "F"]},
    {"id": 2,  "t1": "1I", "t2": "3", "t3_groups": ["C", "D", "F", "G", "H"]},
    {"id": 3,  "t1": "2A", "t2": "2B"},
    {"id": 4,  "t1": "1F", "t2": "2C"},
    {"id": 5,  "t1": "2K", "t2": "2L"},
    {"id": 6,  "t1": "1H", "t2": "2J"},
    {"id": 7,  "t1": "1D", "t2": "3", "t3_groups": ["B", "E", "F", "I", "J"]},
    {"id": 8,  "t1": "1G", "t2": "3", "t3_groups": ["A", "E", "H", "I", "J"]},
    # ── Metade de baixo → Semifinal 2 ─────────────────────────────────
    {"id": 9,  "t1": "1C", "t2": "2F"},
    {"id": 10, "t1": "2E", "t2": "2I"},
    {"id": 11, "t1": "1A", "t2": "3", "t3_groups": ["C", "E", "F", "H", "I"]},
    {"id": 12, "t1": "1L", "t2": "3", "t3_groups": ["E", "H", "I", "J", "K"]},
    {"id": 13, "t1": "1J", "t2": "2H"},
    {"id": 14, "t1": "2D", "t2": "2G"},
    {"id": 15, "t1": "1B", "t2": "3", "t3_groups": ["E", "F", "G", "I", "J"]},
    {"id": 16, "t1": "1K", "t2": "3", "t3_groups": ["D", "E", "I", "J", "L"]},
]

# Vencedores de pares consecutivos avançam (mesma topologia em todas as fases)
R16_PAIRS = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]
QF_PAIRS  = [(1, 2), (3, 4), (5, 6), (7, 8)]
SF_PAIRS  = [(1, 2), (3, 4)]


def pos_label(src: str) -> str:
    if src == "3":
        return "3º Classif."
    pos = "1º" if src[0] == "1" else "2º"
    return f"{pos} Gr.{src[1]}"
