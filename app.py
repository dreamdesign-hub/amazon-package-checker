# app.py — Streamlit simples (Medida 1/2/3 + Resultado)
import streamlit as st

st.set_page_config(page_title="Teste de Dimensões — Amazon", page_icon="📦", layout="centered")

st.title("Teste de Dimensões — Amazon")
st.write(
    "Informe **três medidas** em cm (qualquer ordem)."
)

# ---------- Entradas (iguais ao Gradio: três campos simples) ----------
col1, col2, col3 = st.columns(3)
with col1:
    m1 = st.number_input("Medida 1 (cm)", min_value=0.0, step=1.0, format="%.2f")
with col2:
    m2 = st.number_input("Medida 2 (cm)", min_value=0.0, step=1.0, format="%.2f")
with col3:
    m3 = st.number_input("Medida 3 (cm)", min_value=0.0, step=1.0, format="%.2f")

if st.button("Verificar"):
    try:
        # Normaliza (ordena) para identificar maior/meio/menor
        lados = sorted([float(m1), float(m2), float(m3)], reverse=True)
        maior, meio, menor = lados[0], lados[1], lados[2]
        total = maior + 2 * (meio + menor)

        # Resultado textual, no mesmo espírito do Gradio
        if maior > 180:
            resultado = f"❌ Não aceita — maior lado {maior:.2f} > 180 cm"
        elif total > 432:
            resultado = f"❌ Não aceita — total {total:.2f} > 432 cm"
        else:
            resultado = f"✅ Aceita — total {total:.2f}, maior lado {maior:.2f}"

        # Saída direta, sem cards/tabela
        st.subheader("Resultado")
        st.write(resultado)

    

    except Exception:
        st.error("Entrada inválida. Verifique os valores numéricos.")
