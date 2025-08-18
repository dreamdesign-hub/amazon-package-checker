# app.py
# 📦 Amazon Package Checker — Streamlit (manual + CSV + cards + KPIs)
import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon", page_icon="📦", layout="wide")

# ---------- Utilidades ----------
def _to_float(s):
    """Converte string para float aceitando vírgula decimal e remove milhar."""
    if s is None:
        raise ValueError("valor vazio")
    s = str(s).strip().replace(",", ".")
    # remove milhar com ponto quando seguido por 3 dígitos: 1.234,56 -> 1234.56
    s = re.sub(r"(?<=\d)\.(?=\d{3}(\D|$))", "", s)
    return float(s)

def parse_dims_any(text_or_list):
    """
    Recebe string "120x50x40" / "120×50×40" / "120 50 40" / "120;50;40"
    ou lista/tupla [120, 50, 40]; retorna 3 floats.
    """
    if isinstance(text_or_list, (list, tuple, pd.Series)):
        vals = [_to_float(v) for v in text_or_list]
    else:
        parts = re.split(r"[xX×,; ]+", str(text_or_list).strip())
        parts = [p for p in parts if p != ""]
        if len(parts) != 3:
            raise ValueError(f"Informe exatamente 3 dimensões. Recebido: {text_or_list!r}")
        vals = [_to_float(p) for p in parts]
    return vals

def normalize_dims(dims3):
    """Ordena (maior, meio, menor)."""
    a, b, c = sorted([_to_float(x) for x in dims3], reverse=True)
    return a, b, c

def evaluate_box(L, W, H):
    """
    Regras:
      - total = L + 2*(W + H)
      - Aceita se total <= 432 e L <= 180
    """
    total = L + 2*(W + H)
    if L > 180:
        return {"comprimento": L, "largura": W, "altura": H, "total": total,
                "maior_lado": L, "status": "Não aceita", "motivo": "maior lado > 180 cm"}
    if total > 432:
        return {"comprimento": L, "largura": W, "altura": H, "total": total,
                "maior_lado": L, "status": "Não aceita", "motivo": "(maior + 2×(largura+altura)) > 432 cm"}
    return {"comprimento": L, "largura": W, "altura": H, "total": total,
            "maior_lado": L, "status": "Aceita", "motivo": ""}

def evaluate_from_any(x):
    L, W, H = normalize_dims(parse_dims_any(x))
    return evaluate_box(L, W, H)

def _fmt_num(x):
    if x is None or pd.isna(x):
        return ""
    # arredonda pra ficar limpo
    return f"{x:,.0f}".replace(",", ".")

# ---------- Header ----------
st.title("Teste de Dimensões — Amazon")
st.write(
    "Informe as 3 medidas **em cm** (qualquer ordem). O app identifica o maior, calcula "
    "`maior + 2 × (largura + altura)` e aplica as regras: **total ≤ 432 cm** e **maior lado ≤ 180 cm**."
)

# ---------- Sidebar ----------
st.sidebar.header("Entrada")
mode = st.sidebar.radio("Modo", ["Manual (várias linhas)", "Upload CSV"], index=0)

# ---------- KPIs/top summary ----------
def show_kpis(df):
    total = len(df)
    aceitas = (df["status"] == "Aceita").sum()
    reprov = (df["status"] == "Não aceita").sum()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de caixas", total)
    col2.metric("Aceitas", aceitas)
    col3.metric("Não aceitas", reprov)
    col4.metric("% Aceitas", f"{(aceitas/total*100):.1f}%" if total else "0.0%")

# ---------- Cards renderer ----------
def cards(df):
    # cores por status
    style = {
        "Aceita": ("✅ Aceita", "#16a34a", "#dcfce7"),          # label, fg, bg
        "Não aceita": ("❌ Não aceita", "#b91c1c", "#fee2e2"),
        "Erro": ("⚠️ Erro", "#92400e", "#fef3c7"),
    }
    # grid responsivo simples com markdown/HTML
    for i in range(0, len(df), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j >= len(df):
                continue
            r = df.iloc[i + j]
            label, fg, bg = style.get(r["status"], (r["status"], "#334155", "#e2e8f0"))
            motivo = (r["motivo"] or "").replace(">", "&gt;")
            with col:
                st.markdown(
                    f"""
<div style="border:1px solid #e5e7eb; border-radius:16px; padding:14px; background:#ffffff; min-height:170px;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:.5rem;">
    <div style="font-weight:700; color:#334155;">Caixa</div>
    <div style="background:{bg}; color:{fg}; padding:.25rem .6rem; border-radius:999px; font-weight:700;">{label}</div>
  </div>
  <div style="display:flex; gap:10px; flex-wrap:wrap; margin:.25rem 0 .5rem;">
    <span style="background:#e5e7eb;color:#1f2937;padding:.25rem .6rem;border-radius:999px;">Compr.: {_fmt_num(r['comprimento'])} cm</span>
    <span style="background:#e5e7eb;color:#1f2937;padding:.25rem .6rem;border-radius:999px;">Larg.: {_fmt_num(r['largura'])} cm</span>
    <span style="background:#e5e7eb;color:#1f2937;padding:.25rem .6rem;border-radius:999px;">Alt.: {_fmt_num(r['altura'])} cm</span>
  </div>
  <div style="display:flex; gap:10px; flex-wrap:wrap;">
    <span style="background:#f1f5f9;color:#1f2937;padding:.25rem .6rem;border-radius:999px;">Total: {_fmt_num(r['total'])} cm</span>
    <span style="background:#f1f5f9;color:#1f2937;padding:.25rem .6rem;border-radius:999px;">Maior lado: {_fmt_num(r['maior_lado'])} cm</span>
  </div>
  {f'<div style="margin-top:.75rem;color:#991b1b;">Motivo: {motivo}</div>' if r["status"]!="Aceita" and motivo else ""}
</div>
""",
                    unsafe_allow_html=True,
                )

# ---------- Processamento conforme modo ----------
if mode == "Manual (várias linhas)":
    default_text = "120x50x40\n160x70x50\n200x50x30\n180x100x70"
    txt = st.text_area("Cole suas caixas, uma por linha", value=default_text, height=160)
    if st.button("Avaliar"):
        linhas = [ln.strip() for ln in txt.splitlines() if ln.strip()]
        rows = []
        for ln in linhas:
            try:
                rows.append(evaluate_from_any(ln))
            except Exception as e:
                rows.append({"comprimento": None, "largura": None, "altura": None,
                             "total": None, "maior_lado": None, "status": "Erro", "motivo": str(e)})
        df = pd.DataFrame(rows)
        show_kpis(df)
        st.markdown("### Cards")
        cards(df)
        st.markdown("### Tabela")
        st.dataframe(df)

else:
    up = st.file_uploader("Envie um CSV com 3 colunas (qualquer nome)", type=["csv"])
    sep = st.selectbox("Separador", [",", ";", "\t", "|"], index=0)
    if up and st.button("Avaliar CSV"):
        df_in = pd.read_csv(up, sep=sep)
        st.write("Prévia do arquivo:")
        st.dataframe(df_in.head())
        # Tenta usar as 3 primeiras colunas
        cols = list(df_in.columns[:3])
        rows = []
        for _, row in df_in.iterrows():
            try:
                vals = [row[cols[0]], row[cols[1]], row[cols[2]]]
                L, W, H = normalize_dims(vals)
                rows.append(evaluate_box(L, W, H))
            except Exception as e:
                rows.append({"comprimento": None, "largura": None, "altura": None,
                             "total": None, "maior_lado": None, "status": "Erro", "motivo": str(e)})
        df = pd.DataFrame(rows)
        show_kpis(df)
        st.markdown("### Cards")
        cards(df)
        st.markdown("### Tabela")
        st.dataframe(df)

# ---------- Testes rápidos (opcional) ----------
with st.expander("Testes (sanity check)"):
    t1 = evaluate_from_any("120x50x40")
    t2 = evaluate_from_any("160x70x50")
    t3 = evaluate_from_any("200x50x30")
    st.write("Exemplo 1 (aceita):", t1)
    st.write("Exemplo 2 (aceita):", t2)
    st.write("Maior > 180 (não aceita):", t3)
