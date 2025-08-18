# app.py — Streamlit simples (Medida 1/2/3 + Resultado) com CSV opcional e download
import re
import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon", page_icon="📦", layout="centered")

# ============ Regras e utilitários ============
def _to_float(s):
    """Converte string/num para float aceitando vírgula decimal e removendo milhar com ponto."""
    if s is None:
        raise ValueError("valor vazio")
    s = str(s).strip().replace(",", ".")
    # remove milhar com ponto quando seguido por 3 dígitos: 1.234,56 -> 1234.56
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def normalize_dims(vals3):
    """Ordena (maior, meio, menor)."""
    a, b, c = sorted([_to_float(x) for x in vals3], reverse=True)
    return a, b, c

def evaluate_box(maior, meio, menor):
    """Retorna dict com total, maior_lado e status/motivo."""
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"maior lado {maior:.2f} > 180 cm"}
    if total > 432:
        return {"total": total, "maior_lado": maior, "status": "Não aceita", "motivo": f"total {total:.2f} > 432 cm"}
    return {"total": total, "maior_lado": maior, "status": "Aceita", "motivo": ""}

def evaluate_three(m1, m2, m3):
    """Entrada de 3 números/strings -> avaliação + lados ordenados."""
    maior, meio, menor = normalize_dims([m1, m2, m3])
    r = evaluate_box(maior, meio, menor)
    r.update({"comprimento": maior, "largura": meio, "altura": menor})
    return r

@st.cache_data(show_spinner=False)
def read_csv_cached(file, sep):
    return pd.read_csv(file, sep=sep)

def evaluate_df(df, cols):
    """Avalia um DataFrame com 3 colunas (strings ou números)."""
    rows = []
    for _, row in df.iterrows():
        try:
            maior, meio, menor = normalize_dims([row[cols[0]], row[cols[1]], row[cols[2]]])
            r = evaluate_box(maior, meio, menor)
            rows.append({
                "Medida 1": row[cols[0]],
                "Medida 2": row[cols[1]],
                "Medida 3": row[cols[2]],
                "Comprimento (maior)": maior,
                "Largura (2º)": meio,
                "Altura (menor)": menor,
                "Total (cm)": r["total"],
                "Maior lado (cm)": r["maior_lado"],
                "Resultado": r["status"],
                "Motivo": r["motivo"]
            })
        except Exception as e:
            rows.append({
                "Medida 1": row[cols[0]] if cols[0] in df.columns else None,
                "Medida 2": row[cols[1]] if cols[1] in df.columns else None,
                "Medida 3": row[cols[2]] if cols[2] in df.columns else None,
                "Comprimento (maior)": None,
                "Largura (2º)": None,
                "Altura (menor)": None,
                "Total (cm)": None,
                "Maior lado (cm)": None,
                "Resultado": "Erro",
                "Motivo": str(e)
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
        m1 = st.number_input("Medida 1 (cm)", min_value=0.0, step=1.0, format="%.2f")
    with col2:
        m2 = st.number_input("Medida 2 (cm)", min_value=0.0, step=1.0, format="%.2f")
    with col3:
        m3 = st.number_input("Medida 3 (cm)", min_value=0.0, step=1.0, format="%.2f")

    if st.button("Verificar", type="primary"):
        try:
            res = evaluate_three(m1, m2, m3)
            maior, meio, menor = res["comprimento"], res["largura"], res["altura"]
            total = res["total"]

            # Saída textual simples (estilo Gradio)
            if res["status"] == "Aceita":
                st.success(f"✅ Aceita — total {total:.2f}, maior lado {maior:.2f}")
            else:
                st.error(f"❌ Não aceita — {res['motivo']}")

            with st.expander("Ver cálculo (opcional)"):
                st.markdown(
                    f"- Ordenado (C × L × A): **{maior:.2f} × {meio:.2f} × {menor:.2f}** cm\n"
                    f"- Cálculo: `{maior:.2f} + 2 × ({meio:.2f} + {menor:.2f}) = {total:.2f} cm`\n"
                    f"- Regras: total ≤ 432 cm | maior lado ≤ 180 cm"
                )

            # Download (linha única)
            df_one = pd.DataFrame([{
                "Medida 1": m1, "Medida 2": m2, "Medida 3": m3,
                "Comprimento (maior)": maior, "Largura (2º)": meio, "Altura (menor)": menor,
                "Total (cm)": total, "Maior lado (cm)": res["maior_lado"],
                "Resultado": res["status"], "Motivo": res["motivo"]
            }])
            st.download_button(
                "Baixar resultado (CSV)",
                df_one.to_csv(index=False).encode("utf-8"),
                file_name="resultado_dimensoes.csv",
                mime="text/csv"
            )

        except Exception:
            st.error("Entrada inválida. Verifique os valores.")

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

            # Por padrão, usa as 3 primeiras colunas
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
