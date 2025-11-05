import streamlit as st

st.set_page_config(page_title="Verificador de Dimensões", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #f2f2f2;
    }
    h1 {
        text-align: center;
        font-size: 38px;
        margin-bottom: 40px;
        color: #222;
    }
    h2 {
        font-size: 32px;
        margin-bottom: 10px;
    }
    .section {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 35px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    }
    .amazon h2 { color: #ff9900; }
    .correios h2 { color: #004aad; }
    .ml h2 { color: #ffcc00; }

    .rules {
        background-color: #fafafa;
        padding: 15px 20px;
        border-left: 4px solid #ccc;
        border-radius: 8px;
        margin-bottom: 25px;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #e0e0e0 !important;
        color: #222 !important;
        font-size: 18px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #d5d5d5 !important;
    }
    .result-ok {
        color: green;
        font-size: 20px;
        font-weight: bold;
    }
    .result-fail {
        color: red;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Teste de Dimensões</h1>", unsafe_allow_html=True)

# ---------------- AMAZON ----------------
st.markdown('<div class="section amazon">', unsafe_allow_html=True)
st.markdown("<h2>Amazon</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="rules">
    <ul>
        <li>Cada lado ≤ <strong>105 cm</strong></li>
        <li>Soma total (altura + largura + comprimento) ≤ <strong>200 cm</strong></li>
        <li>Peso máximo ≤ <strong>30 kg</strong></li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

colA1, colA2, colA3, colA4 = st.columns(4)
altura_amazon = colA1.number_input("Altura (cm)", key="altura_amazon", min_value=0)
largura_amazon = colA2.number_input("Largura (cm)", key="largura_amazon", min_value=0)
comprimento_amazon = colA3.number_input("Comprimento (cm)", key="comprimento_amazon", min_value=0)
peso_amazon = colA4.number_input("Peso (kg)", key="peso_amazon", min_value=0)

if st.button("Verificar Amazon"):
    soma = altura_amazon + largura_amazon + comprimento_amazon
    if (
        altura_amazon <= 105
        and largura_amazon <= 105
        and comprimento_amazon <= 105
        and soma <= 200
        and peso_amazon <= 30
    ):
        st.markdown('<p class="result-ok">✅ Atende às dimensões da Amazon</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result-fail">❌ Não atende às dimensões da Amazon</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- CORREIOS ----------------
st.markdown('<div class="section correios">', unsafe_allow_html=True)
st.markdown("<h2>Correios</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="rules">
    <ul>
        <li>Cada lado ≤ <strong>100 cm</strong></li>
        <li>Soma total (altura + largura + comprimento) ≤ <strong>200 cm</strong></li>
        <li>Peso máximo ≤ <strong>30 kg</strong></li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

colC1, colC2, colC3, colC4 = st.columns(4)
altura_correios = colC1.number_input("Altura (cm)", key="altura_correios", min_value=0)
largura_correios = colC2.number_input("Largura (cm)", key="largura_correios", min_value=0)
comprimento_correios = colC3.number_input("Comprimento (cm)", key="comprimento_correios", min_value=0)
peso_correios = colC4.number_input("Peso (kg)", key="peso_correios", min_value=0)

if st.button("Verificar Correios"):
    soma = altura_correios + largura_correios + comprimento_correios
    if (
        altura_correios <= 100
        and largura_correios <= 100
        and comprimento_correios <= 100
        and soma <= 200
        and peso_correios <= 30
    ):
        st.markdown('<p class="result-ok">✅ Atende às dimensões dos Correios</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result-fail">❌ Não atende às dimensões dos Correios</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------- MERCADO LIVRE ----------------
st.markdown('<div class="section ml">', unsafe_allow_html=True)
st.markdown("<h2>Mercado Livre</h2>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="rules">
    <ul>
        <li>Cada lado ≤ <strong>200 cm</strong></li>
        <li>Soma total (altura + largura + comprimento) ≤ <strong>300 cm</strong></li>
        <li>Peso máximo ≤ <strong>50 kg</strong></li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# corrigido: nomes sem “ML” visível, mas keys únicas
colM1, colM2, colM3, colM4 = st.columns(4)
altura_ml = colM1.number_input("Altura (cm)", key="altura_ml", min_value=0)
largura_ml = colM2.number_input("Largura (cm)", key="largura_ml", min_value=0)
comprimento_ml = colM3.number_input("Comprimento (cm)", key="comprimento_ml", min_value=0)
peso_ml = colM4.number_input("Peso (kg)", key="peso_ml", min_value=0)

if st.button("Verificar Mercado Livre"):
    soma = altura_ml + largura_ml + comprimento_ml
    if (
        altura_ml <= 200
        and largura_ml <= 200
        and comprimento_ml <= 200
        and soma <= 300
        and peso_ml <= 50
    ):
        st.markdown('<p class="result-ok">✅ Atende às dimensões do Mercado Livre</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result-fail">❌ Não atende às dimensões do Mercado Livre</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
