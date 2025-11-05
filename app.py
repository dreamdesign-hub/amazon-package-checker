import re
import streamlit as st

# ===== CONFIGURAÇÃO =====
st.set_page_config(
    page_title="Teste de Dimensões — Amazon, Correios & Mercado Livre",
    page_icon="📦",
    layout="centered",
)

# Força o modo claro (neutraliza o tema do navegador)
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f9fafb; /* fundo cinza-claro */
        color: #111827 !important; /* texto escuro */
    }

    /* inputs */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
    }

    /* títulos e textos */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #111827 !important; /* texto quase preto */
    }

    /* caixas de regras */
    .rule-block {
        background: #ffffff;
        border-left: 4px solid #e5e7eb;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #111827 !important;
    }

    /* botões */
    .stButton>button {
        background-color: #2563eb;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #1e40af;
    }

    /* títulos de seção */
    .section-title {
        font-weight: 700;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ===== util =====
def _to_float(s):
    if s is None or str(s).strip() == "":
        raise ValueError("valor vazio")
    s = str(s).strip().replace(",", ".")
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

# ===== regras =====
def evaluate_amazon(maior, meio, menor):
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"total": total, "status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"total": total, "status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"total": total, "status": "Aceita", "motivo": ""}

def evaluate_correios(a, b, c):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    if any(x > 100 for x in lados):
        return {"soma": sum(lados), "status": "Não aceita", "motivo": f"um dos lados {max(lados):.2f} > 100 cm"}
    soma = sum(lados)
    if soma > 200:
        return {"soma": soma, "status": "Não aceita", "motivo": f"soma {soma:.2f} > 200 cm"}
    return {"soma": soma, "status": "Aceita", "motivo": ""}

def evaluate_ml(a, b, c, peso):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    soma = sum(lados)
    p = _to_float(peso)
    if any(x > 200 for x in lados):
        return {"status": "Não aceita", "motivo": f"um dos lados {max(lados):.2f} > 200 cm"}
    if soma > 300:
        return {"status": "Não aceita", "motivo": f"soma {soma:.2f} > 300 cm"}
    if p > 50:
        return {"status": "Não aceita", "motivo": f"peso {p:.2f} kg > 50 kg"}
    return {"status": "Aceita", "motivo": ""}

# ===== UI =====
st.title("📦 Teste de Dimensões — Amazon, Correios & Mercado Livre")
st.write("Verifique rapidamente se suas embalagens atendem às regras de envio de cada transportadora.")

# --- Amazon (cor: branco sobre azul-escuro visual) ---
st.markdown('<div class="section-title" style="color:#0f172a">Amazon</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="rule-block"><ul style="margin:0;padding-left:18px"><li>Fórmula: <b>maior + 2 × (largura + altura) ≤ 432 cm</b></li>'
    '<li>Maior lado ≤ <b>180 cm</b></li></ul></div>',
    unsafe_allow_html=True,
)

col_a1, col_a2, col_a3 = st.columns(3)
with col_a1:
    amz1 = st.text_input("Medida 1 (cm) - Amazon", value="", key="amz_m1")
with col_a2:
    amz2 = st.text_input("Medida 2 (cm) - Amazon", value="", key="amz_m2")
with col_a3:
    amz3 = st.text_input("Medida 3 (cm) - Amazon", value="", key="amz_m3")

if st.button("Verificar Amazon", key="btn_amz"):
    try:
        A, B, C = normalize_dims([amz1, amz2, amz3])
        res = evaluate_amazon(A, B, C)
        if res["status"] == "Aceita":
            st.success(f"✅ Aceita — total {res['total']:.2f} cm")
        else:
            st.error(f"❌ {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha corretamente as 3 medidas (ex.: 120, 50, 40).")

st.markdown("---")

# --- Correios (cor azul) ---
st.markdown('<div class="section-title" style="color:#0b63d6">Correios</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="rule-block"><ul style="margin:0;padding-left:18px"><li>Cada lado ≤ <b>100 cm</b></li>'
    '<li>Soma (altura + largura + comprimento) ≤ <b>200 cm</b></li></ul></div>',
    unsafe_allow_html=True,
)

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    co1 = st.text_input("Altura (cm) - Correios", value="", key="cor_m1")
with col_c2:
    co2 = st.text_input("Largura (cm) - Correios", value="", key="cor_m2")
with col_c3:
    co3 = st.text_input("Comprimento (cm) - Correios", value="", key="cor_m3")

if st.button("Verificar Correios", key="btn_cor"):
    try:
        res = evaluate_correios(co1, co2, co3)
        if res["status"] == "Aceita":
            st.success(f"✅ Aceita — soma {res['soma']:.2f} cm")
        else:
            st.error(f"❌ {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha corretamente as 3 medidas.")

st.markdown("---")

# --- Mercado Livre (cor amarelo) ---
st.markdown('<div class="section-title" style="color:#f7c600">Mercado Livre</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="rule-block"><ul style="margin:0;padding-left:18px"><li>Cada lado ≤ <b>200 cm</b></li>'
    '<li>Soma total (altura + largura + comprimento) ≤ <b>300 cm</b></li>'
    '<li>Peso máximo ≤ <b>50 kg</b></li></ul></div>',
    unsafe_allow_html=True,
)

col_m1, col_m2, col_m3, col_m4 = st.columns([1,1,1,1])
with col_m1:
    ml1 = st.text_input("Altura (cm) - ML", value="", key="ml_m1")
with col_m2:
    ml2 = st.text_input("Largura (cm) - ML", value="", key="ml_m2")
with col_m3:
    ml3 = st.text_input("Comprimento (cm) - ML", value="", key="ml_m3")
with col_m4:
    peso = st.text_input("Peso (kg) - ML", value="", key="ml_wt")

if st.button("Verificar Mercado Livre", key="btn_ml"):
    try:
        res = evaluate_ml(ml1, ml2, ml3, peso)
        if res["status"] == "Aceita":
            st.success("✅ Aceita — dentro dos limites")
        else:
            st.error(f"❌ {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as medidas e o peso corretamente.")
