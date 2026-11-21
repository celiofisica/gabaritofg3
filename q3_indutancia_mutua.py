import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from comum import caixa, configurar_pagina, confira, fmt, passos, quiz, rodape
from modelos import MU0, Bz_plano_espira, M_aprox, M_exato, M_integrando_fluxo

configurar_pagina("Q3 — Indutância mútua", "🔗")
st.title("🔗 Questão 3 — Indutância mútua entre espiras concêntricas")

R1, R2, N2, I0, f, Rr, L2 = 0.20, 0.02, 50, 3.0, 1000.0, 0.50, 0.25e-3
om = 2 * np.pi * f
M = M_aprox(R1, R2, N2)
Mex = M_exato(R1, R2, N2)
eps0 = M * I0 * om
XL2 = om * L2
Z2 = np.hypot(Rr, XL2)
i20 = eps0 / Z2
fase = np.degrees(np.arctan(XL2 / Rr))

abas = st.tabs(["📝 Enunciado", "🧭 Estratégia", "✍️ Resolução", "🎛️ Laboratório", "✅ Confira", "🧠 Conceitos"])

with abas[0]:
    with st.container(border=True):
        st.markdown(
            r"""

Duas espiras circulares coplanares e concêntricas têm raios $R_1 = 20$ cm e $R_2 = 2{,}0$ cm ($R_1\gg R_2$).
A maior tem uma volta e conduz $i_1(t) = I_0\sin\omega t$, com $I_0 = 3{,}0$ A e $f = 1{,}0$ kHz. A menor é uma pequena bobina de
$N_2 = 50$ voltas, com resistência $R = 0{,}50\ \Omega$ e autoindutância $L_2 = 0{,}25$ mH, fechada sobre si mesma.

**(a)** *(5 pts)* Justifique por que o campo de $i_1$ pode ser considerado uniforme sobre a espira menor e mostre que
$M\approx\dfrac{\mu_0\pi N_2R_2^2}{2R_1}$. Calcule $M$.

**(b)** *(5 pts)* Obtenha $\varepsilon_2(t)$ e sua amplitude.

**(c)** *(6 pts)* Determine a amplitude de $i_2(t)$ e o atraso de fase de $i_2$ em relação a $\varepsilon_2$. É razoável desprezar $L_2$? Justifique numericamente.

**(d)** *(4 pts)* Se a corrente $I_0\sin\omega t$ circulasse na bobina menor, qual seria a amplitude da fem na espira maior?
Por que calcular isso **diretamente** seria muito mais trabalhoso?
"""
        )

with abas[1]:
    with st.expander("Dica 1 — Qual é o campo no centro da espira grande?"):
        st.markdown(r"Você já calculou na Questão 1: $B(0) = \mu_0 i_1/(2R_1)$.")
    with st.expander("Dica 2 — Quanto o campo varia até ρ = R₂?"):
        st.markdown(r"No plano da espira, perto do centro, $B_z(\rho)\approx B(0)\left[1+\tfrac34(\rho/R_1)^2\right]$. Com $\rho/R_1 = 0{,}1$, a variação é < 1%.")
    with st.expander("Dica 3 — Definição de M"):
        st.markdown(r"$N_2\Phi_{21} = M\,i_1$: o fluxo **concatenado** (todas as voltas!) na bobina 2 por unidade de corrente na espira 1.")
    with st.expander("Dica 4 — Circuito da bobina menor"):
        st.markdown(r"A bobina menor é um circuito **RL série** excitado pela fem $\varepsilon_2$: impedância $Z = \sqrt{R^2 + (\omega L_2)^2}$.")
    with st.expander("Dica 5 — Reciprocidade"):
        st.markdown(r"$M_{12} = M_{21}$ sempre (teorema de Neumann). Use o resultado que já tem!")

with abas[2]:
    st.markdown("#### Item (a) — Aproximação e cálculo de M")

    def a1():
        st.markdown(r"O campo no plano da espira grande, a uma distância $\rho$ do centro, cresce conforme nos aproximamos do fio. "
                    r"Expandindo para $\rho\ll R_1$:")
        st.latex(r"B_z(\rho) \approx \frac{\mu_0 i_1}{2R_1}\left[1 + \frac34\left(\frac{\rho}{R_1}\right)^2 + \dots\right]")
        st.markdown(r"Com $\rho\le R_2 = 0{,}1R_1$, a correção é no máximo $0{,}75\%$: o campo é **praticamente uniforme** sobre a espira menor. "
                    r"Veja o gráfico na aba **Laboratório**.")

    def a2():
        st.latex(r"\Phi_{21} \approx B(0)\,\pi R_2^2 = \frac{\mu_0 i_1}{2R_1}\pi R_2^2")
        st.latex(r"M = \frac{N_2\Phi_{21}}{i_1} = \boxed{\frac{\mu_0\pi N_2 R_2^2}{2R_1}}")
        st.markdown(r"Note: $M$ **não depende de $i_1$** nem do tempo — é puramente geométrico (forma, tamanho, posição, número de voltas).")

    def a3():
        st.latex(r"M = \frac{(4\pi\times10^{-7})\,\pi\,(50)(0{,}02)^2}{2(0{,}20)}")
        st.markdown(f"**M ≈ {fmt(M,'H')}**  (por volta: {fmt(M/N2,'H')})")
        caixa(f"<b>Quão boa é a aproximação?</b> A fórmula exata (de Maxwell, com integrais elípticas) dá M = {fmt(Mex,'H')}: "
              f"diferença de apenas {100*(Mex/M-1):.2f}%. O valor exato é ligeiramente <i>maior</i>, porque B cresce em direção ao fio.", "ok")

    passos([("Justificando a uniformidade", a1), ("Fluxo e definição de M", a2), ("Valor numérico", a3)])

    st.markdown("#### Item (b) — Fem induzida")

    def b1():
        st.latex(r"\varepsilon_2(t) = -M\frac{di_1}{dt} = -M I_0\omega\cos\omega t")
        st.latex(r"\varepsilon_0 = M I_0\omega = (1{,}974\times10^{-7})(3{,}0)(2\pi\times10^3)")
        st.markdown(f"**ε₀ ≈ {fmt(eps0,'V')}**")

    passos([("Lei de Faraday com M", b1)])

    st.markdown("#### Item (c) — Corrente induzida")

    def c1():
        st.latex(r"X_{L_2} = \omega L_2 = (2\pi\times10^3)(0{,}25\times10^{-3}) \approx " + f"{XL2:.2f}".replace('.', '{,}') + r"\ \Omega")
        st.markdown(f"Isso é **maior** que R = 0,50 Ω! A reatância domina.")

    def c2():
        st.latex(r"|Z_2| = \sqrt{R^2 + (\omega L_2)^2} = \sqrt{0{,}50^2 + 1{,}571^2}\approx " + f"{Z2:.3f}".replace('.', '{,}') + r"\ \Omega")
        st.latex(r"i_{2,0} = \frac{\varepsilon_0}{|Z_2|} \approx " + f"{i20*1e3:.2f}".replace('.', '{,}') + r"\ \text{mA}")
        st.latex(r"\tan\delta = \frac{\omega L_2}{R}\ \Rightarrow\ \delta \approx " + f"{fase:.1f}".replace('.', '{,}') + r"^\circ\ \text{(atraso de } i_2 \text{ em relação a } \varepsilon_2)")

    def c3():
        st.markdown(f"Desprezando L₂ teríamos i₂,₀ = ε₀/R ≈ {fmt(eps0/Rr,'A')} — cerca de **{eps0/Rr/i20:.1f}× maior** que o valor correto. "
                    "**Não** é razoável desprezar L₂ nesta frequência.")
        caixa("Regra prática: só podemos desprezar a autoindutância quando ωL ≪ R. Aqui ωL/R ≈ 3,1. "
              "Em 60 Hz, ωL₂ seria ≈ 0,094 Ω e a aproximação passaria a ser aceitável (erro ≈ 2%).", "fisica")

    passos([("Reatância da bobina menor", c1), ("Impedância, corrente e fase", c2), ("Dá para desprezar L₂?", c3)])

    st.markdown("#### Item (d) — Reciprocidade")

    def d1():
        st.markdown(r"Pelo **teorema de reciprocidade** (fórmula de Neumann), $M_{12} = M_{21} = M$:")
        st.latex(r"M = \frac{\mu_0}{4\pi}N_1N_2\oint_1\oint_2\frac{d\vec\ell_1\cdot d\vec\ell_2}{|\vec r_1-\vec r_2|}")
        st.markdown(r"A expressão é **simétrica** na troca $1\leftrightarrow2$. Portanto a amplitude da fem na espira maior é a mesma: "
                    + f"**ε₀ ≈ {fmt(eps0,'V')}**.")

    def d2():
        caixa("<b>Por que é difícil diretamente?</b> A bobina menor se comporta, longe dela, como um dipolo magnético. "
              "O fluxo através da espira grande exige integrar o campo do dipolo sobre toda a área de raio R₁ — e esse campo "
              "<i>não</i> é uniforme: ele é intenso e positivo perto da bobina pequena e negativo (retorna) no resto do plano. "
              "Há cancelamentos delicados e uma singularidade junto à bobina pequena. A reciprocidade nos poupa todo esse trabalho.", "fisica")

    passos([("M₁₂ = M₂₁", d1), ("A dificuldade do cálculo direto", d2)])

with abas[3]:
    st.markdown("### 1. O campo é mesmo uniforme sobre a espira menor?")
    c1, c2 = st.columns([1, 3])
    with c1:
        R1l = st.slider("R₁ (cm)", 5.0, 50.0, 20.0, 1.0) / 100
        R2l = st.slider("R₂ (cm)", 0.5, 45.0, 2.0, 0.5) / 100
        if R2l >= R1l:
            st.error("R₂ precisa ser menor que R₁.")
            R2l = 0.9 * R1l
        N2l = st.slider("N₂ (voltas)", 1, 200, 50)
    with c2:
        rho = np.linspace(0, 0.97 * R1l, 400)
        Bn = Bz_plano_espira(1.0, R1l, rho) / (MU0 / (2 * R1l))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rho / R1l, y=Bn, name="B_z(ρ)/B(0) — exato", line=dict(color="#2563eb", width=3)))
        fig.add_trace(go.Scatter(x=rho / R1l, y=1 + 0.75 * (rho / R1l) ** 2, name="1 + ¾(ρ/R₁)²", line=dict(color="#16a34a", dash="dash")))
        fig.add_vrect(x0=0, x1=R2l / R1l, fillcolor="#dc2626", opacity=0.12, line_width=0, annotation_text="área da espira menor")
        fig.update_layout(xaxis_title="ρ / R₁", yaxis_title="B_z / B(0)", height=380, yaxis_range=[0.9, 4])
        st.plotly_chart(fig, width="stretch")

    Ma, Me, Mn = M_aprox(R1l, R2l, N2l), M_exato(R1l, R2l, N2l), M_integrando_fluxo(R1l, R2l, N2l)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("M aproximado", fmt(Ma, "H"))
    m2.metric("M exato (Maxwell)", fmt(Me, "H"))
    m3.metric("M (integração numérica do fluxo)", fmt(Mn, "H"))
    m4.metric("Erro da aproximação", f"{100*(Ma/Me-1):+.2f} %")
    with st.expander("Ver a fórmula exata de Maxwell"):
        st.latex(r"M = \mu_0\sqrt{R_1R_2}\left[\left(\frac2k-k\right)K(k)-\frac2kE(k)\right],\qquad k^2=\frac{4R_1R_2}{(R_1+R_2)^2}")
        st.markdown("K e E são as integrais elípticas completas de 1ª e 2ª espécie. Para k → 0 ela se reduz à nossa aproximação.")

    st.markdown("### 2. Até onde vale a aproximação?")
    razoes = np.linspace(0.01, 0.95, 200)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=razoes, y=M_exato(1, razoes) / (MU0), name="exato", line=dict(color="#2563eb", width=3)))
    fig.add_trace(go.Scatter(x=razoes, y=M_aprox(1, razoes) / MU0, name="aproximação μ₀πR₂²/2R₁", line=dict(color="#ea580c", dash="dash")))
    fig.add_vline(x=R2l / R1l, line_dash="dot", annotation_text="sua escolha")
    fig.update_layout(xaxis_title="R₂/R₁", yaxis_title="M / (μ₀ R₁)  (por volta)", height=360, yaxis_type="log")
    st.plotly_chart(fig, width="stretch")
    caixa("Para R₂/R₁ ≲ 0,2 a aproximação é excelente (erro < 2%). Quando as espiras têm raios próximos, M cresce muito mais "
          "(logaritmicamente divergente) porque os fios ficam muito próximos — a aproximação de campo uniforme falha completamente.", "dica")

    st.markdown("### 3. Sinais no tempo: i₁, ε₂ e i₂")
    c1, c2 = st.columns([1, 3])
    with c1:
        fl = st.select_slider("Frequência f (Hz)", [50, 60, 100, 200, 500, 1000, 2000, 5000, 10000], 1000)
        Rl = st.slider("R da bobina menor (Ω)", 0.05, 5.0, 0.50, 0.05)
        L2l = st.slider("L₂ (mH)", 0.0, 1.0, 0.25, 0.05) * 1e-3
    with c2:
        oml = 2 * np.pi * fl
        Mloc = M_aprox(R1, R2, N2)
        t = np.linspace(0, 2 / fl, 600)
        i1 = I0 * np.sin(oml * t)
        e2 = -Mloc * I0 * oml * np.cos(oml * t)
        Zc = Rl + 1j * oml * L2l
        e2c = -Mloc * I0 * oml * 1.0  # amplitude complexa de -cos
        i2 = np.real((Mloc * I0 * oml / Zc) * (-1) * np.exp(1j * oml * t))
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08)
        fig.add_trace(go.Scatter(x=t * 1e3, y=i1, name="i₁ (A)", line=dict(color="#2563eb")), row=1, col=1)
        fig.add_trace(go.Scatter(x=t * 1e3, y=e2 * 1e3, name="ε₂ (mV)", line=dict(color="#dc2626")), row=2, col=1)
        fig.add_trace(go.Scatter(x=t * 1e3, y=i2 * 1e3, name="i₂ (mA)", line=dict(color="#16a34a")), row=2, col=1)
        fig.update_xaxes(title_text="t (ms)", row=2, col=1)
        fig.update_layout(height=450)
        st.plotly_chart(fig, width="stretch")
    st.write(f"f = {fl} Hz: ε₀ = {fmt(Mloc*I0*oml,'V')}, ωL₂/R = {oml*L2l/Rl:.2f}, "
             f"i₂,₀ = {fmt(Mloc*I0*oml/abs(Zc),'A')}, atraso de i₂ em relação a ε₂ = {np.degrees(np.angle(Zc)):.1f}°")
    caixa("Observe: em baixas frequências i₂ acompanha ε₂ (resistivo). Em altas frequências, i₂ tende a um valor <b>independente de f</b> "
          "(i₂ → M i₁/L₂) e fica em oposição de fase com i₁ — a bobina pequena “expulsa” o fluxo, como uma blindagem.", "fisica")

with abas[4]:
    confira("(a) M", M, "nH", "q3a", escala=1e-9, dica_erro="Não esqueça o fator N₂ = 50.")
    confira("(b) Amplitude ε₀", eps0, "mV", "q3b", escala=1e-3)
    confira("(c) Amplitude de i₂", i20, "mA", "q3c", escala=1e-3,
            dica_erro="Use |Z| = √(R² + (ωL₂)²), não apenas R.")
    confira("(c) Atraso de fase de i₂", fase, "graus", "q3c2")
    confira("(d) Fem na espira maior", eps0, "mV", "q3d", escala=1e-3)

with abas[5]:
    quiz("1) Se R₂ dobrar (mantendo R₁ ≫ R₂), M:",
         ["dobra", "quadruplica", "cai à metade", "não muda"], 1, "M ∝ R₂² (área da espira menor).", "q3q1")
    quiz("2) Se a espira menor for girada até ficar perpendicular ao plano da maior, M:",
         ["dobra", "fica máximo", "vai a zero", "muda de sinal mas mantém o módulo"], 2,
         "O campo no centro é perpendicular ao plano da espira grande; com a pequena perpendicular, o fluxo é nulo.", "q3q2")
    quiz("3) A indutância mútua depende:",
         ["da corrente i₁", "da frequência", "apenas da geometria e do meio", "da resistência das espiras"], 2,
         "M é um coeficiente geométrico (e de μ do meio).", "q3q3")
    st.markdown("#### ⚠️ Erros comuns")
    caixa("• Esquecer N₂ no fluxo concatenado.<br>• Usar B de um fio longo em vez do campo no centro de uma espira.<br>"
          "• Usar f no lugar de ω.<br>• Calcular a corrente com i = ε/R ignorando a reatância indutiva.", "alerta")

rodape()
