import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from comum import caixa, configurar_pagina, confira, fmt, passos, quiz, rodape
from modelos import rlc_livre, rlc_serie

configurar_pagina("Q4 — Circuito RLC", "📈")
st.title("📈 Questão 4 — Circuito RLC série")

R, L, C, V0 = 20.0, 50e-3, 2.0e-6, 10.0
w0 = 1 / np.sqrt(L * C)
f0 = w0 / (2 * np.pi)
Q = w0 * L / R
df = R / L / (2 * np.pi)
I0r = V0 / R
Pr = 0.5 * I0r**2 * R
VLr = I0r * w0 * L
r400 = rlc_serie(R, L, C, V0, 400.0)
alpha = R / (2 * L)
wd = np.sqrt(w0**2 - alpha**2)
Rc = 2 * np.sqrt(L / C)

abas = st.tabs(["📝 Enunciado", "🧭 Estratégia", "✍️ Resolução", "🎛️ Laboratório", "✅ Confira", "🧠 Conceitos"])

with abas[0]:
    st.markdown(
        r"""
<div class="enunciado">

Um circuito RLC série tem $R = 20\ \Omega$, $L = 50$ mH e $C = 2{,}0\ \mu$F, alimentado por uma fonte senoidal de amplitude $V_0 = 10$ V e frequência ajustável.

**(a)** *(5 pts)* Calcule $f_0$, o fator de qualidade $Q$ e a largura de banda $\Delta f$.

**(b)** *(5 pts)* Na ressonância: amplitude da corrente, potência média e amplitude da tensão no indutor. $V_L\gg V_0$ viola a conservação de energia?

**(c)** *(6 pts)* Para $f = 400$ Hz: impedância, amplitude da corrente, ângulo de fase $\phi$ e potência média. O circuito é capacitivo ou indutivo?

**(d)** *(4 pts)* A fonte é removida com o capacitor carregado a 10 V. Classifique o regime, calcule $\omega_d$, o $R$ crítico e o tempo para a amplitude cair a $1/e$.
</div>
""",
        unsafe_allow_html=True,
    )

with abas[1]:
    with st.expander("Dica 1 — O que acontece na ressonância?"):
        st.markdown(r"$X_L = X_C$: as reatâncias se cancelam, $Z = R$ (mínimo) e a corrente é máxima, em fase com a fonte.")
    with st.expander("Dica 2 — Fator de qualidade"):
        st.markdown(r"$Q = \omega_0 L/R = \frac1R\sqrt{L/C}$. Ele mede quão “afiada” é a ressonância e quanto a tensão no L (ou no C) é amplificada: $V_L = Q V_0$.")
    with st.expander("Dica 3 — Sinal do ângulo de fase"):
        st.markdown(r"$\tan\phi = (X_L-X_C)/R$. Se $X_C > X_L$, $\phi<0$: a corrente está **adiantada** em relação à tensão ⇒ comportamento capacitivo.")
    with st.expander("Dica 4 — RLC livre"):
        st.markdown(r"$L\ddot q + R\dot q + q/C = 0$. Compare $\alpha = R/2L$ com $\omega_0$: $\alpha<\omega_0$ ⇒ oscila (subamortecido).")

with abas[2]:
    st.markdown("#### Item (a)")

    def a1():
        st.latex(r"\omega_0 = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{(0{,}050)(2{,}0\times10^{-6})}} = \frac{1}{\sqrt{10^{-7}}}\approx 3162\ \text{rad/s}")
        st.latex(r"f_0 = \frac{\omega_0}{2\pi}\approx " + f"{f0:.1f}".replace('.', '{,}') + r"\ \text{Hz}")

    def a2():
        st.latex(r"Q = \frac{\omega_0 L}{R} = \frac{(3162)(0{,}050)}{20}\approx " + f"{Q:.2f}".replace('.', '{,}'))
        st.latex(r"\Delta\omega = \frac{R}{L} = 400\ \text{rad/s}\ \Rightarrow\ \Delta f = \frac{\Delta\omega}{2\pi} \approx "
                 + f"{df:.1f}".replace('.', '{,}') + r"\ \text{Hz}\quad\left(=\frac{f_0}{Q}\right)")

    passos([("Frequência de ressonância", a1), ("Q e largura de banda", a2)])

    st.markdown("#### Item (b)")

    def b1():
        st.latex(r"Z = R\ \Rightarrow\ I_0 = \frac{V_0}{R} = \frac{10}{20} = 0{,}50\ \text{A}")
        st.latex(r"P_{\text{méd}} = \tfrac12 I_0^2R = \tfrac12(0{,}50)^2(20) = 2{,}5\ \text{W}")

    def b2():
        st.latex(r"V_{L,0} = I_0\,\omega_0 L = (0{,}50)(158{,}1) \approx " + f"{VLr:.1f}".replace('.', '{,}') + r"\ \text{V} = Q\,V_0")
        caixa("<b>Não viola</b> a conservação de energia. Tensão não é energia! A energia oscila entre o campo magnético do indutor e o "
              "campo elétrico do capacitor; v_L e v_C são iguais em módulo e <b>opostas em fase</b> (somam zero a cada instante). "
              "A fonte só repõe o que R dissipa (2,5 W). É como empurrar um balanço no ritmo certo: pequenos empurrões, grande amplitude.", "fisica")

    passos([("Corrente e potência", b1), ("Tensão no indutor", b2)])

    st.markdown("#### Item (c) — f = 400 Hz")

    def c1():
        st.latex(r"\omega = 2\pi(400)\approx 2513\ \text{rad/s}")
        st.latex(r"X_L = \omega L \approx " + f"{r400['XL']:.1f}".replace('.', '{,}') + r"\ \Omega,\qquad X_C = \frac{1}{\omega C}\approx "
                 + f"{r400['XC']:.1f}".replace('.', '{,}') + r"\ \Omega")

    def c2():
        st.latex(r"Z = \sqrt{20^2 + (125{,}7-198{,}9)^2}\approx " + f"{r400['Z']:.1f}".replace('.', '{,}') + r"\ \Omega,\qquad I_0 = \frac{V_0}{Z}\approx "
                 + f"{r400['I0']*1e3:.0f}" + r"\ \text{mA}")

    def c3():
        st.latex(r"\tan\phi = \frac{X_L-X_C}{R} \approx -3{,}66\ \Rightarrow\ \phi\approx " + f"{np.degrees(r400['phi']):.1f}".replace('.', '{,}') + r"^\circ")
        st.latex(r"P_{\text{méd}} = \tfrac12 I_0^2 R \approx " + f"{r400['P']:.3f}".replace('.', '{,}') + r"\ \text{W}"
                 r"\quad\left(=\tfrac12 V_0 I_0\cos\phi\right)")
        caixa("Abaixo da ressonância X_C > X_L ⇒ o circuito é <b>capacitivo</b>: a corrente está <b>adiantada</b> ≈ 75° em relação à tensão. "
              "A potência cai para ~7% do valor na ressonância porque f está fora da banda (f₀ ± Δf/2 ≈ 471–535 Hz).", "fisica")

    passos([("Reatâncias", c1), ("Impedância e corrente", c2), ("Fase e potência", c3)])

    st.markdown("#### Item (d) — Oscilações livres")

    def d1():
        st.latex(r"\alpha = \frac{R}{2L} = \frac{20}{0{,}10} = 200\ \text{s}^{-1}\ \ll\ \omega_0 = 3162\ \text{s}^{-1}\ \Rightarrow\ \textbf{subamortecido}")
        st.latex(r"q(t) = q_0 e^{-\alpha t}\left[\cos\omega_d t + \frac{\alpha}{\omega_d}\sin\omega_d t\right],\quad q_0 = CV = 20\ \mu\text{C}")

    def d2():
        st.latex(r"\omega_d = \sqrt{\omega_0^2-\alpha^2} \approx " + f"{wd:.0f}" + r"\ \text{rad/s}\ (\text{quase igual a }\omega_0)")
        st.latex(r"R_c = 2\sqrt{L/C} = 2\sqrt{25\,000}\approx " + f"{Rc:.0f}" + r"\ \Omega")
        st.latex(r"\tau = 1/\alpha = 5{,}0\ \text{ms}\quad(\approx " + f"{wd/(2*np.pi)*5e-3:.1f}".replace('.', '{,}') + r"\ \text{oscilações})")

    passos([("Classificação do regime", d1), ("ω_d, R crítico e tempo de decaimento", d2)])

with abas[3]:
    st.markdown("### 1. Curva de ressonância e diagrama de fasores")
    c1, c2 = st.columns([1, 3])
    with c1:
        Rl = st.slider("R (Ω)", 1.0, 200.0, 20.0, 1.0)
        Ll = st.slider("L (mH)", 5.0, 200.0, 50.0, 5.0) * 1e-3
        Cl = st.slider("C (μF)", 0.2, 20.0, 2.0, 0.2) * 1e-6
        f0l = 1 / (2 * np.pi * np.sqrt(Ll * Cl))
        fl = st.slider("Frequência da fonte f (Hz)", 20.0, 2000.0, 400.0, 5.0)
    with c2:
        ff = np.linspace(20, 2000, 1500)
        r = rlc_serie(Rl, Ll, Cl, V0, ff)
        rp = rlc_serie(Rl, Ll, Cl, V0, fl)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Amplitude da corrente e potência", "Fase φ (tensão − corrente)"))
        fig.add_trace(go.Scatter(x=ff, y=r["I0"] * 1e3, name="I₀ (mA)", line=dict(color="#2563eb", width=3)), row=1, col=1)
        Pmax = 0.5 * (V0 / Rl) ** 2 * Rl
        fig.add_trace(go.Scatter(x=ff, y=r["P"] / Pmax * (V0 / Rl) * 1e3, name="P (escala relativa)",
                                 line=dict(color="#ea580c", dash="dot")), row=1, col=1)
        fig.add_vrect(x0=f0l - Rl / Ll / (4 * np.pi), x1=f0l + Rl / Ll / (4 * np.pi), fillcolor="#16a34a", opacity=0.15,
                      line_width=0, row=1, col=1)
        fig.add_vline(x=fl, line_dash="dash", line_color="#dc2626", row=1, col=1)
        fig.add_trace(go.Scatter(x=ff, y=np.degrees(r["phi"]), name="φ (graus)", line=dict(color="#7c3aed", width=3)), row=1, col=2)
        fig.add_vline(x=fl, line_dash="dash", line_color="#dc2626", row=1, col=2)
        fig.add_hline(y=0, line_color="gray", row=1, col=2)
        fig.update_xaxes(title_text="f (Hz)")
        fig.update_layout(height=380, legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, width="stretch")
    m = st.columns(5)
    m[0].metric("f₀", f"{f0l:.1f} Hz")
    m[1].metric("Q", f"{2*np.pi*f0l*Ll/Rl:.2f}")
    m[2].metric("Z", f"{rp['Z']:.1f} Ω")
    m[3].metric("I₀", fmt(rp["I0"], "A"))
    m[4].metric("φ", f"{np.degrees(rp['phi']):.1f}°", "indutivo" if rp["phi"] > 0.01 else ("capacitivo" if rp["phi"] < -0.01 else "ressonância"))
    st.caption("Faixa verde = banda de meia potência (Δf = R/2πL). Linha vermelha = frequência escolhida.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Fasores de tensão** (corrente como referência horizontal)")
        I0p = rp["I0"]
        VR, VLp, VC = I0p * Rl, I0p * rp["XL"], I0p * rp["XC"]
        fig = go.Figure()

        def seta(x0, y0, x1, y1, cor, nome):
            fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowwidth=3, arrowcolor=cor)
            fig.add_trace(go.Scatter(x=[x1], y=[y1], mode="text", text=[nome], textposition="top right",
                                     showlegend=False, textfont=dict(color=cor, size=14)))

        seta(0, 0, VR, 0, "#2563eb", "V_R")
        seta(0, 0, 0, VLp, "#16a34a", "V_L")
        seta(0, 0, 0, -VC, "#ea580c", "V_C")
        seta(0, 0, VR, VLp - VC, "#dc2626", "V₀ (fonte)")
        lim = max(VR, VLp, VC, V0) * 1.2
        fig.update_layout(height=400, xaxis=dict(range=[-lim * 0.3, lim], zeroline=True, title="V"),
                          yaxis=dict(range=[-lim, lim], scaleanchor="x", zeroline=True), showlegend=False)
        st.plotly_chart(fig, width="stretch")
    with c2:
        st.markdown("**Sinais no tempo**")
        t = np.linspace(0, 3 / fl, 600)
        om_l = 2 * np.pi * fl
        v = V0 * np.cos(om_l * t)
        i = rp["I0"] * np.cos(om_l * t - rp["phi"])
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=t * 1e3, y=v, name="v(t) fonte (V)", line=dict(color="#dc2626")))
        fig.add_trace(go.Scatter(x=t * 1e3, y=i * 1e3, name="i(t) (mA)", line=dict(color="#2563eb")), secondary_y=True)
        fig.add_trace(go.Scatter(x=t * 1e3, y=v * i, name="p(t)=v·i (W)", line=dict(color="#16a34a", dash="dot")))
        fig.update_xaxes(title_text="t (ms)")
        fig.update_layout(height=400, legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig, width="stretch")
    caixa("Mova f através de f₀ e observe: (1) os fasores V_L e V_C trocam de tamanho; (2) na ressonância eles se cancelam e "
          "V₀ fica alinhado com V_R; (3) fora da ressonância a potência instantânea p(t) fica negativa em parte do ciclo — "
          "energia voltando para a fonte. Aumente R e veja a ressonância “alargar”.", "dica")

    st.markdown("### 2. Oscilações livres: do subamortecido ao superamortecido")
    c1, c2 = st.columns([1, 3])
    with c1:
        Rf = st.slider("R (Ω) — circuito livre", 0.0, 800.0, 20.0, 5.0, key="Rf")
        st.write(f"R crítico = {Rc:.0f} Ω")
        energia = st.checkbox("Mostrar energias U_C e U_L", False)
    with c2:
        t = np.linspace(0, 0.02, 2000)
        q0 = C * V0
        q, regime = rlc_livre(Rf, L, C, q0, t)
        fig = go.Figure()
        if energia:
            dq = np.gradient(q, t)
            fig.add_trace(go.Scatter(x=t * 1e3, y=q**2 / (2 * C) * 1e6, name="U_C (μJ)", line=dict(color="#ea580c")))
            fig.add_trace(go.Scatter(x=t * 1e3, y=0.5 * L * dq**2 * 1e6, name="U_L (μJ)", line=dict(color="#16a34a")))
            fig.add_trace(go.Scatter(x=t * 1e3, y=(q**2 / (2 * C) + 0.5 * L * dq**2) * 1e6, name="total (μJ)",
                                     line=dict(color="black", width=3)))
            fig.update_yaxes(title_text="energia (μJ)")
        else:
            fig.add_trace(go.Scatter(x=t * 1e3, y=q * 1e6, name="q(t) (μC)", line=dict(color="#2563eb", width=2)))
            if Rf > 0:
                a_ = Rf / (2 * L)
                fig.add_trace(go.Scatter(x=t * 1e3, y=q0 * np.exp(-a_ * t) * 1e6, name="envoltória q₀e^(−αt)",
                                         line=dict(color="gray", dash="dash")))
            fig.update_yaxes(title_text="q (μC)")
        fig.update_layout(height=380, xaxis_title="t (ms)", title=f"Regime: {regime}")
        st.plotly_chart(fig, width="stretch")

with abas[4]:
    confira("(a) f₀", f0, "Hz", "q4a1")
    confira("(a) Q", Q, "adimensional", "q4a2")
    confira("(a) Δf", df, "Hz", "q4a3", dica_erro="Δω = R/L é em rad/s; divida por 2π.")
    confira("(b) I₀ na ressonância", I0r, "A", "q4b1")
    confira("(b) Potência média", Pr, "W", "q4b2")
    confira("(b) V_L na ressonância", VLr, "V", "q4b3")
    confira("(c) Z em 400 Hz", r400["Z"], "Ω", "q4c1")
    confira("(c) I₀ em 400 Hz", r400["I0"], "mA", "q4c2", escala=1e-3)
    confira("(c) φ em 400 Hz", np.degrees(r400["phi"]), "graus", "q4c3")
    confira("(c) Potência média em 400 Hz", r400["P"], "W", "q4c4")
    confira("(d) ω_d", wd, "rad/s", "q4d1")
    confira("(d) R crítico", Rc, "Ω", "q4d2")
    confira("(d) Tempo para cair a 1/e", 1 / alpha, "ms", "q4d3", escala=1e-3)

with abas[5]:
    quiz("1) Dobrando R (mantendo L e C), a largura de banda:", ["cai à metade", "não muda", "dobra", "quadruplica"], 2, "Δω = R/L.", "q4q1")
    quiz("2) Na ressonância, a tensão no capacitor é:", ["zero", "V₀", "Q·V₀, em oposição de fase a V_L", "igual a V_R"], 2,
         "V_C = V_L = QV₀, defasadas de 180° entre si.", "q4q2")
    quiz("3) Acima da ressonância, o circuito se comporta como:", ["resistivo", "indutivo (corrente atrasada)", "capacitivo (corrente adiantada)", "curto-circuito"], 1,
         "Para ω > ω₀, X_L > X_C ⇒ φ > 0.", "q4q3")
    st.markdown("#### ⚠️ Erros comuns")
    caixa("• Somar V_R + V_L + V_C como números (elas estão defasadas — some fasores!).<br>"
          "• Confundir f₀ com ω₀ (fator 2π).<br>• Usar P = V₀I₀ esquecendo o ½ e o cos φ.<br>"
          "• Achar que φ < 0 é impossível ou “erro de sinal”: é simplesmente o caso capacitivo.", "alerta")

rodape()
