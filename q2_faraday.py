import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from comum import caixa, configurar_pagina, confira, fmt, passos, quiz, rodape
from modelos import MU0, fem_espira_afastando, fem_mov_lados, fluxo_fio_espira

configurar_pagina("Q2 — Lei de Faraday", "⚡")
st.title("⚡ Questão 2 — Lei de Faraday")

I, ell, w, x, v, R = 20.0, 0.20, 0.10, 0.05, 2.0, 0.010
I0, f = 20.0, 60.0
om = 2 * np.pi * f
Phi = fluxo_fio_espira(I, ell, w, x)
eps = fem_espira_afastando(I, ell, w, x, v)
i_ind = eps / R
e1, e2 = fem_mov_lados(I, ell, w, x, v)
eps0_ac = MU0 * ell / (2 * np.pi) * np.log((x + w) / x) * I0 * om

abas = st.tabs(["📝 Enunciado", "🧭 Estratégia", "✍️ Resolução", "🎛️ Laboratório", "✅ Confira", "🧠 Conceitos"])

with abas[0]:
    with st.container(border=True):
        st.markdown(
            r"""

Um fio retilíneo muito longo conduz $I = 20$ A. Uma espira retangular, coplanar ao fio, tem lados $\ell = 20$ cm (paralelo ao fio)
e $w = 10$ cm (perpendicular), e resistência $R = 0{,}010\ \Omega$. O lado mais próximo do fio está à distância $x$.

**(a)** *(5 pts)* Mostre que $\Phi_B(x) = \dfrac{\mu_0 I\ell}{2\pi}\ln\!\left(\dfrac{x+w}{x}\right)$.

**(b)** *(6 pts)* A espira se afasta do fio com $v = 2{,}0$ m/s. Determine a fem e a corrente induzidas quando $x = 5{,}0$ cm e o sentido da corrente (Lenz).

**(c)** *(4 pts)* Confirme (b) pela fem de movimento $\oint(\vec v\times\vec B)\cdot d\vec\ell$. Por que os lados perpendiculares ao fio não contribuem?

**(d)** *(5 pts)* Agora a espira está **parada** em $x = 5{,}0$ cm e $I(t) = I_0\sin\omega t$, com $I_0 = 20$ A e $f = 60$ Hz. Obtenha $\varepsilon(t)$, sua amplitude e a defasagem em relação a $I(t)$.
"""
        )
    st.caption("Na figura da prova: corrente para cima, espira à direita do fio ⇒ B entrando no plano (⊗) na região da espira.")

with abas[1]:
    with st.expander("Dica 1 — O campo não é uniforme sobre a espira"):
        st.markdown(r"$B = \mu_0 I/(2\pi r)$ depende da distância $r$ ao fio. Divida a espira em **faixas** de largura $dr$ paralelas ao fio: "
                    r"em cada faixa $B$ é constante e $dA = \ell\,dr$.")
    with st.expander("Dica 2 — Derivada de um fluxo que depende de x(t)"):
        st.markdown(r"Use a regra da cadeia: $\dfrac{d\Phi}{dt} = \dfrac{d\Phi}{dx}\dfrac{dx}{dt} = \dfrac{d\Phi}{dx}\,v$.")
    with st.expander("Dica 3 — Lenz"):
        st.markdown("Pergunte: o fluxo está **aumentando ou diminuindo**? A corrente induzida cria um campo que tenta **repor** o que está mudando.")
    with st.expander("Dica 4 — Fem de movimento"):
        st.markdown(r"Em cada lado paralelo ao fio, $|\vec v\times\vec B| = vB$ e aponta ao longo do lado. Os dois lados paralelos “empurram” cargas em sentidos opostos no circuito: a fem líquida é a **diferença**.")

with abas[2]:
    st.markdown("#### Item (a) — Fluxo")

    def a1():
        st.markdown(r"Tomamos uma faixa entre $r$ e $r+dr$ (paralela ao fio). Nela $B$ é praticamente constante e perpendicular ao plano:")
        st.latex(r"d\Phi_B = B(r)\,dA = \frac{\mu_0 I}{2\pi r}\,\ell\,dr")

    def a2():
        st.latex(r"\Phi_B = \frac{\mu_0 I\ell}{2\pi}\int_x^{x+w}\frac{dr}{r} = \boxed{\frac{\mu_0 I\ell}{2\pi}\ln\frac{x+w}{x}}")
        st.markdown(f"Para x = 5 cm: Φ = (2×10⁻⁷)(20)(0,20) ln 3 ≈ **{fmt(Phi,'Wb')}**")

    passos([("Elemento de área", a1), ("Integração", a2)])

    st.markdown("#### Item (b) — Espira se afastando")

    def b1():
        st.latex(r"\varepsilon = -\frac{d\Phi_B}{dt} = -\frac{\mu_0 I\ell}{2\pi}\frac{d}{dt}\left[\ln(x+w)-\ln x\right]"
                 r"= -\frac{\mu_0 I\ell}{2\pi}\left(\frac{1}{x+w}-\frac{1}{x}\right)\frac{dx}{dt}")
        st.latex(r"\Rightarrow\ |\varepsilon| = \frac{\mu_0 I\ell\,w\,v}{2\pi\,x(x+w)}")

    def b2():
        st.latex(r"|\varepsilon| = \frac{(2\times10^{-7})(20)(0{,}20)(0{,}10)(2{,}0)}{(0{,}05)(0{,}15)}")
        st.markdown(f"**ε ≈ {fmt(eps,'V')}**  e  **i = ε/R ≈ {fmt(i_ind,'A')}**")

    def b3():
        caixa("<b>Lenz:</b> ao se afastar, a espira atravessa regiões de campo mais fraco ⇒ o fluxo <b>entrando</b> (⊗) "
              "<b>diminui</b>. A corrente induzida tenta repor esse fluxo, criando B entrando no interior da espira ⇒ "
              "sentido <b>horário</b> (na figura da prova).", "fisica")
        st.markdown("Conferência com forças: no lado próximo (corrente para baixo, antiparalela à do fio) a força é de **repulsão**; "
                    "no lado distante (corrente para cima) é de **atração**, porém mais fraca. Resultado: força líquida puxando a espira "
                    "**de volta** ao fio — ela se opõe ao movimento, como Lenz exige.")

    passos([("Derivando o fluxo", b1), ("Substituindo os valores", b2), ("Sentido da corrente", b3)])

    st.markdown("#### Item (c) — Fem de movimento")

    def c1():
        st.markdown(r"Com $\vec v = v\,\hat x$ (afastando do fio) e $\vec B = -B\,\hat z$ (entrando), temos "
                    r"$\vec v\times\vec B = vB\,\hat y$: a força sobre as cargas é **paralela ao fio**. "
                    r"Nos lados perpendiculares ao fio, $d\vec\ell$ está ao longo de $\hat x$ ⇒ $(\vec v\times\vec B)\cdot d\vec\ell = 0$: "
                    r"esses lados apenas “conduzem”, não geram fem.")

    def c2():
        st.latex(r"\varepsilon = B(x)\,\ell\,v - B(x+w)\,\ell\,v = \frac{\mu_0 I\ell v}{2\pi}\left(\frac1x - \frac{1}{x+w}\right)"
                 r"= \frac{\mu_0 I\ell\,w\,v}{2\pi\,x(x+w)}\ \checkmark")
        st.markdown(f"Lado próximo: {fmt(e1,'V')}; lado distante: {fmt(e2,'V')}; diferença: **{fmt(e1-e2,'V')}** — igual ao item (b).")
        caixa("Duas leituras do mesmo fenômeno: para um observador no laboratório, a fem vem da força magnética sobre cargas que se movem "
              "com a espira; pela lei de Faraday, vem da variação do fluxo. A lei do fluxo engloba as duas.", "fisica")

    passos([("Lados perpendiculares", c1), ("Lados paralelos", c2)])

    st.markdown("#### Item (d) — Corrente alternada, espira parada")

    def d1():
        st.latex(r"\Phi_B(t) = \frac{\mu_0\ell}{2\pi}\ln\!\left(\frac{x+w}{x}\right) I_0\sin\omega t \;\Rightarrow\;"
                 r"\varepsilon(t) = -\frac{\mu_0\ell}{2\pi}\ln 3\; I_0\,\omega\cos\omega t")

    def d2():
        st.latex(r"\varepsilon_0 = (2\times10^{-7})(0{,}20)(\ln 3)(20)(2\pi\cdot 60)")
        st.markdown(f"**ε₀ ≈ {fmt(eps0_ac,'V')}**")
        st.markdown(r"Como $-\cos\omega t = \sin(\omega t - 90^\circ)$, a fem está **atrasada de 90°** em relação à corrente do fio: "
                    r"ela é máxima quando $I$ passa por zero (é aí que $I$ varia mais rápido) e nula nos picos de $I$.")

    passos([("Fluxo dependente do tempo", d1), ("Amplitude e fase", d2)])

with abas[3]:
    st.markdown("### Simulador: espira próxima a um fio")
    c1, c2 = st.columns([1, 3])
    with c1:
        I_l = st.slider("Corrente no fio I (A)", 1.0, 50.0, 20.0)
        ell_l = st.slider("ℓ (cm)", 5.0, 40.0, 20.0) / 100
        w_l = st.slider("w (cm)", 2.0, 30.0, 10.0) / 100
        v_l = st.slider("v (m/s)", -5.0, 5.0, 2.0, 0.5, help="positivo = afastando do fio")
        x_l = st.slider("Posição x (cm)", 1.0, 40.0, 5.0, 0.5) / 100
    with c2:
        xs = np.linspace(0.005, 0.5, 400)
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Mapa de B (μT) e a espira", "Fluxo e fem em função de x"),
                            specs=[[{}, {"secondary_y": True}]])
        gx = np.linspace(0.005, 0.5, 120)
        gy = np.linspace(-0.25, 0.25, 60)
        GX, GY = np.meshgrid(gx, gy)
        Bmap = MU0 * I_l / (2 * np.pi * GX) * 1e6
        fig.add_trace(go.Heatmap(x=gx * 100, y=gy * 100, z=np.log10(Bmap), colorscale="Blues", showscale=False,
                                 hovertemplate="r=%{x:.1f} cm<extra></extra>"), row=1, col=1)
        fig.add_trace(go.Scatter(x=[0, 0], y=[-25, 25], mode="lines", line=dict(color="black", width=5), name="fio"), row=1, col=1)
        xr = np.array([x_l, x_l + w_l, x_l + w_l, x_l, x_l]) * 100
        yr = np.array([-ell_l / 2, -ell_l / 2, ell_l / 2, ell_l / 2, -ell_l / 2]) * 100
        fig.add_trace(go.Scatter(x=xr, y=yr, mode="lines", line=dict(color="#dc2626", width=4), name="espira"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs * 100, y=fluxo_fio_espira(I_l, ell_l, w_l, xs) * 1e6, name="Φ (μWb)",
                                 line=dict(color="#2563eb")), row=1, col=2)
        fig.add_trace(go.Scatter(x=xs * 100, y=fem_espira_afastando(I_l, ell_l, w_l, xs, v_l) * 1e6, name="ε (μV)",
                                 line=dict(color="#dc2626")), row=1, col=2, secondary_y=True)
        fig.add_vline(x=x_l * 100, line_dash="dot", row=1, col=2)
        fig.update_xaxes(title_text="x (cm)", row=1, col=1)
        fig.update_xaxes(title_text="x (cm)", row=1, col=2)
        fig.update_yaxes(title_text="Φ (μWb)", row=1, col=2)
        fig.update_yaxes(title_text="ε (μV)", row=1, col=2, secondary_y=True)
        fig.update_layout(height=430, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, width="stretch")
    e_now = fem_espira_afastando(I_l, ell_l, w_l, x_l, v_l)
    sentido = "horário" if v_l > 0 else ("anti-horário" if v_l < 0 else "— (sem corrente)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Fluxo Φ", fmt(fluxo_fio_espira(I_l, ell_l, w_l, x_l), "Wb"))
    m2.metric("Fem |ε|", fmt(abs(e_now), "V"))
    m3.metric("Sentido da corrente induzida", sentido)
    caixa("Experimente: (1) aproxime a espira do fio (x pequeno) — a fem cresce muito, porque B varia rapidamente perto do fio. "
          "(2) Inverta v — o sentido da corrente inverte. (3) Faça w muito pequeno: ε ≈ ℓ v w · |dB/dr| — a fem mede o "
          "<b>gradiente</b> do campo, não o campo!", "dica")

    st.markdown("### Item (d): corrente alternada no fio")
    fL = st.slider("Frequência f (Hz)", 10, 1000, 60, 10)
    t = np.linspace(0, 2 / fL, 500)
    om_l = 2 * np.pi * fL
    Iw = I0 * np.sin(om_l * t)
    ew = -MU0 * ell / (2 * np.pi) * np.log(3) * I0 * om_l * np.cos(om_l * t)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=t * 1e3, y=Iw, name="I(t) no fio (A)", line=dict(color="#2563eb")))
    fig.add_trace(go.Scatter(x=t * 1e3, y=ew * 1e3, name="ε(t) na espira (mV)", line=dict(color="#dc2626")), secondary_y=True)
    fig.update_xaxes(title_text="t (ms)")
    fig.update_yaxes(title_text="I (A)")
    fig.update_yaxes(title_text="ε (mV)", secondary_y=True)
    fig.update_layout(height=340)
    st.plotly_chart(fig, width="stretch")
    st.write(f"Amplitude da fem: **{fmt(MU0*ell/(2*np.pi)*np.log(3)*I0*om_l,'V')}** — proporcional a f. "
             "É por isso que transformadores e sensores indutivos funcionam melhor em frequências mais altas.")

with abas[4]:
    confira("(a) Fluxo em x = 5 cm", Phi, "μWb", "q2a", escala=1e-6)
    confira("(b) Fem induzida", eps, "μV", "q2b", escala=1e-6,
            dica_erro="Use ε = μ₀Iℓwv / [2π x (x+w)], com tudo em metros.")
    confira("(b) Corrente induzida", i_ind, "mA", "q2b2", escala=1e-3)
    confira("(d) Amplitude da fem com CA", eps0_ac, "mV", "q2d", escala=1e-3)
    quiz("(b) Sentido da corrente induzida (figura da prova):", ["horário", "anti-horário"], 0,
         "O fluxo ⊗ diminui; a corrente induzida reforça o ⊗ no interior ⇒ horário.", "q2sent")

with abas[5]:
    quiz("1) Se a espira se mover paralelamente ao fio (para cima), a fem induzida será:",
         ["máxima", "nula", "igual à do item (b)", "dependerá de ℓ"], 1,
         "O fluxo não muda (B só depende da distância ao fio). Na fem de movimento, os dois lados paralelos ao fio têm v ∥ dℓ ⇒ (v×B)·dℓ = 0 e os lados perpendiculares se cancelam.", "q2q1")
    quiz("2) No item (d), dobrar a frequência faz a amplitude da fem:",
         ["cair à metade", "não mudar", "dobrar", "quadruplicar"], 2, "ε₀ ∝ ω I₀.", "q2q2")
    quiz("3) O sinal negativo na lei de Faraday expressa:",
         ["que a fem é sempre negativa", "a lei de Lenz (oposição à variação do fluxo)", "uma convenção sem significado físico",
          "a conservação de carga"], 1, "É a conservação de energia disfarçada: se a fem reforçasse a variação, teríamos um moto-perpétuo.", "q2q3")
    st.markdown("#### ⚠️ Erros comuns")
    caixa("• Usar Φ = B·A com B avaliado num único ponto (o campo não é uniforme!).<br>"
          "• Errar os limites da integral (de 0 a w em vez de x a x+w).<br>"
          "• No item (d), usar f em vez de ω = 2πf.<br>"
          "• Achar que o sentido da corrente é o que “acompanha” o fluxo, em vez de se opor à <i>variação</i>.", "alerta")

rodape()
