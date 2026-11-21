import numpy as np
import plotly.graph_objects as go
import streamlit as st

from comum import caixa, configurar_pagina, confira, fmt, passos, quiz, rodape
from modelos import (MU0, B_centro_poligono, B_dipolo_eixo, B_eixo_espira,
                            biot_savart_numerico, espira_circular_pts)

configurar_pagina("Q1 — Biot–Savart", "🌀")
st.title("🌀 Questão 1 — Lei de Biot–Savart")

I, a, z, L = 5.0, 0.10, 0.10, 0.20
B0 = MU0 * I / (2 * a)
Bz = B_eixo_espira(I, a, z)
Bq = 2 * np.sqrt(2) * MU0 * I / (np.pi * L)
Bc = MU0 * I / L

abas = st.tabs(["📝 Enunciado", "🧭 Estratégia", "✍️ Resolução", "🎛️ Laboratório", "✅ Confira", "🧠 Conceitos"])

# ------------------------------------------------------------------ Enunciado
with abas[0]:
    st.markdown(
        r"""
<div class="enunciado">

Uma espira circular de raio $a = 10{,}0$ cm conduz uma corrente estacionária $I = 5{,}0$ A.

**(a)** *(8 pts)* Partindo da lei de Biot–Savart, mostre que o campo em um ponto do eixo da espira, a uma distância $z$ do centro, é
$B(z) = \dfrac{\mu_0 I a^2}{2(a^2+z^2)^{3/2}}$. Explique por simetria por que as componentes perpendiculares ao eixo se cancelam.

**(b)** *(4 pts)* Calcule $B$ no centro e em $z = 10{,}0$ cm.

**(c)** *(5 pts)* A mesma corrente percorre uma espira **quadrada** de lado $L = 20{,}0$ cm. Usando
$B = \frac{\mu_0 I}{4\pi d}(\sin\theta_2-\sin\theta_1)$ para um segmento finito, mostre que no centro
$B_\square = \frac{2\sqrt2\,\mu_0 I}{\pi L}$ e calcule-o. Compare com uma espira circular **inscrita** ($a = L/2$).

**(d)** *(3 pts)* Mostre que, para $z\gg a$, $B\approx \frac{\mu_0\mathfrak m}{2\pi z^3}$ com $\mathfrak m = I\pi a^2$. Qual o significado de $\mathfrak m$?
</div>
""",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ Estratégia
with abas[1]:
    st.markdown("Abra as dicas **uma de cada vez** e tente avançar sozinho entre elas.")
    with st.expander("Dica 1 — O que é constante ao longo da espira?"):
        st.markdown(r"Para um ponto **no eixo**, a distância $r$ de *qualquer* elemento $d\vec\ell$ até o ponto é a mesma: "
                    r"$r=\sqrt{a^2+z^2}$. Além disso, $d\vec\ell$ é sempre perpendicular a $\vec r$. Isso simplifica muito o produto vetorial.")
    with st.expander("Dica 2 — Desenhe dois elementos diametralmente opostos"):
        st.markdown(r"Os $d\vec B$ de dois elementos opostos têm a **mesma** componente ao longo de $z$ e componentes radiais **opostas**. "
                    r"Logo, só a componente $dB_z = dB\cos\alpha$ sobrevive, com $\cos\alpha = a/r$.")
    with st.expander("Dica 3 — Para o quadrado"):
        st.markdown(r"Cada lado é um segmento a distância $d = L/2$ do centro, visto sob ângulos $\theta_1=-45^\circ$ e $\theta_2=+45^\circ$. "
                    r"Os quatro lados contribuem **no mesmo sentido** (regra da mão direita).")
    with st.expander("Dica 4 — Limite de dipolo"):
        st.markdown(r"Se $z\gg a$, então $a^2+z^2\approx z^2$ e $(a^2+z^2)^{3/2}\approx z^3$.")

# ------------------------------------------------------------------ Resolução
with abas[2]:
    st.markdown("#### Item (a) — Campo no eixo")

    def p1():
        st.markdown(r"Escolhemos o eixo $z$ passando pelo centro, perpendicular ao plano da espira. Um elemento $d\vec\ell$ "
                    r"está na posição $(a\cos\varphi, a\sin\varphi, 0)$ e o ponto de observação é $(0,0,z)$.")
        st.latex(r"r = \sqrt{a^2+z^2}\quad\text{(igual para todos os elementos!)},\qquad d\vec\ell\perp\vec r \Rightarrow |d\vec\ell\times\hat r| = d\ell")

    def p2():
        st.latex(r"dB = \frac{\mu_0}{4\pi}\frac{I\,d\ell}{r^2} = \frac{\mu_0}{4\pi}\frac{I\,d\ell}{a^2+z^2}")
        st.markdown(r"Esse $d\vec B$ é perpendicular ao plano formado por $d\vec\ell$ e $\vec r$: ele aponta **inclinado**, formando um ângulo "
                    r"$\alpha$ com o eixo, onde $\cos\alpha = a/r$.")

    def p3():
        st.markdown(r"**Argumento de simetria.** Para cada elemento em $\varphi$ existe outro em $\varphi+\pi$. Suas contribuições têm a mesma "
                    r"componente $z$ e componentes radiais **opostas**, que se anulam aos pares. Por isso só precisamos somar $dB_z$:")
        st.latex(r"dB_z = dB\cos\alpha = \frac{\mu_0}{4\pi}\frac{I\,d\ell}{a^2+z^2}\cdot\frac{a}{\sqrt{a^2+z^2}}")
        caixa("Veja isso acontecendo na aba <b>Laboratório</b>: o gráfico 3D mostra os vetores dB formando um cone; "
              "a soma deles aponta só ao longo do eixo.", "fisica")

    def p4():
        st.markdown(r"Como tudo é constante ao longo da espira, a integral é só $\oint d\ell = 2\pi a$:")
        st.latex(r"B(z) = \frac{\mu_0 I a}{4\pi(a^2+z^2)^{3/2}}\oint d\ell = \frac{\mu_0 I a}{4\pi(a^2+z^2)^{3/2}}\,2\pi a"
                 r"\;\Longrightarrow\; \boxed{B(z) = \frac{\mu_0 I a^2}{2(a^2+z^2)^{3/2}}}")
        st.markdown("Sentido: regra da mão direita — dedos no sentido da corrente, polegar indica $\\vec B$ no eixo.")

    passos([("Geometria", p1), ("Módulo de dB", p2), ("Simetria: só sobra a componente z", p3), ("Integração", p4)])

    st.markdown("#### Item (b) — Valores numéricos")

    def b1():
        st.latex(r"B(0) = \frac{\mu_0 I}{2a} = \frac{(4\pi\times10^{-7})(5{,}0)}{2(0{,}10)} = \pi\times10^{-5}\ \text{T}")
        st.markdown(f"**B(0) ≈ {fmt(B0,'T')}**")

    def b2():
        st.latex(r"B(z) = \frac{\mu_0 I a^2}{2(a^2+z^2)^{3/2}} = \frac{(4\pi\times10^{-7})(5{,}0)(0{,}10)^2}{2\,(0{,}02)^{3/2}}")
        st.markdown(f"**B(10 cm) ≈ {fmt(Bz,'T')}** — exatamente $B(0)/2^{{3/2}} = B(0)/(2\\sqrt2)$, pois com $z=a$ temos $(2a^2)^{{3/2}} = 2\\sqrt2\\,a^3$.")

    passos([("Centro da espira", b1), ("Em z = a", b2)])

    st.markdown("#### Item (c) — Espira quadrada")

    def c1():
        st.markdown(r"Cada lado está a $d=L/2$ do centro. Visto do centro, o lado vai de $\theta_1=-45^\circ$ a $\theta_2=+45^\circ$:")
        st.latex(r"B_{\text{lado}} = \frac{\mu_0 I}{4\pi (L/2)}\left[\sin 45^\circ - \sin(-45^\circ)\right] = \frac{\mu_0 I}{2\pi L}\cdot\sqrt2")

    def c2():
        st.markdown("Os quatro lados produzem campo **no mesmo sentido** no centro (todos “giram” a corrente do mesmo modo):")
        st.latex(r"B_\square = 4\,\frac{\sqrt2\,\mu_0 I}{2\pi L} = \boxed{\frac{2\sqrt2\,\mu_0 I}{\pi L}}")
        st.markdown(f"**B□ ≈ {fmt(Bq,'T')}**")

    def c3():
        st.latex(r"B_{\circ}(a=L/2) = \frac{\mu_0 I}{2(L/2)} = \frac{\mu_0 I}{L} \approx " + f"{Bc*1e6:.1f}".replace('.', '{,}') + r"\ \mu\text{T}")
        st.latex(r"\frac{B_\square}{B_\circ} = \frac{2\sqrt2}{\pi}\approx 0{,}90")
        caixa("<b>Interpretação:</b> o círculo inscrito tem <i>todos</i> os seus pontos à distância L/2 do centro. "
              "No quadrado, só o meio de cada lado está a L/2; os cantos estão mais longe (até L/√2) e ainda contribuem "
              "com ângulo desfavorável. Como dB ∝ 1/r², a corrente “mais afastada” do quadrado produz menos campo, "
              "apesar de o quadrado ter mais fio (4L = 8a contra 2πa ≈ 6,28a).", "fisica")

    passos([("Campo de um lado", c1), ("Somando os quatro lados", c2), ("Comparação com o círculo inscrito", c3)])

    st.markdown("#### Item (d) — Limite de dipolo")

    def d1():
        st.latex(r"z\gg a\ \Rightarrow\ (a^2+z^2)^{3/2}\approx z^3\ \Rightarrow\ B\approx\frac{\mu_0 I a^2}{2z^3}"
                 r"=\frac{\mu_0 (I\pi a^2)}{2\pi z^3}=\frac{\mu_0\,\mathfrak m}{2\pi z^3}")
        st.markdown(r"$\mathfrak m = IA$ é o **momento de dipolo magnético** da espira: longe dela, só importa o produto corrente × área "
                    r"(e a orientação), não a forma. O campo cai com $1/z^3$, como o campo elétrico de um dipolo elétrico.")

    passos([("Aproximação e identificação do dipolo", d1)])

# ------------------------------------------------------------------ Laboratório
with abas[3]:
    st.markdown("### 1. Veja a simetria acontecer (3D)")
    c1, c2 = st.columns([1, 3])
    with c1:
        n_el = st.slider("Nº de elementos dℓ mostrados", 2, 24, 8, step=2)
        z_rel = st.slider("Posição z/a do ponto", 0.0, 3.0, 1.0, 0.1)
        mostrar_soma = st.checkbox("Mostrar soma vetorial", True)
    with c2:
        a_ = 1.0
        zp = z_rel * a_
        phi = np.linspace(0, 2 * np.pi, n_el, endpoint=False)
        t = np.linspace(0, 2 * np.pi, 200)
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(x=np.cos(t), y=np.sin(t), z=0 * t, mode="lines",
                                   line=dict(color="#dc2626", width=6), name="espira"))
        fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[-0.5, 3.2], mode="lines",
                                   line=dict(color="gray", dash="dash"), name="eixo z"))
        escala = 0.9
        soma = np.zeros(3)
        for k, ph in enumerate(phi):
            pos = np.array([np.cos(ph), np.sin(ph), 0])
            dl = np.array([-np.sin(ph), np.cos(ph), 0])
            r = np.array([0, 0, zp]) - pos
            dB = np.cross(dl, r) / np.linalg.norm(r) ** 3
            soma += dB
            tip = np.array([0, 0, zp]) + escala * dB / max(1e-9, (1 / (1 + zp**2)))
            fig.add_trace(go.Scatter3d(x=[0, tip[0]], y=[0, tip[1]], z=[zp, tip[2]], mode="lines",
                                       line=dict(color="#2563eb", width=4), showlegend=(k == 0), name="dB de cada elemento"))
            fig.add_trace(go.Scatter3d(x=[pos[0], pos[0] + 0.25 * dl[0]], y=[pos[1], pos[1] + 0.25 * dl[1]], z=[0, 0],
                                       mode="lines", line=dict(color="#ea580c", width=8), showlegend=(k == 0), name="dℓ"))
        if mostrar_soma:
            sv = soma / n_el
            tip = np.array([0, 0, zp]) + escala * sv / max(1e-9, (1 / (1 + zp**2))) * 1.0
            fig.add_trace(go.Scatter3d(x=[0, tip[0]], y=[0, tip[1]], z=[zp, tip[2]], mode="lines+markers",
                                       line=dict(color="#16a34a", width=10), marker=dict(size=3), name="média dos dB (∥ eixo)"))
        fig.update_layout(height=520, margin=dict(l=0, r=0, t=10, b=0),
                          scene=dict(aspectmode="data", xaxis_title="x/a", yaxis_title="y/a", zaxis_title="z/a"))
        st.plotly_chart(fig, width="stretch")
    caixa("Gire o gráfico com o mouse. Os vetores azuis formam um <b>cone</b>: cada um tem uma componente ao longo do eixo e "
          "outra radial. As radiais apontam em todas as direções e se cancelam; a média (verde) é puramente axial.", "fisica")

    st.markdown("### 2. Perfil B(z) — exato, numérico e dipolo")
    c1, c2 = st.columns([1, 3])
    with c1:
        I_l = st.slider("Corrente I (A)", 0.5, 20.0, 5.0, 0.5)
        a_l = st.slider("Raio a (cm)", 2.0, 30.0, 10.0, 1.0) / 100
        log = st.checkbox("Escala log-log (ver lei 1/z³)", False)
    with c2:
        zz = np.linspace(0.001, 6 * a_l, 400) if not log else np.logspace(np.log10(0.05 * a_l), np.log10(30 * a_l), 300)
        Bex = B_eixo_espira(I_l, a_l, zz)
        Bdip = B_dipolo_eixo(I_l, a_l, zz)
        pts = espira_circular_pts(a_l, 400)
        zn = zz[:: max(1, len(zz) // 25)]
        Bnum = [np.linalg.norm(biot_savart_numerico(pts, I_l, np.array([0, 0, zi]))) for zi in zn]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=zz * 100, y=Bex * 1e6, name="analítico", line=dict(color="#2563eb", width=3)))
        fig.add_trace(go.Scatter(x=zn * 100, y=np.array(Bnum) * 1e6, mode="markers", name="Biot–Savart numérico (400 elementos)",
                                 marker=dict(color="#ea580c", size=8, symbol="x")))
        fig.add_trace(go.Scatter(x=zz * 100, y=Bdip * 1e6, name="aproximação de dipolo", line=dict(color="#16a34a", dash="dash")))
        fig.update_layout(xaxis_title="z (cm)", yaxis_title="B (μT)", height=420,
                          yaxis=dict(type="log" if log else "linear", range=None if log else [0, 1.15 * Bex.max() * 1e6]),
                          xaxis=dict(type="log" if log else "linear"), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, width="stretch")
    st.markdown("Para qual $z/a$ o erro da aproximação de dipolo cai abaixo de 5%?")
    zr = np.linspace(0.1, 10, 5000)
    erro = B_dipolo_eixo(1, 1, zr) / B_eixo_espira(1, 1, zr) - 1
    st.info(f"Erro < 5% para z/a > {zr[np.argmax(erro < 0.05)]:.2f}. (Verifique: o erro relativo é (1+a²/z²)^{{3/2}} − 1 ≈ 1,5·a²/z².)")

    st.markdown("### 3. Do quadrado ao círculo: polígonos regulares")
    c1, c2 = st.columns([1, 3])
    with c1:
        N = st.slider("Número de lados N", 3, 40, 4)
        st.latex(r"B_N = \frac{\mu_0 I N\sin(\pi/N)}{2\pi d}")
        st.caption("d = apótema (distância do centro ao meio de cada lado). Para N=4: o resultado do item (c).")
    with c2:
        Ns = np.arange(3, 41)
        razao = B_centro_poligono(1, Ns, 1) / (MU0 / 2)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Ns, y=razao, mode="lines+markers", name="B_N / B_círculo inscrito", line=dict(color="#7c3aed")))
        fig.add_trace(go.Scatter(x=[N], y=[B_centro_poligono(1, N, 1) / (MU0 / 2)], mode="markers",
                                 marker=dict(size=16, color="#dc2626"), name=f"N = {N}"))
        fig.add_hline(y=1, line_dash="dot", annotation_text="círculo")
        fig.update_layout(xaxis_title="N", yaxis_title="B_N / (μ₀I/2d)", height=360)
        st.plotly_chart(fig, width="stretch")
    st.write(f"Para N = {N}: B_N/B_círculo = {B_centro_poligono(1, N, 1) / (MU0 / 2):.4f}. "
             "Quanto mais lados, mais o polígono se aproxima do círculo inscrito (por baixo).")

# ------------------------------------------------------------------ Confira
with abas[4]:
    st.markdown("Digite seus resultados **na unidade indicada**.")
    confira("(b) B no centro", B0, "μT", "q1b1", escala=1e-6)
    confira("(b) B em z = 10 cm", Bz, "μT", "q1b2", escala=1e-6,
            dica_erro="Lembre: (a²+z²)^(3/2) com a = z = 0,10 m dá (0,02)^(3/2) ≈ 2,83×10⁻³ m³.")
    confira("(c) B no centro do quadrado", Bq, "μT", "q1c", escala=1e-6)
    confira("(c) razão B□ / B○ (inscrito)", Bq / Bc, "adimensional", "q1c2")

# ------------------------------------------------------------------ Conceitos
with abas[5]:
    quiz("1) Se dobrarmos o raio da espira mantendo I, o campo no centro:",
         ["dobra", "cai à metade", "cai a um quarto", "não muda"], 1,
         "B(0) = μ₀I/2a: o comprimento do fio dobra (×2), mas cada elemento fica 2× mais longe (÷4).", "q1q1")
    quiz("2) Longe da espira (z ≫ a), dobrar z faz o campo:",
         ["cair à metade", "cair a 1/4", "cair a 1/8", "não mudar"], 2, "Regime de dipolo: B ∝ 1/z³.", "q1q2")
    quiz("3) Por que não podemos usar a lei de Ampère para obter B no eixo da espira?",
         ["Porque a corrente não é estacionária",
          "Porque não há simetria suficiente para escolher uma curva amperiana onde B seja constante e conhecido",
          "Porque a lei de Ampère só vale no vácuo", "Podemos, e dá o mesmo resultado mais rápido"], 1,
         "Ampère é sempre verdadeira, mas só é útil para calcular B com alta simetria (fio infinito, solenoide, toroide).", "q1q3")
    st.markdown("#### ⚠️ Erros comuns")
    caixa("• Integrar o <b>módulo</b> dB sem projetar no eixo (esquecer o cos α = a/r) → resultado com a em vez de a²/r.<br>"
          "• Usar r = z em vez de r = √(a²+z²).<br>"
          "• No quadrado, usar ângulos de 0 a 90° (isso valeria para o ponto na extremidade, não no centro).<br>"
          "• Esquecer de converter cm → m.", "alerta")

rodape()
