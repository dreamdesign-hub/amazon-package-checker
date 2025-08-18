# app.py — Streamlit somente modo simples (sem CSV, sem "ver cálculo")
import re
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon", page_icon="📦", layout="centered")

# ============ Regras e utilitários ============
def _to_float(s):
    if s is None:
        raise ValueError("valor vazio")
    s = str(s).strip()
    if s == "":
        raise ValueError("valor vazio")
    s = s.replace(",", ".")
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)  # remove milhar
    return float(s)

def normalize_dims(vals3):
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

def evaluate_box(maior, meio, menor):
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"total": total, "maior_lado": maior, "status": "Aceita", "motivo": ""}

def evaluate_three(m1, m2, m3):
    maior, meio, menor = normalize_dims([m1, m2, m3])
    r = evaluate_box(maior, meio, menor)
    r.update({"comprimento": maior, "largura": meio, "altura": menor})
    return r

# ============ UI ============
st.title("Teste de Dimensões — Amazon")
st.write(
    "Informe três medidas **em cm** (qualquer ordem). O app identifica o **maior** lado e calcula "
    "`maior + 2 × (largura + altura)`. Regras: **Total ≤ 432 cm**\n\n**Maior lado ≤ 180 cm**\n\n**Peso bruto ≤ 45kg**."
)

col1, col2, col3 = st.columns(3)
with col1:
    m1 = st.text_input("Medida 1 (cm)", value="", placeholder="ex.: 120")
with col2:
    m2 = st.text_input("Medida 2 (cm)", value="", placeholder="ex.: 50")
with col3:
    m3 = st.text_input("Medida 3 (cm)", value="", placeholder="ex.: 40")

if st.button("Verificar", type="primary"):
    try:
        res = evaluate_three(m1, m2, m3)
        maior, total = res["comprimento"], res["total"]

        if res["status"] == "Aceita":
            st.success(f"✅ Aceita — total {total:.2f}, maior lado {maior:.2f}")
        else:
            st.error(f"❌ Não aceita — {res['motivo']}")

    except Exception:
        st.error("Entrada inválida. Preencha as três medidas corretamente.")
