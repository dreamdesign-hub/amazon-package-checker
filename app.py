# app.py — Amazon + Correios + Mercado Livre (layout aprimorado)
import re
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon, Correios & Mercado Livre", page_icon="📦", layout="centered")

# ======= Estilo CSS =======
st.markdown("""
    <style>
    /* Centralizar tudo e ajustar fontes */
    body { font-family: "Inter", sans-serif; color: #222; }
    h1, h2, h3 { color: #1a1a1a; }
    .section-box {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 24px 20px;
        margin-bottom: 25px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .title {
        font-size: 22px;
        font-weight: 600;
        color: #333;
        margin-bottom: 10px;
    }
    .desc {
        font-size: 14px;
        color: #555;
        margin-bottom: 15px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px !important;
        padding: 0.6em 1em;
        font-weight: 600;
        background-color: #0072ff;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #005ce6;
    }
    </style>
""", unsafe_allow_html=True)

# ======= Utilitários =======
def _to_float(s):
    if s is None or str(s).strip() == "":
        raise ValueError("valor vazio")
    s = str(s).strip().replace(",", ".")
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

# ======= Regras =======
def evaluate_amazon(maior, meio, menor):
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"status": "❌ Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"status": "❌ Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"status": "✅ Aceita", "motivo": "Dentro dos limites da Amazon"}

def check_amazon(m1, m2, m3):
    maior, meio, menor = normalize_dims([m1, m2, m3])
    return evaluate_amazon(maior, meio, menor)

def evaluate_correios(a, b, c):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    if any(x > 100 for x in lados):
        maior_excesso = max(lados)
        return {"status": "❌ Não aceita", "motivo": f"um dos lados {maior_excesso:.2f} > 100 cm"}
    soma = sum(lados)
    if soma > 200:
        return {"status": "❌ Não aceita", "motivo": f"soma {soma:.2f} > 200 cm"}
    return {"status": "✅ Aceita", "motivo": "Dentro das regras dos Correios"}

def evaluate_ml(a, b, c, peso):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    p = _to_float(peso)
    if any(x > 200 for x in lados):
        maior_excesso = max(lados)
        return {"status": "❌ Não aceita", "motivo": f"um dos lados {maior_excesso:.2f} > 200 cm"}
    soma = sum(lados)
    if soma > 300:
        return {"status": "❌ Não aceita", "motivo": f"soma {soma:.2f} > 300 cm"}
    if p > 50:
        return {"status": "❌ Não aceita", "motivo": f"peso {p:.2f} kg > 50 kg"}
    return {"status": "✅ Aceita", "motivo": "Dentro das regras do Mercado Livre"}

# ======= UI =======
st.title("📦 Teste de Dimensões — Amazon, Correios & Mercado Livre")
st.markdown("Verifique rapidamente se suas embalagens atendem às regras de envio de cada transportadora.")

# ---- Amazon ----
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">📦 Amazon</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc">Regras: maior + 2 × (largura + altura) ≤ 432 cm e maior lado ≤ 180 cm.</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        amz1 = st.text_input("Medida 1 (cm)", value="", placeholder="ex.: 120", key="a1")
    with col2:
        amz2 = st.text_input("Medida 2 (cm)", value="", placeholder="ex.: 50", key="a2")
    with col3:
        amz3 = st.text_input("Medida 3 (cm)", value="", placeholder="ex.: 40", key="a3")

    if st.button("Verificar Amazon", key="b1"):
        try:
            res = check_amazon(amz1, amz2, amz3)
            st.success(res["status"] + " — " + res["motivo"]) if "Aceita" in res["status"] else st.error(res["status"] + " — " + res["motivo"])
        except Exception:
            st.error("⚠️ Entrada inválida. Preencha as três medidas corretamente.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Correios ----
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">📮 Correios</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc">Cada lado ≤ 100 cm e soma (altura + largura + comprimento) ≤ 200 cm.</div>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        c1 = st.text_input("Altura (cm)", value="", placeholder="ex.: 80", key="c1")
    with col5:
        c2 = st.text_input("Largura (cm)", value="", placeholder="ex.: 60", key="c2")
    with col6:
        c3 = st.text_input("Comprimento (cm)", value="", placeholder="ex.: 50", key="c3")

    if st.button("Verificar Correios", key="b2"):
        try:
            r = evaluate_correios(c1, c2, c3)
            st.success(r["status"] + " — " + r["motivo"]) if "Aceita" in r["status"] else st.error(r["status"] + " — " + r["motivo"])
        except Exception:
            st.error("⚠️ Entrada inválida. Preencha as medidas corretamente.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---- Mercado Livre ----
with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">📦 Mercado Livre</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc">Cada lado ≤ 200 cm, soma (altura + largura + comprimento) ≤ 300 cm e peso ≤ 50 kg.</div>', unsafe_allow_html=True)
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        ml1 = st.text_input("Altura (cm)", value="", placeholder="ex.: 100", key="m1")
    with col8:
        ml2 = st.text_input("Largura (cm)", value="", placeholder="ex.: 80", key="m2")
    with col9:
        ml3 = st.text_input("Comprimento (cm)", value="", placeholder="ex.: 60", key="m3")
    with col10:
        peso = st.text_input("Peso (kg)", value="", placeholder="ex.: 25", key="m4")

    if st.button("Verificar Mercado Livre", key="b3"):
        try:
            r = evaluate_ml(ml1, ml2, ml3, peso)
            st.success(r["status"] + " — " + r["motivo"]) if "Aceita" in r["status"] else st.error(r["status"] + " — " + r["motivo"])
        except Exception:
            st.error("⚠️ Entrada inválida. Preencha as medidas e o peso corretamente.")
    st.markdown('</div>', unsafe_allow_html=True)
