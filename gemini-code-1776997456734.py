import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import data, analysis, strategy

st.set_page_config(page_title="Aviator Analytics", layout="wide")
data.init_db()

st.warning("⚠️ O jogo é baseado em aleatoriedade (RNG). Use apenas para análise e controle de risco.")

with st.sidebar:
    st.header("📥 Entrada de Dados")
    with st.form("manual"):
        new_mult = st.number_input("Multiplicador", min_value=1.0, step=0.01)
        if st.form_submit_button("Registrar"):
            data.add_multiplier(new_mult)
            st.rerun()

df = data.get_data()
if df.empty:
    st.info("Adicione dados para começar.")
    st.stop()

tab1, tab2 = st.tabs(["📊 Estatísticas", "📈 Simulação"])

with tab1:
    stats = analysis.get_basic_stats(df)
    st.metric("Média", f"{stats['Média']:.2f}x")
    st.plotly_chart(px.line(df.tail(50), x='id', y='multiplier', title="Tendência Recente"))

with tab2:
    banca = st.number_input("Banca", value=100.0)
    alvo = st.slider("Alvo (Cashout)", 1.1, 5.0, 2.0)
    if st.button("Simular"):
        res = strategy.simulate_strategy(df, banca, 5.0, alvo, 0, banca*5, 100)
        st.write(f"Resultado Final: ${res['Saldo Final']}")
        st.line_chart(res['Evolução'])