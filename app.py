# app.py — Streamlit simples (sem "ver cálculo" e sem download na aba simples)
import re
import pandas as pd
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

@st.cache_data(show_spinner=False)
def read_csv_cached(file, sep):
    return pd.read_csv(file, sep=sep)

def evaluate_df(df, cols):
    rows = []
    for _, row in df.iterrows():
        try:
            maior, meio, menor = normalize_dims([row[cols[0]], row[cols[1]], row[cols[2]]])
            r = evaluate_box(maior, meio, menor)
            rows.append({
                "Medida 1": row[cols[0]], "Medida 2": row[cols[1]], "Medida 3": row[cols[2]],
                "Comprimento (maior)": maior, "Largura (2º)": meio, "Altura (menor)": menor,
                "Total (cm)": r["total"], "Maior lado (cm)": r["maior_lado"],
                "Resultado": r["status"], "Motivo": r["motivo"]
            })
        except Exception as e:
            rows.append({
                "Medida 1": row[cols[0]], "Medida 2": row[cols[1]], "Medida 3": row[cols[2]],
                "Comprimento (maior)": None, "Largura (2º)": None, "Altura (menor)": None,
                "Total (cm)": None, "Maior lado (cm)": None,
                "Resultado": "Erro", "Motivo": str(e)
            })
    return pd.DataFrame(rows)

# ============ UI ============
st.title("Teste de Dimensões — Amazon")
st.write(
    "Informe três medidas **em cm** (qualquer ordem). O app identifica o **maior** lado e calcula "
    "`maior + 2 × (largura + altura)`. Regras: **total ≤ 432 cm** e **maior lado ≤ 180 cm**."
)

tab1, tab2 = st.tabs(["Simples (3 medidas)", "CSV (opcional)"])

# ---- Aba 1: Simples ----
with tab1:
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

# ---- Aba 2: CSV ----
with tab2:
    st.write("Envie um **CSV** com **3 colunas** (quaisquer nomes) correspondendo às três medidas.")
    up = st.file_uploader("Arquivo CSV", type=["csv"])
    sep = st.selectbox("Separador", [",", ";", "\t", "|"], index=0)
    if up and st.button("Avaliar CSV", type="primary"):
        try:
            df_in = read_csv_cached(up, sep=sep)
            st.caption("Prévia do arquivo")
            st.dataframe(df_in.head())

            cols = list(df_in.columns[:3])
            st.caption(f"Usando colunas: {cols}")
            df_out = evaluate_df(df_in, cols)
            st.success("Avaliação concluída.")
            st.dataframe(df_out)

            st.download_button(
                "Baixar resultados (CSV)",
                df_out.to_csv(index=False).encode("utf-8"),
                file_name="resultados_dimensoes.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Erro ao processar CSV: {e}")
