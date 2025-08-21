# app.py — Amazon + Mercado Livre (Leve) — simples, sem CSV, entradas vazias
import re
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon & Mercado Livre", page_icon="📦", layout="centered")

# ============ Utilitários ============
def _to_float(s):
    if s is None:
        raise ValueError("valor vazio")
    s = str(s).strip()
    if s == "":
        raise ValueError("valor vazio")
    s = s.replace(",", ".")
    # remove milhar com ponto quando seguido por 3 dígitos: 1.234,56 -> 1234.56
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    """Ordena (maior, meio, menor)."""
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

# ============ Regras — Amazon ============
def evaluate_amazon(maior, meio, menor):
    """
    Amazon:
      total = maior + 2*(meio + menor)
      Aceita se total <= 432 e maior <= 180
    """
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"total": total, "maior_lado": maior, "status": "Aceita", "motivo": ""}

def check_amazon(m1, m2, m3):
    maior, meio, menor = normalize_dims([m1, m2, m3])
    r = evaluate_amazon(maior, meio, menor)
    r.update({"comprimento": maior, "largura": meio, "altura": menor})
    return r

# ============ Regras — Mercado Livre (Leve) ============
def evaluate_ml(a, b, c):
    """
    Mercado Livre — Leve:
      - Cada lado (altura, largura, comprimento) <= 100 cm
      - Soma dos 3 lados (a+b+c) <= 200 cm
      * Não importa a ordem; NÃO reordena por maior/meio/menor
    """
    lados = [_to_float(a), _to_float(b), _to_float(c)]
    # Regras individuais
    if any(x > 100 for x in lados):
        maior_excesso = max(lados)
        return {
            "soma": sum(lados),
            "status": "Não aceita",
            "motivo": f"um dos lados {maior_excesso:.2f} > 100 cm"
        }
    # Regra da soma
    soma = sum(lados)
    if soma > 200:
        return {"soma": soma, "status": "Não aceita", "motivo": f"soma {soma:.2f} > 200 cm"}
    return {"soma": soma, "status": "Aceita", "motivo": ""}

# ===================== UI =====================
st.title("Teste de Dimensões — Amazon & Mercado Livre")

st.markdown(
    "**Amazon**: informe 3 medidas em cm (qualquer ordem). O app identifica o maior lado e calcula "
    "`maior + 2 × (largura + altura)`. Regras: **total ≤ 432** e **maior lado ≤ 180**."
)

# ---- Seção 1: Amazon ----
st.subheader("Amazon")
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
            st.success(f"✅ Aceita — total {res['total']:.2f}, maior lado {res['maior_lado']:.2f}")
        else:
            st.error(f"❌ Não aceita — {res['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as três medidas corretamente (números, vírgula ou ponto para decimais).")

st.markdown("---")

# ---- Seção 2: Mercado Livre (Leve) ----
st.subheader("Mercado Livre (Leve)")
st.markdown(
    "Regras: **cada lado ≤ 100 cm** e **soma (altura + largura + comprimento) ≤ 200 cm**."
)

col4, col5, col6 = st.columns(3)
with col4:
    ml1 = st.text_input("Altura (cm)", value="", placeholder="ex.: 80")
with col5:
    ml2 = st.text_input("Largura (cm)", value="", placeholder="ex.: 60")
with col6:
    ml3 = st.text_input("Comprimento (cm)", value="", placeholder="ex.: 50")

if st.button("Verificar Mercado Livre"):
    try:
        r = evaluate_ml(ml1, ml2, ml3)
        if r["status"] == "Aceita":
            st.success(f"✅ Aceita — soma {r['soma']:.2f} cm (todos os lados ≤ 100 cm)")
        else:
            st.error(f"❌ Não aceita — {r['motivo']}")
    except Exception:
        st.error("Entrada inválida. Preencha as três medidas corretamente (números, vírgula ou ponto para decimais).")
