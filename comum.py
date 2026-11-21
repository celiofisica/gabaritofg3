"""Utilidades compartilhadas pelo gabarito interativo de Física Geral III."""
from __future__ import annotations

import numpy as np
import streamlit as st

MU0 = 4e-7 * np.pi  # T·m/A

PALETA = {
    "azul": "#2563eb",
    "vermelho": "#dc2626",
    "verde": "#16a34a",
    "laranja": "#ea580c",
    "roxo": "#7c3aed",
    "cinza": "#6b7280",
}


def configurar_pagina(titulo: str, icone: str = "🧲") -> None:
    st.markdown(
        """
        <style>
        .caixa-dica {background:#eff6ff;border-left:5px solid #2563eb;padding:0.8rem 1rem;border-radius:6px;margin:0.4rem 0;}
        .caixa-alerta {background:#fef2f2;border-left:5px solid #dc2626;padding:0.8rem 1rem;border-radius:6px;margin:0.4rem 0;}
        .caixa-ok {background:#f0fdf4;border-left:5px solid #16a34a;padding:0.8rem 1rem;border-radius:6px;margin:0.4rem 0;}
        .caixa-fisica {background:#faf5ff;border-left:5px solid #7c3aed;padding:0.8rem 1rem;border-radius:6px;margin:0.4rem 0;}
        .enunciado {background:#f8fafc;border:1px solid #e2e8f0;padding:1rem 1.2rem;border-radius:8px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def caixa(texto: str, tipo: str = "dica") -> None:
    """Caixa colorida. tipo ∈ {dica, alerta, ok, fisica}. Aceita markdown simples."""
    st.markdown(f'<div class="caixa-{tipo}">{texto}</div>', unsafe_allow_html=True)


def fmt(valor: float, unidade: str = "", sig: int = 3) -> str:
    """Formata número em notação de engenharia com prefixo SI e vírgula decimal."""
    if valor == 0 or not np.isfinite(valor):
        return f"{valor} {unidade}".strip()
    prefixos = {-12: "p", -9: "n", -6: "μ", -3: "m", 0: "", 3: "k", 6: "M"}
    exp = int(np.floor(np.log10(abs(valor)) / 3) * 3)
    exp = max(min(exp, 6), -12)
    mant = valor / 10**exp
    texto = f"{mant:.{sig}g}".replace(".", ",")
    return f"{texto} {prefixos[exp]}{unidade}".strip()


def confira(rotulo: str, correto: float, unidade: str, chave: str,
            tol: float = 0.03, escala: float = 1.0, dica_erro: str | None = None) -> None:
    """Campo para o aluno digitar sua resposta e receber feedback imediato.

    `escala` converte a unidade digitada para SI (ex.: μT → 1e-6).
    """
    col1, col2 = st.columns([2, 3])
    with col1:
        valor = st.number_input(f"{rotulo} [{unidade}]", value=None, format="%.4g",
                                key=chave, placeholder="digite sua resposta")
    with col2:
        if valor is None:
            st.write("")
            st.caption("Digite seu resultado para conferir (tolerância de ±3%).")
            return
        v_si = valor * escala
        erro = abs(v_si - correto) / abs(correto)
        if erro <= tol:
            st.success(f"✅ Correto! Valor de referência: {f'{correto/escala:.4g}'.replace('.', ',')} {unidade}")
        elif abs(abs(v_si) - abs(correto)) / abs(correto) <= tol:
            st.warning("⚠️ O módulo está certo, mas o sinal não. Reveja a convenção de sentido/fase.")
        else:
            razao = v_si / correto
            msg = f"❌ Ainda não. Seu valor difere {erro*100:.0f}% do esperado."
            for pot in (1e3, 1e6, 1e-3, 1e-6, 10, 0.1):
                if abs(razao / pot - 1) < tol:
                    msg += " Parece um erro de **prefixo/potência de 10** — confira as unidades!"
                    break
            else:
                if abs(razao / (2 * np.pi) - 1) < tol or abs(razao * 2 * np.pi - 1) < tol:
                    msg += " Diferença de um fator **2π**: confundiu f com ω?"
                elif abs(razao / 2 - 1) < tol or abs(razao * 2 - 1) < tol:
                    msg += " Diferença de um fator **2**: reveja o fator ½ (ou a amplitude × valor eficaz)."
            if dica_erro:
                msg += f"\n\n💡 {dica_erro}"
            st.error(msg)


def passos(lista: list[tuple[str, callable]]) -> None:
    """Renderiza uma resolução em passos revelados progressivamente (expanders)."""
    for i, (titulo, corpo) in enumerate(lista, start=1):
        with st.expander(f"Passo {i} — {titulo}"):
            corpo()


def quiz(pergunta: str, opcoes: list[str], correta: int, explicacao: str, chave: str) -> None:
    st.markdown(f"**{pergunta}**")
    escolha = st.radio("Escolha:", opcoes, index=None, key=chave, label_visibility="collapsed")
    if escolha is not None:
        if opcoes.index(escolha) == correta:
            st.success("✅ Isso mesmo! " + explicacao)
        else:
            st.error("❌ Não é essa. " + explicacao)


def rodape() -> None:
    st.divider()
    st.caption("Física Geral III — IFES Campus Vitória · Gabarito interativo · "
               "Use as setas da barra lateral para navegar entre as questões.")
