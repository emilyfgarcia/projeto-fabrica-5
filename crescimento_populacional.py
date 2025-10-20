import streamlit as st
import pandas as pd

# 🎨 Configuração da página
st.set_page_config(
    page_title="🌍 Crescimento Populacional — País A vs País B",
    page_icon="🌎",
    layout="centered"
)

# 🏠 Cabeçalho
st.title("🌍 Crescimento Populacional — País A vs País B")
st.caption("Mini-projeto educativo — crescimento composto, laço while e visualização com Pandas + Streamlit")

st.divider()

# 🎯 Introdução
st.write("""
Este simulador estima **em quantos anos a população do País A ultrapassa (ou iguala) a do País B**, 
mantendo taxas de crescimento anuais constantes.  
Você pode usar os valores padrão do enunciado ou testar seus próprios cenários.
""")

# 🧮 Parâmetros
usar_padrao = st.radio(
    "Deseja usar os valores padrão do enunciado?",
    options=["Sim", "Não"],
    horizontal=True
)

if usar_padrao == "Sim":
    pop_a_inicial = 80000
    taxa_a = 3.0
    pop_b_inicial = 200000
    taxa_b = 1.5
else:
    st.subheader("✏️ Personalize os dados")
    col1, col2 = st.columns(2)
    with col1:
        pop_a_inicial = st.number_input("População inicial do País A", min_value=1, value=80000, step=1000)
        taxa_a = st.number_input("Taxa de crescimento anual do País A (%)", min_value=0.0, value=3.0, step=0.1)
    with col2:
        pop_b_inicial = st.number_input("População inicial do País B", min_value=1, value=200000, step=1000)
        taxa_b = st.number_input("Taxa de crescimento anual do País B (%)", min_value=0.0, value=1.5, step=0.1)

st.divider()

# 🚀 Simulação
if st.button("▶️ Calcular crescimento"):
    anos = 0
    pop_a = pop_a_inicial
    pop_b = pop_b_inicial
    historico = []

    # Evita loops infinitos
    max_anos = 500

    # Simulação anual
    while pop_a < pop_b and anos < max_anos:
        anos += 1
        pop_a += pop_a * (taxa_a / 100)
        pop_b += pop_b * (taxa_b / 100)
        historico.append({
            "Ano": anos,
            "População País A": int(pop_a),
            "População País B": int(pop_b),
            "Diferença (B - A)": int(pop_b - pop_a)
        })

    df = pd.DataFrame(historico)

    # 🧠 Verificações
    if anos >= max_anos and pop_a < pop_b:
        st.error("🚫 O País A nunca ultrapassa o País B com essas taxas de crescimento.")
    else:
        st.success(f"✅ Após **{anos} anos**, o País A ultrapassa (ou iguala) o País B.")

        # 📊 Resultados finais
        col1, col2, col3 = st.columns(3)
        col1.metric("Anos até ultrapassar", anos)
        col2.metric("População final País A", f"{int(pop_a):,}".replace(",", "."))
        col3.metric("População final País B", f"{int(pop_b):,}".replace(",", "."))

        # 📈 Gráfico de evolução
        st.subheader("📈 Evolução Populacional")
        st.line_chart(df.set_index("Ano")[["População País A", "População País B"]])

        # 📋 Tabela ano a ano
        st.subheader("📅 Tabela de Crescimento Ano a Ano")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # 💾 Exportar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📂 Baixar histórico em CSV",
            data=csv,
            file_name="crescimento_populacional.csv",
            mime="text/csv"
        )

        # 💬 Observação
        st.info("Observação: Os cálculos são aproximados e consideram crescimento composto ano a ano (sem frações de habitantes).")

else:
    st.info("Clique em **Calcular crescimento** para iniciar a simulação.")
