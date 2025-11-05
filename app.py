# app.py — Amazon, Correios e Mercado Livre — versão com layout aprimorado
import re
import streamlit as st

# ================= CONFIGURAÇÃO GERAL =================
st.set_page_config(
    page_title="Teste de Dimensões — Amazon, Correios & Mercado Livre",
    page_icon="📦",
    layout="centered"
)

# --- Estilo customizado ---
st.markdown("""
<style>
/* Fundo neutro */
[data-testid="stAppViewContainer"] {
    background-color: #f4f4f4;
}

/* Caixas e botões */
.stTextInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

button[kind="primary"] {
    background-color: #007bff !important;
    color: white !important;
    border-radius: 8px;
}

/* Títulos */
h1, h2, h3 {
    color: #222222 !important;
    font-weight: 700;
}

/* Cores das seções */
.amazon-title {
    color: #ffffff !important;
    background-color: #232f3e;
    padding: 8px 12px;
    border-radius: 8px;
}
.correios-title {
    color: #0046ad !important;
    font-weight: 700;
}
.ml-title {
    color: #f7c600 !important;
    font-weight: 700;
}

/* Regras em lista */
.rules {
    background-color: #ffffff;
    border-left: 4px solid #ddd;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 10px;
    font-size: 15px;
}
.rules ul {
    margin: 0;
    padding-left: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================= FUNÇÕES =================
def _to_float(s):
    if s is None or str(s).strip() == "":
        raise ValueError("valor vazio")
    s = str(s).strip().replace(",", ".")
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

# --- Amazon ---
def evaluate_amazon(maior, meio, menor):
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"total": total, "status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"total": total, "status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"total": total, "status": "Aceita", "motivo": ""}

# --- Correios ---
def evaluate_correios(a, b, c):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    if any(x > 100 for x in lados):
        return {"soma": sum(lados), "status": "Não aceita", "motivo": f"um dos lados {max(lados):.2f} > 100 cm"}
    soma = sum(lados)
    if soma > 200:
        return {"soma": soma, "status": "Não aceita", "motivo": f"soma {soma:.2f} > 200 cm"}
    return {"soma": soma, "status": "Aceita", "motivo": ""}

# --- Mercado Livre ---
def evaluate_ml(a, b, c, peso):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    soma = sum(lados)
    peso = _to_float(peso)

    if any(x > 200 for x in lados):
        return {"status": "Não aceita", "motivo": f"um dos lados {max(lados):.2f} > 200 cm"}
    if soma > 300:
        return {"status": "Não aceita", "motivo": f"soma {soma:.2f} > 300 cm"}
    if peso > 50:
        return {"status": "Não aceita", "motivo": f"peso {peso:.2f} kg > 50 kg"}
    return {"status": "Aceita", "motivo": ""}

# ================= INTERFACE =================
st.title("📦 Teste de Dimensões — Amazon, Correios & Mercado Livre")
st.markdown("Verifique rapidamente se suas embalagens atendem às regras de envio de cada transportadora.")

# ===== AMAZON =====
st.markdown("<h3 class='amazon-title'>Amazon</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="rules">
<ul>
<li>Fórmula: <b>maior + 2 × (largura + altura) ≤ 432 cm</b></li>
<li>Maior lado ≤ <b>180 cm</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1: a1 = st.text_input("Medida 1 (cm)", "")
with col2: a2 = st.text_input("Medida 2 (cm)", "")
with col3: a3 = st.text_input("Medida 3 (cm)", "")
if st.button("Verificar Amazon"):
    try:
        A, B, C = normalize_dims([a1, a2, a3])
        res = evaluate_amazon(A, B, C)
        if res["status"] == "Aceita":
            st.success(f"✅ Aceita — total {res['total']:.2f} cm")
        else:
            st.error(f"❌ {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha corretamente.")

st.markdown("---")

# ===== CORREIOS =====
st.markdown("<h3 class='correios-title'>📮 Correios</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="rules">
<ul>
<li>Cada lado ≤ <b>100 cm</b></li>
<li>Soma (altura + largura + comprimento) ≤ <b>200 cm</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: co1 = st.text_input("Altura (cm)", "")
with c2: co2 = st.text_input("Largura (cm)", "")
with c3: co3 = st.text_input("Comprimento (cm)", "")
if st.button("Verificar Correios"):
    try:
        r = evaluate_correios(co1, co2, co3)
        if r["status"] == "Aceita":
            st.success(f"✅ Aceita — soma {r['soma']:.2f} cm")
        else:
            st.error(f"❌ {r['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha corretamente.")

st.markdown("---")

# ===== MERCADO LIVRE =====
st.markdown("<h3 class='ml-title'>🟡 Mercado Livre</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="rules">
<ul>
<li>Cada lado ≤ <b>200 cm</b></li>
<li>Soma total (altura + largura + comprimento) ≤ <b>300 cm</b></li>
<li>Peso máximo: <b>50 kg</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1: ml1 = st.text_input("Altura (cm)", "")
with m2: ml2 = st.text_input("Largura (cm)", "")
with m3: ml3 = st.text_input("Comprimento (cm)", "")
peso = st.text_input("Peso (kg)", "")

if st.button("Verificar Mercado Livre"):
    try:
        r = evaluate_ml(ml1, ml2, ml3, peso)
        if r["status"] == "Aceita":
            st.success("✅ Aceita — dentro dos limites")
        else:
            st.error(f"❌ {r['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha corretamente.")
