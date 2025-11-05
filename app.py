# app.py — Amazon + Correios + Mercado Livre — simples, sem CSV, entradas vazias
import re
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon, Correios & Mercado Livre", page_icon="📦", layout="centered")

# ============ Utilitários ============
def _to_float(s):
    if s is None:
        raise ValueError("valor vazio")
    s = str(s).strip()
    if s == "":
        raise ValueError("valor vazio")
    s = s.replace(",", ".")
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    """Ordena (maior, meio, menor)."""
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

# ============ Regras — Amazon ============
def evaluate_amazon(maior, meio, menor):
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"status": "Aceita", "motivo": ""}

def check_amazon(m1, m2, m3):
    maior, meio, menor = normalize_dims([m1, m2, m3])
    return evaluate_amazon(maior, meio, menor)

# ============ Regras — Correios ============
def evaluate_correios(a, b, c):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    if any(x > 100 for x in lados):
        maior_excesso = max(lados)
        return {"status": "Não aceita", "motivo": f"um dos lados {maior_excesso:.2f} > 100 cm"}
    soma = sum(lados)
    if soma > 200:
        return {"status": "Não aceita", "motivo": f"soma {soma:.2f} > 200 cm"}
    return {"status": "Aceita", "motivo": ""}

# ============ Regras — Mercado Livre ============
def evaluate_ml(a, b, c, peso):
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    p = _to_float(peso)
    if any(x > 200 for x in lados):
        maior_excesso = max(lados)
        return {"status": "Não aceita", "motivo": f"um dos lados {maior_excesso:.2f} > 200 cm"}
    soma = sum(lados)
    if soma > 300:
        return {"status": "Não aceita", "motivo": f"soma {soma:.2f} > 300 cm"}
    if p > 50:
        return {"status": "Não aceita", "motivo": f"peso {p:.2f} kg > 50 kg"}
    return {"status": "Aceita", "motivo": ""}

# ===================== UI =====================
st.title("Teste de Dimensões — Amazon, Correios & Mercado Livre")

# ---- Seção Amazon ----
st.subheader("Amazon")
st.markdown("Regras:/n**maior + 2 × (largura + altura) ≤ 432 cm**/n**maior lado ≤ 180 cm**.")

col1, col2, col3 = st.columns(3)
with col1:
    amz1 = st.text_input("Medida 1 (cm)", value="", placeholder="ex.: 120")
with col2:
    amz2 = st.text_input("Medida 2 (cm)", value="", placeholder="ex.: 50")
with col3:
    amz3 = st.text_input("Medida 3 (cm)", value="", placeholder="ex.: 40")

if st.button("Verificar Amazon", type="primary"):
    try:
        res = check_amazon(amz1, amz2, amz3)
        if res["status"] == "Aceita":
            st.success("✅ Aceita — dentro das regras da Amazon")
        else:
            st.error(f"❌ Não aceita — {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as três medidas corretamente.")

st.markdown("---")

# ---- Seção Correios ----
st.subheader("Correios")
st.markdown("Regras: **cada lado ≤ 100 cm**, **soma (altura + largura + comprimento) ≤ 200 cm**.")

col4, col5, col6 = st.columns(3)
with col4:
    c1 = st.text_input("Altura (cm)", value="", placeholder="ex.: 80")
with col5:
    c2 = st.text_input("Largura (cm)", value="", placeholder="ex.: 60")
with col6:
    c3 = st.text_input("Comprimento (cm)", value="", placeholder="ex.: 50")

if st.button("Verificar Correios"):
    try:
        r = evaluate_correios(c1, c2, c3)
        if r["status"] == "Aceita":
            st.success("✅ Aceita — dentro das regras dos Correios")
        else:
            st.error(f"❌ Não aceita — {r['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as três medidas corretamente.")

st.markdown("---")

# ---- Seção Mercado Livre ----
st.subheader("Mercado Livre")
st.markdown("Regras: **cada lado ≤ 200 cm**, **soma (altura + largura + comprimento) ≤ 300 cm**, **peso ≤ 50 kg**.")

col7, col8, col9, col10 = st.columns(4)
with col7:
    ml1 = st.text_input("Altura (cm)", value="", placeholder="ex.: 100")
with col8:
    ml2 = st.text_input("Largura (cm)", value="", placeholder="ex.: 80")
with col9:
    ml3 = st.text_input("Comprimento (cm)", value="", placeholder="ex.: 60")
with col10:
    peso = st.text_input("Peso (kg)", value="", placeholder="ex.: 25")

if st.button("Verificar Mercado Livre"):
    try:
        r = evaluate_ml(ml1, ml2, ml3, peso)
        if r["status"] == "Aceita":
            st.success("✅ Aceita — dentro das regras do Mercado Livre")
        else:
            st.error(f"❌ Não aceita — {r['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as medidas e o peso corretamente.")
