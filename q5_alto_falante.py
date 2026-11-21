import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from comum import caixa, configurar_pagina, confira, fmt, passos, quiz, rodape
from modelos import falante_resposta, falante_Z

configurar_pagina("Q5 — Alto-falante", "🔊")
st.title("🔊 Questão 5 — Como funciona um alto-falante (ou fone de ouvido)?")

Bl, Re, Le, m, k, b = 7.0, 6.0, 0.50e-3, 0.020, 2.0e3, 1.5
v_teste = 0.50
Ceq, Leq, Req = m / Bl**2, Bl**2 / k, Bl**2 / b
fs = np.sqrt(k / m) / (2 * np.pi)
Zfs = abs(falante_Z(fs, Bl, Re, Le, m, k, b))

SVG_FALANTE = """
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width:520px;width:100%">
  <defs><marker id="seta" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <path d="M0,0 L0,6 L9,3 z" fill="#2563eb"/></marker></defs>
  <!-- placa e carcaça do ímã -->
  <rect x="150" y="200" width="220" height="30" fill="#6b7280"/>
  <rect x="150" y="110" width="40" height="120" fill="#6b7280"/>
  <rect x="330" y="110" width="40" height="120" fill="#6b7280"/>
  <rect x="225" y="120" width="70" height="80" fill="#9ca3af"/>
  <text x="260" y="165" font-size="16" text-anchor="middle" fill="white">N</text>
  <text x="170" y="135" font-size="14" text-anchor="middle" fill="white">S</text>
  <text x="350" y="135" font-size="14" text-anchor="middle" fill="white">S</text>
  <!-- bobina -->
  <g fill="#dc2626">
    <circle cx="210" cy="140" r="4"/><circle cx="210" cy="152" r="4"/><circle cx="210" cy="164" r="4"/><circle cx="210" cy="176" r="4"/>
    <circle cx="310" cy="140" r="4"/><circle cx="310" cy="152" r="4"/><circle cx="310" cy="164" r="4"/><circle cx="310" cy="176" r="4"/>
  </g>
  <line x1="210" y1="100" x2="210" y2="185" stroke="#dc2626" stroke-width="1" stroke-dasharray="3"/>
  <line x1="310" y1="100" x2="310" y2="185" stroke="#dc2626" stroke-width="1" stroke-dasharray="3"/>
  <!-- campo radial -->
  <line x1="222" y1="190" x2="196" y2="190" stroke="#2563eb" stroke-width="2" marker-end="url(#seta)"/>
  <line x1="298" y1="190" x2="324" y2="190" stroke="#2563eb" stroke-width="2" marker-end="url(#seta)"/>
  <text x="260" y="250" font-size="13" text-anchor="middle" fill="#2563eb">B radial no entreferro</text>
  <!-- cone -->
  <path d="M210,100 L90,20 M310,100 L430,20" stroke="black" stroke-width="3" fill="none"/>
  <path d="M210,100 L310,100" stroke="black" stroke-width="2"/>
  <path d="M80,20 q-12,-10 0,-14 M440,20 q12,-10 0,-14" stroke="#16a34a" stroke-width="3" fill="none"/>
  <text x="440" y="45" font-size="13" fill="black">cone</text>
  <text x="440" y="10" font-size="12" fill="#16a34a">suspensão (k, b)</text>
  <text x="335" y="95" font-size="13" fill="#dc2626">bobina móvel</text>
  <!-- seta de movimento -->
  <line x1="260" y1="95" x2="260" y2="45" stroke="black" stroke-width="2" marker-end="url(#seta)"/>
  <text x="268" y="60" font-size="14">x(t)</text>
  <path d="M30,80 q10,-10 0,-20 M45,85 q14,-15 0,-30 M60,90 q18,-20 0,-40" stroke="#7c3aed" stroke-width="2" fill="none"/>
  <text x="5" y="115" font-size="12" fill="#7c3aed">ondas sonoras</text>
</svg>
"""

SVG_CIRCUITO = """
<svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg" style="max-width:560px;width:100%;font-family:sans-serif">
  <g stroke="black" stroke-width="2" fill="none">
    <line x1="20" y1="40" x2="60" y2="40"/>
    <polyline points="60,40 68,30 76,50 84,30 92,50 100,30 108,50 116,40"/>
    <line x1="116" y1="40" x2="150" y2="40"/>
    <path d="M150,40 a10,10 0 0 1 20,0 a10,10 0 0 1 20,0 a10,10 0 0 1 20,0 a10,10 0 0 1 20,0"/>
    <line x1="230" y1="40" x2="300" y2="40"/>
    <line x1="300" y1="40" x2="500" y2="40"/>
    <line x1="300" y1="160" x2="500" y2="160"/>
    <line x1="20" y1="160" x2="300" y2="160"/>
    <!-- C -->
    <line x1="320" y1="40" x2="320" y2="92"/><line x1="305" y1="92" x2="335" y2="92"/>
    <line x1="305" y1="104" x2="335" y2="104"/><line x1="320" y1="104" x2="320" y2="160"/>
    <!-- L -->
    <line x1="410" y1="40" x2="410" y2="65"/>
    <path d="M410,65 a10,10 0 0 1 0,20 a10,10 0 0 1 0,20 a10,10 0 0 1 0,20"/>
    <line x1="410" y1="125" x2="410" y2="160"/>
    <!-- R -->
    <line x1="490" y1="40" x2="490" y2="65"/>
    <polyline points="490,65 480,72 500,80 480,88 500,96 480,104 500,112 490,120"/>
    <line x1="490" y1="120" x2="490" y2="160"/>
  </g>
  <circle cx="20" cy="40" r="4"/><circle cx="20" cy="160" r="4"/>
  <text x="5" y="105" font-size="14">V</text>
  <text x="75" y="25" font-size="13">Rₑ</text><text x="180" y="25" font-size="13">Lₑ</text>
  <text x="340" y="90" font-size="13">C_eq = m/(Bℓ)²</text>
  <text x="420" y="140" font-size="13">L_eq</text>
  <text x="505" y="100" font-size="13">R_eq</text>
  <text x="310" y="190" font-size="12" fill="#7c3aed">“parte mecânica” vista pelo amplificador (RLC paralelo)</text>
</svg>
"""

abas = st.tabs(["📝 Enunciado", "🧭 Estratégia", "✍️ Resolução", "🎛️ Laboratório", "✅ Confira", "🧠 Conceitos"])

with abas[0]:
    c1, c2 = st.columns([3, 2])
    with c1:
        with st.container(border=True):
            st.markdown(
                r"""

Num alto-falante dinâmico, uma bobina móvel presa ao cone fica no entreferro de um ímã permanente, onde o campo é **radial**.
Dados: $B\ell = 7{,}0$ T·m, $R_e = 6{,}0\ \Omega$, $L_e = 0{,}50$ mH, $m = 20$ g, $k = 2{,}0\times10^3$ N/m, $b = 1{,}5$ N·s/m.

**(a)** *(4 pts)* Explique como um sinal elétrico de áudio se transforma em som. Por que o campo no entreferro é radial?

**(b)** *(4 pts)* Mostre que, quando o cone se move com velocidade $v$, surge na bobina a fem $\varepsilon = B\ell v$. Calcule-a para $v = 0{,}50$ m/s. Ela auxilia ou se opõe à corrente?

**(c)** *(6 pts)* A partir de $m\ddot x + b\dot x + kx = B\ell\,i$ e $V = R_ei + L_e\frac{di}{dt} + B\ell\dot x$, mostre que a parte mecânica equivale a um
**RLC paralelo** com $C_{eq} = m/(B\ell)^2$, $L_{eq} = (B\ell)^2/k$, $R_{eq} = (B\ell)^2/b$. Calcule-os.

**(d)** *(4 pts)* Calcule $f_s$ e $|Z|$ nessa frequência. Por que $|Z(f)|$ tem um **pico** (e não um vale) em $f_s$?

**(e)** *(2 pts)* Por que um fone de ouvido dinâmico, ligado à entrada de microfone, funciona como microfone?
"""
            )
    with c2:
        st.markdown(SVG_FALANTE, unsafe_allow_html=True)
        st.caption("Corte de um alto-falante dinâmico: o ímã cria um campo radial; a bobina presa ao cone se move axialmente.")

with abas[1]:
    with st.expander("Dica 1 — Qual força move o cone?"):
        st.markdown(r"A força magnética sobre um fio com corrente: $\vec F = I\vec\ell\times\vec B$. Com $\vec B$ radial e a corrente azimutal (dando voltas), a força é **axial**.")
    with st.expander("Dica 2 — Um fio que se move num campo"):
        st.markdown(r"Cada pedaço de fio da bobina se move com $\vec v$ (axial) num $\vec B$ radial: $\vec v\times\vec B$ é **azimutal**, ao longo do fio. Integre $(\vec v\times\vec B)\cdot d\vec\ell$ ao longo do fio.")
    with st.expander("Dica 3 — Escreva a corrente em função da fem de retorno"):
        st.markdown(r"Substitua $v = \dot x = \varepsilon/(B\ell)$ na equação mecânica e isole $i$. Cada termo vira uma corrente: $C\,d\varepsilon/dt$, $\varepsilon/R$ e $\frac1L\int\varepsilon\,dt$.")
    with st.expander("Dica 4 — Ressonância"):
        st.markdown(r"$\omega_s^2 = 1/(L_{eq}C_{eq}) = k/m$: é a frequência natural do sistema massa-mola do cone!")

with abas[2]:
    st.markdown("#### Item (a) — Do sinal elétrico ao som")

    def a1():
        st.markdown(
            """
1. O amplificador aplica uma tensão **v(t)** que reproduz a forma da onda sonora; circula uma corrente **i(t)** na bobina.
2. A bobina está imersa no campo **B radial** do ímã. Cada volta sofre a força $\\vec F = i\\,\\vec\\ell\\times\\vec B$, que é **axial** e vale $F = B\\ell\\, i$.
3. A força é **proporcional à corrente**: o cone é empurrado para frente e para trás acompanhando o sinal.
4. O cone, de grande área, comprime e rarefaz o ar ⇒ **ondas de pressão** = som.
5. A suspensão (aranha e borda) funciona como **mola** (k), trazendo o cone de volta, e com **atrito/amortecimento** (b).
"""
        )
        caixa("<b>Por que radial?</b> Com B radial, ele é perpendicular ao fio em <i>todos</i> os pontos da bobina, e as forças em "
              "cada pedacinho de fio apontam todas na <b>mesma direção axial</b> — somam-se em vez de se cancelar. "
              "Além disso, B ℓ permanece constante enquanto a bobina se move dentro do entreferro: força proporcional à corrente ⇒ "
              "<b>baixa distorção</b>. Um campo uniforme (como entre dois polos planos) produziria forças que se cancelariam numa bobina circular.", "fisica")

    passos([("Cadeia de conversões", a1)])

    st.markdown("#### Item (b) — Fem induzida (lei de Faraday)")

    def b1():
        st.markdown(r"Cada elemento $d\vec\ell$ da bobina move-se com $\vec v = v\,\hat z$ num campo $\vec B = B\,\hat\rho$:")
        st.latex(r"\vec v\times\vec B = vB\,(\hat z\times\hat\rho) = vB\,\hat\varphi \quad\text{(ao longo do fio!)}")
        st.latex(r"\varepsilon = \oint(\vec v\times\vec B)\cdot d\vec\ell = vB\oint d\ell = \boxed{B\ell\,v}")
        st.markdown(r"Pela forma de fluxo: em $dt$ o fio “varre” a área $\ell\,v\,dt$ atravessada por $B$ radial, ou seja, $d\Phi = B\ell v\,dt$ — mesmo resultado.")

    def b2():
        st.latex(r"\varepsilon = (7{,}0\ \text{T·m})(0{,}50\ \text{m/s}) = 3{,}5\ \text{V}")
        caixa("<b>Lenz:</b> essa fem <b>se opõe</b> à corrente que produziu o movimento — é uma <b>força contraeletromotriz</b>, "
              "exatamente como num motor elétrico. É por ela que o alto-falante “retira” energia elétrica do amplificador para "
              "transformar em energia mecânica/acústica. Também é ela que <b>freia</b> o cone (amortecimento elétrico).", "fisica")

    passos([("Fem de movimento numa bobina em campo radial", b1), ("Valor e sentido", b2)])

    st.markdown("#### Item (c) — O sistema mecânico como um RLC paralelo")

    def c1():
        st.markdown(r"Na equação mecânica, use $v = \dot x$ e a fem de retorno $\varepsilon = B\ell\,v$ ⇒ $v = \varepsilon/(B\ell)$:")
        st.latex(r"m\frac{dv}{dt} + b\,v + k\int v\,dt = B\ell\,i")
        st.latex(r"\Rightarrow\ i = \underbrace{\frac{m}{(B\ell)^2}}_{C_{eq}}\frac{d\varepsilon}{dt} + \underbrace{\frac{b}{(B\ell)^2}}_{1/R_{eq}}\varepsilon"
                 r" + \underbrace{\frac{k}{(B\ell)^2}}_{1/L_{eq}}\int\varepsilon\,dt")

    def c2():
        st.markdown(r"Compare com um **RLC paralelo** submetido à tensão $\varepsilon$: a corrente total é a soma das correntes em cada ramo,")
        st.latex(r"i = C\frac{d\varepsilon}{dt} + \frac{\varepsilon}{R} + \frac1L\int\varepsilon\,dt")
        st.markdown(r"A identificação é termo a termo. A **mesma tensão** ($\varepsilon$) em todos os elementos e correntes que **se somam** "
                    r"caracterizam uma ligação **em paralelo**. A equação elétrica $V = R_ei + L_e\,di/dt + \varepsilon$ mostra que esse bloco está "
                    r"**em série** com $R_e$ e $L_e$.")
        st.markdown(SVG_CIRCUITO, unsafe_allow_html=True)

    def c3():
        st.latex(r"C_{eq} = \frac{0{,}020}{49} \approx " + f"{Ceq*1e6:.0f}" + r"\ \mu\text{F},\qquad L_{eq} = \frac{49}{2000} = "
                 + f"{Leq*1e3:.1f}".replace('.', '{,}') + r"\ \text{mH},\qquad R_{eq} = \frac{49}{1{,}5}\approx " + f"{Req:.1f}".replace('.', '{,}') + r"\ \Omega")
        caixa("<b>Dualidade curiosa:</b> a <b>massa</b> (inércia) vira um <b>capacitor</b>, e a <b>mola</b> vira um <b>indutor</b>. "
              "No RLC série “direto” (analogia força–tensão) seria o contrário; aqui, como a fem é proporcional à velocidade, "
              "aparece a analogia <i>mobilidade</i>. Note também: amortecimento mecânico pequeno (b pequeno) ⇒ R_eq grande.", "fisica")

    passos([("Reescrevendo a equação mecânica em termos de ε", c1), ("Identificando o RLC paralelo", c2), ("Valores numéricos", c3)])

    st.markdown("#### Item (d) — Ressonância e o pico de impedância")

    def d1():
        st.latex(r"f_s = \frac{1}{2\pi\sqrt{L_{eq}C_{eq}}} = \frac{1}{2\pi}\sqrt{\frac{k}{m}} = \frac{1}{2\pi}\sqrt{\frac{2000}{0{,}020}}\approx "
                 + f"{fs:.1f}".replace('.', '{,}') + r"\ \text{Hz}")

    def d2():
        st.markdown(r"Na ressonância de um RLC **paralelo**, os ramos L e C se cancelam e a impedância do bloco é **máxima** e igual a $R_{eq}$:")
        st.latex(r"Z(f_s) = R_e + j\omega_sL_e + R_{eq} \approx 6{,}0 + 32{,}7 + j\,0{,}16\ \Omega\ \Rightarrow\ |Z|\approx "
                 + f"{Zfs:.1f}".replace('.', '{,}') + r"\ \Omega")
        caixa("<b>Interpretação física:</b> na ressonância mecânica o cone se move com a <b>maior velocidade</b> para uma dada força. "
              "Maior velocidade ⇒ maior fem de retorno Bℓv ⇒ ela “cancela” boa parte da tensão aplicada ⇒ a corrente cai ⇒ "
              "o amplificador “vê” uma impedância <b>alta</b>. Daí o pico (e não vale): é o oposto do RLC série porque aqui o bloco ressonante está em paralelo. "
              "Um alto-falante de “6 Ω nominais” chega a quase 40 Ω em f_s!", "fisica")

    passos([("Frequência de ressonância", d1), ("Impedância e o porquê do pico", d2)])

    st.markdown("#### Item (e) — O fone como microfone")

    def e1():
        st.markdown(
            r"""
O transdutor é **reversível**. Quando a onda sonora empurra o diafragma, a bobina se move com velocidade $v(t)$ no campo radial e,
pela **lei de Faraday**, surge $\varepsilon(t) = B\ell\,v(t)$ — uma tensão que reproduz a pressão sonora. É exatamente o princípio do
**microfone dinâmico**. A tensão é pequena (fones têm $B\ell$ e áreas pequenos: tipicamente mV), por isso a entrada de microfone, que tem um
pré-amplificador de alto ganho, consegue usá-la.
"""
        )

    passos([("Reciprocidade do transdutor eletrodinâmico", e1)])

with abas[3]:
    st.markdown("### Simulador de alto-falante")
    c1, c2 = st.columns([1, 3])
    with c1:
        Bl_l = st.slider("Bℓ (T·m)", 1.0, 20.0, 7.0, 0.5)
        Re_l = st.slider("Rₑ (Ω)", 2.0, 16.0, 6.0, 0.5)
        Le_l = st.slider("Lₑ (mH)", 0.0, 3.0, 0.5, 0.1) * 1e-3
        m_l = st.slider("massa móvel m (g)", 1.0, 100.0, 20.0, 1.0) / 1000
        k_l = st.slider("rigidez k (N/m)", 200.0, 10000.0, 2000.0, 100.0)
        b_l = st.slider("amortecimento b (N·s/m)", 0.2, 10.0, 1.5, 0.1)
        V0 = st.slider("Tensão do amplificador V₀ (V)", 0.5, 20.0, 2.83, 0.01, help="2,83 V ≈ 1 W em 8 Ω (padrão de medida)")
    with c2:
        ff = np.logspace(1, np.log10(20000), 800)
        r = falante_resposta(ff, V0, Bl_l, Re_l, Le_l, m_l, k_l, b_l)
        r_sem = falante_Z(ff, 0.0, Re_l, Le_l, m_l, k_l, b_l)
        fs_l = np.sqrt(k_l / m_l) / (2 * np.pi)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                            subplot_titles=("Impedância elétrica |Z(f)|", "Deslocamento do cone |x(f)|"),
                            specs=[[{"secondary_y": True}], [{}]])
        fig.add_trace(go.Scatter(x=ff, y=np.abs(r["Z"]), name="|Z| (Ω)", line=dict(color="#2563eb", width=3)), row=1, col=1)
        fig.add_trace(go.Scatter(x=ff, y=np.abs(r_sem), name="|Z| se Bℓ = 0 (bobina bloqueada)", line=dict(color="gray", dash="dash")),
                      row=1, col=1)
        fig.add_trace(go.Scatter(x=ff, y=np.degrees(np.angle(r["Z"])), name="fase de Z (°)", line=dict(color="#7c3aed", dash="dot")),
                      row=1, col=1, secondary_y=True)
        fig.add_trace(go.Scatter(x=ff, y=np.abs(r["x"]) * 1e3, name="|x| (mm)", line=dict(color="#16a34a", width=3)), row=2, col=1)
        for rr in (1, 2):
            fig.add_vline(x=fs_l, line_dash="dot", line_color="#dc2626", row=rr, col=1)
        fig.update_xaxes(type="log", title_text="f (Hz)", row=2, col=1)
        fig.update_xaxes(type="log", row=1, col=1)
        fig.update_yaxes(title_text="Ω", row=1, col=1)
        fig.update_yaxes(title_text="fase (°)", row=1, col=1, secondary_y=True, range=[-90, 90])
        fig.update_yaxes(title_text="mm", type="log", row=2, col=1)
        fig.update_layout(height=620, legend=dict(orientation="h", y=-0.12))
        st.plotly_chart(fig, width="stretch")
    rs = falante_resposta(fs_l, V0, Bl_l, Re_l, Le_l, m_l, k_l, b_l)
    mm = st.columns(5)
    mm[0].metric("f_s", f"{fs_l:.1f} Hz")
    mm[1].metric("|Z(f_s)|", f"{abs(rs['Z']):.1f} Ω")
    mm[2].metric("R_eq = (Bℓ)²/b", f"{Bl_l**2/b_l:.1f} Ω")
    mm[3].metric("velocidade do cone em f_s", fmt(abs(rs["v"]), "m/s"))
    mm[4].metric("fem de retorno em f_s", fmt(abs(rs["fem"]), "V"), f"{abs(rs['fem'])/V0*100:.0f}% de V₀")
    caixa("Experimente: (1) zere quase o amortecimento b — o pico fica altíssimo e estreito (R_eq ∝ 1/b). "
          "(2) Aumente a massa — f_s desce (mais grave). (3) Aumente Bℓ — o pico cresce (∝ (Bℓ)²) e o cone fica mais “controlado”. "
          "(4) Em altas frequências, |Z| sobe de novo por causa de Lₑ: o fio da bobina é um indutor comum. "
          "Compare com a curva cinza: sem acoplamento (Bℓ = 0), não há pico nenhum — o pico é <b>pura indução de Faraday</b>.", "dica")

    st.markdown("### Animação: a fem de retorno “come” a tensão aplicada")
    fsel = st.select_slider("Frequência do sinal (Hz)", [20, 30, 40, 45, 50, 55, 60, 80, 100, 200, 500, 1000], 50)
    rr = falante_resposta(fsel, V0, Bl, Re, Le, m, k, b)
    t = np.linspace(0, 2 / fsel, 400)
    w = 2 * np.pi * fsel
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t * 1e3, y=V0 * np.cos(w * t), name="V aplicada", line=dict(color="black", width=3)))
    fig.add_trace(go.Scatter(x=t * 1e3, y=np.real(rr["fem"] * np.exp(1j * w * t)), name="fem de retorno Bℓv", line=dict(color="#dc2626")))
    fig.add_trace(go.Scatter(x=t * 1e3, y=np.real(rr["i"] * Re * np.exp(1j * w * t)), name="queda em Rₑ (= Rₑ·i)", line=dict(color="#2563eb")))
    fig.update_layout(height=340, xaxis_title="t (ms)", yaxis_title="V", title=f"Parâmetros da prova, f = {fsel} Hz")
    st.plotly_chart(fig, width="stretch")
    st.caption("Perto de 50 Hz a fem de retorno quase iguala a tensão aplicada e fica em fase com ela: sobra pouca tensão para Rₑ ⇒ corrente pequena ⇒ |Z| grande.")

    st.markdown("### Modo microfone (item e)")
    c1, c2 = st.columns(2)
    with c1:
        Bl_fone = st.slider("Bℓ de um fone (T·m)", 0.1, 3.0, 0.8, 0.1)
        v_fone = st.slider("Velocidade do diafragma (mm/s)", 0.1, 50.0, 5.0, 0.1)
    with c2:
        st.metric("Tensão gerada ε = Bℓv", fmt(Bl_fone * v_fone * 1e-3, "V"))
        st.caption("Ordem de grandeza típica de um microfone dinâmico: de centenas de μV a alguns mV — por isso ele precisa de pré-amplificador.")

with abas[4]:
    confira("(b) Fem para v = 0,50 m/s", Bl * v_teste, "V", "q5b")
    confira("(c) C_eq", Ceq, "μF", "q5c1", escala=1e-6)
    confira("(c) L_eq", Leq, "mH", "q5c2", escala=1e-3)
    confira("(c) R_eq", Req, "Ω", "q5c3")
    confira("(d) f_s", fs, "Hz", "q5d1", dica_erro="ω_s = √(k/m); não esqueça de converter 20 g → 0,020 kg e de dividir por 2π.")
    confira("(d) |Z(f_s)|", Zfs, "Ω", "q5d2", dica_erro="Na ressonância o bloco paralelo vale R_eq; some R_e (o termo de L_e é pequeno).")

with abas[5]:
    quiz("1) Se dobrarmos a massa móvel do cone, a frequência de ressonância:",
         ["dobra", "cai pelo fator √2", "cai à metade", "não muda"], 1, "f_s ∝ √(k/m).", "q5q1")
    quiz("2) O amortecimento “elétrico” do cone quando o amplificador (fonte de tensão de baixa impedância) está ligado vem de:",
         ["atrito do ar apenas", "a corrente induzida pela fem de retorno, que gera uma força que se opõe ao movimento",
          "o peso do cone", "a indutância Lₑ"], 1,
         "A fem Bℓv faz circular corrente pelo circuito, e essa corrente sofre força Bℓi oposta à velocidade (Lenz). É o “fator de amortecimento” dos amplificadores.", "q5q2")
    quiz("3) Com a bobina desconectada (circuito aberto), o cone, ao ser tocado:",
         ["fica mais amortecido", "fica menos amortecido (sem corrente induzida, não há freio elétrico)", "não se move", "gera mais tensão nos terminais"], 1,
         "Experimente em casa: dê um toque no cone com os terminais abertos e depois em curto. Em curto, o movimento é bem mais “morto”.", "q5q3")
    st.markdown("#### ⚠️ Erros comuns")
    caixa("• Dizer que o ímã “atrai e repele” a bobina como dois ímãs — a descrição correta é a força de Lorentz sobre a corrente num campo radial.<br>"
          "• Confundir a fem de retorno (que se opõe) com uma fonte extra que ajuda a corrente.<br>"
          "• Achar que a impedância nominal (6 Ω) é constante em frequência.<br>"
          "• Trocar as associações: massa ↔ capacitor e mola ↔ indutor nesta analogia (não o contrário).", "alerta")

rodape()
