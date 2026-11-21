"""Modelos físicos usados no gabarito (funções puras, testáveis sem Streamlit)."""
from __future__ import annotations

import numpy as np
from scipy.integrate import trapezoid
from scipy.special import ellipe, ellipk

MU0 = 4e-7 * np.pi


# ---------------------------------------------------------------- Questão 1
def B_eixo_espira(I, a, z):
    """Campo no eixo de uma espira circular (analítico)."""
    return MU0 * I * a**2 / (2 * (a**2 + z**2) ** 1.5)


def B_dipolo_eixo(I, a, z):
    m = I * np.pi * a**2
    return MU0 * m / (2 * np.pi * np.abs(z) ** 3)


def biot_savart_numerico(pontos_fio: np.ndarray, I: float, r_obs: np.ndarray) -> np.ndarray:
    """Integra Biot–Savart numericamente para um fio poligonal fechado.

    pontos_fio: (N,3) vértices em sequência (o último é ligado ao primeiro).
    r_obs: (3,) ponto de observação. Retorna o vetor B (T).
    """
    p = np.asarray(pontos_fio, float)
    dl = np.roll(p, -1, axis=0) - p
    meio = p + dl / 2
    r = r_obs - meio
    rn = np.linalg.norm(r, axis=1)[:, None]
    dB = MU0 * I / (4 * np.pi) * np.cross(dl, r) / rn**3
    return dB.sum(axis=0)


def espira_circular_pts(a, n=2000):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.column_stack([a * np.cos(t), a * np.sin(t), np.zeros_like(t)])


def B_centro_poligono(I, N, apotema):
    """Campo no centro de um polígono regular de N lados (apótema d)."""
    return MU0 * I * N * np.sin(np.pi / N) / (2 * np.pi * apotema)


# ---------------------------------------------------------------- Questão 2
def fluxo_fio_espira(I, ell, w, x):
    return MU0 * I * ell / (2 * np.pi) * np.log((x + w) / x)


def fem_espira_afastando(I, ell, w, x, v):
    return MU0 * I * ell * w * v / (2 * np.pi * x * (x + w))


def fem_mov_lados(I, ell, w, x, v):
    """Fem de movimento: lado próximo menos lado distante (B·ℓ·v em cada)."""
    B1 = MU0 * I / (2 * np.pi * x)
    B2 = MU0 * I / (2 * np.pi * (x + w))
    return B1 * ell * v, B2 * ell * v


# ---------------------------------------------------------------- Questão 3
def M_aprox(R1, R2, N2=1, N1=1):
    return MU0 * np.pi * N1 * N2 * R2**2 / (2 * R1)


def M_exato(R1, R2, N2=1, N1=1, d=0.0):
    """Indutância mútua exata de duas espiras coaxiais (fórmula de Maxwell)."""
    m = 4 * R1 * R2 / ((R1 + R2) ** 2 + d**2)
    k = np.sqrt(m)
    return N1 * N2 * MU0 * np.sqrt(R1 * R2) * ((2 / k - k) * ellipk(m) - 2 / k * ellipe(m))


def Bz_plano_espira(I, R, rho):
    """Componente z do campo no plano de uma espira (ρ < R), via integrais elípticas."""
    rho = np.asarray(rho, float)
    m = 4 * R * rho / (R + rho) ** 2
    return MU0 * I / (2 * np.pi) / (R + rho) * (ellipk(m) + (R**2 - rho**2) / (R - rho) ** 2 * ellipe(m))


def M_integrando_fluxo(R1, R2, N2=1, n=4000):
    """M obtido integrando numericamente o fluxo de B_z(ρ) sobre o disco de raio R2."""
    rho = np.linspace(0, R2, n)
    integrando = Bz_plano_espira(1.0, R1, rho) * 2 * np.pi * rho
    return N2 * trapezoid(integrando, rho)


# ---------------------------------------------------------------- Questão 4
def rlc_serie(R, L, C, V0, f):
    w = 2 * np.pi * np.asarray(f, float)
    XL, XC = w * L, 1 / (w * C)
    Z = np.sqrt(R**2 + (XL - XC) ** 2)
    I0 = V0 / Z
    phi = np.arctan2(XL - XC, R)
    P = 0.5 * I0**2 * R
    return dict(w=w, XL=XL, XC=XC, Z=Z, I0=I0, phi=phi, P=P)


def rlc_livre(R, L, C, q0, t):
    """Carga q(t) no RLC livre com q(0)=q0, i(0)=0 — todos os regimes."""
    a = R / (2 * L)
    w0 = 1 / np.sqrt(L * C)
    t = np.asarray(t, float)
    if np.isclose(a, w0, rtol=1e-6):
        return q0 * (1 + a * t) * np.exp(-a * t), "crítico"
    if a < w0:
        wd = np.sqrt(w0**2 - a**2)
        return q0 * np.exp(-a * t) * (np.cos(wd * t) + a / wd * np.sin(wd * t)), "subamortecido"
    s = np.sqrt(a**2 - w0**2)
    r1, r2 = -a + s, -a - s
    A = q0 * r2 / (r2 - r1)
    B = -q0 * r1 / (r2 - r1)
    return A * np.exp(r1 * t) + B * np.exp(r2 * t), "superamortecido"


# ---------------------------------------------------------------- Questão 5
def falante_Z(f, Bl, Re, Le, m, k, b):
    w = 2 * np.pi * np.asarray(f, float)
    Zm = b + 1j * w * m + k / (1j * w)  # impedância mecânica
    return Re + 1j * w * Le + Bl**2 / Zm


def falante_resposta(f, V0, Bl, Re, Le, m, k, b):
    """Corrente, velocidade, deslocamento e fem de retorno para tensão de amplitude V0."""
    w = 2 * np.pi * np.asarray(f, float)
    Z = falante_Z(f, Bl, Re, Le, m, k, b)
    i = V0 / Z
    Zm = b + 1j * w * m + k / (1j * w)
    v = Bl * i / Zm
    x = v / (1j * w)
    return dict(Z=Z, i=i, v=v, x=x, fem=Bl * v)
