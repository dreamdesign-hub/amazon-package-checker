import streamlit as st

# --- Funções de cálculo ---

def verificar_amazon(dim1, dim2, dim3):
    lados = sorted([dim1, dim2, dim3], reverse=True)
    maior, meio, menor = lados
    total = maior + 2 * (meio + menor)
    if maior > 180:
        return "Não aceita — maior lado > 180 cm"
    elif total > 432:
        return "Não aceita — (maior + 2×(largura+altura)) > 432 cm"
    else:
        return "Aceita"

def verificar_correios(dim1, dim2, dim3):
    # Novo cálculo (antigo "Mercado Livre", renomeado p/ Correios)
    if dim1 > 100 or dim2 > 100 or dim3 > 100:
        return "Não aceita — algum lado > 100 cm"
    elif (dim1 + dim2 + dim3) > 200:
        return "Não aceita — soma dos lados > 200 cm"
    else:
        return "Aceita"

# --- Layout Streamlit ---

st.title("Verificação de Dimensões")

st.header("📦 Regras Amazon")
dim1_amz = st.number_input("Medida 1 (cm)", min_value=0.0, step=1.0, key="amz1")
dim2_amz = st.number_input("Medida 2 (cm)", min_value=0.0, step=1.0, key="amz2")
dim3_amz = st.number_input("Medida 3 (cm)", min_value=0.0, step=1.0, key="amz3")

if dim1_amz and dim2_amz and dim3_amz:
    resultado_amz = verificar_amazon(dim1_amz, dim2_amz, dim3_amz)
    st.subheader("Resultado Amazon")
    st.write(resultado_amz)

st.markdown("---")  # separador

st.header("📦 Regras Correios")
dim1_cor = st.number_input("Medida 1 (cm)", min_value=0.0, step=1.0, key="cor1")
dim2_cor = st.number_input("Medida 2 (cm)", min_value=0.0, step=1.0, key="cor2")
dim3_cor = st.number_input("Medida 3 (cm)", min_value=0.0, step=1.0, key="cor3")

if dim1_cor and dim2_cor and dim3_cor:
    resultado_cor = verificar_correios(dim1_cor, dim2_cor, dim3_cor)
    st.subheader("Resultado Correios")
    st.write(resultado_cor)
