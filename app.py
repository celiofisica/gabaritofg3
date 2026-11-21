"""Gabarito interativo — Avaliação de Física Geral III (Eletromagnetismo).

Execute com:  streamlit run app.py
Todos os arquivos ficam na MESMA pasta (sem subpastas).
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(page_title="Gabarito FG-III", page_icon="🧲", layout="wide")

paginas = [
    st.Page("inicio.py", title="Início", icon="🧲", default=True),
    st.Page("q1_biot_savart.py", title="Q1 — Biot–Savart", icon="🌀"),
    st.Page("q2_faraday.py", title="Q2 — Lei de Faraday", icon="⚡"),
    st.Page("q3_indutancia_mutua.py", title="Q3 — Indutância mútua", icon="🔗"),
    st.Page("q4_rlc.py", title="Q4 — Circuito RLC", icon="📈"),
    st.Page("q5_alto_falante.py", title="Q5 — Alto-falante", icon="🔊"),
]
st.navigation(paginas).run()
