"""Página inicial do gabarito."""
from pathlib import Path

import streamlit as st

from comum import caixa, configurar_pagina, rodape

configurar_pagina("Gabarito FG-III", "🧲")

st.title("🧲 Física Geral III — Gabarito interativo")
st.subheader("Avaliação: Biot–Savart · Faraday · Indutância mútua · RLC · Alto-falante")

st.markdown(
    """
Este aplicativo é o **gabarito comentado** da avaliação. Ele não entrega só a resposta final:
cada questão foi pensada como uma pequena aula, para que você entenda **de onde** vem cada
resultado e **o que muda** quando os parâmetros mudam.
"""
)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("### Como usar cada página")
    st.markdown(
        """
| Aba | O que você encontra |
|---|---|
| 📝 **Enunciado** | A questão exatamente como na prova. |
| 🧭 **Estratégia** | Dicas progressivas: abra uma de cada vez e tente seguir sozinho. |
| ✍️ **Resolução** | Solução passo a passo, revelada aos poucos. |
| 🎛️ **Laboratório** | Simulações: mexa nos parâmetros e veja a física acontecer. |
| ✅ **Confira** | Digite seus resultados e receba retorno imediato (inclusive dicas sobre o tipo de erro). |
| 🧠 **Conceitos** | Perguntas rápidas e os erros mais comuns. |
"""
    )
    caixa(
        "<b>Sugestão de estudo:</b> antes de abrir a resolução, refaça a questão no papel. "
        "Depois use a aba <b>Confira</b>. Só então abra os passos — e compare o <i>raciocínio</i>, "
        "não apenas o número.",
        "dica",
    )

with col2:
    st.markdown("### Questões")
    st.page_link("q1_biot_savart.py", label="Q1 — Lei de Biot–Savart", icon="🌀")
    st.page_link("q2_faraday.py", label="Q2 — Lei de Faraday", icon="⚡")
    st.page_link("q3_indutancia_mutua.py", label="Q3 — Indutância mútua", icon="🔗")
    st.page_link("q4_rlc.py", label="Q4 — Circuito RLC série", icon="📈")
    st.page_link("q5_alto_falante.py", label="Q5 — Alto-falante e fone de ouvido", icon="🔊")

    pdf = Path(__file__).parent / "prova_fg3.pdf"
    if pdf.exists():
        st.download_button("⬇️ Baixar a prova (PDF)", pdf.read_bytes(),
                           file_name="prova_fg3.pdf", mime="application/pdf")

st.divider()
st.markdown("### O fio condutor da prova")
st.markdown(
    r"""
As cinco questões contam **uma única história**:

1. **Correntes criam campos** (Biot–Savart, Q1).
2. **Campos variáveis criam fems** (Faraday, Q2).
3. Juntando 1 e 2, um circuito “sente” o outro: **indutância mútua** (Q3).
4. Indutores e capacitores trocam energia: **ressonância no RLC** (Q4).
5. Tudo isso dentro de um objeto do dia a dia: o **alto-falante** — onde a força de Lorentz move o cone,
   a lei de Faraday gera uma fem de retorno e o sistema mecânico aparece para o amplificador
   **como um circuito RLC** (Q5).
"""
)

st.markdown("### Constantes e convenções")
st.latex(r"\mu_0 = 4\pi\times10^{-7}\ \mathrm{T\cdot m/A},\qquad \omega = 2\pi f,\qquad "
         r"\text{amplitudes indicadas pelo índice }0\ (I_0,\,V_0,\,\varepsilon_0).")

rodape()
