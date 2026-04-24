import streamlit as st
import pandas as pd
from datetime import datetime
from services import add_transaction, get_transactions, delete_transaction

def dashboard(user_id):
    st.title("💰 Meu Financeiro")

    df = get_transactions(user_id)

    if not df.empty:
        receitas = df[df["type"] == "Receita"]["value"].sum()
        despesas = df[df["type"] == "Despesa"]["value"].sum()
        saldo = receitas - despesas

        col1, col2, col3 = st.columns(3)

        col1.metric("Receitas", f"R$ {receitas:.2f}")
        col2.metric("Despesas", f"R$ {despesas:.2f}")
        col3.metric("Saldo", f"R$ {saldo:.2f}")

        st.subheader("📊 Por categoria")
        st.bar_chart(df.groupby("category")["value"].sum())

        st.subheader("📅 Evolução")
        df["date"] = pd.to_datetime(df["date"])
        st.line_chart(df.groupby("date")["value"].sum())

        st.dataframe(df)
    else:
        st.info("Sem dados")

def add_screen(user_id):
    st.subheader("Nova movimentação")

    name = st.text_input("Descrição")
    value = st.number_input("Valor", min_value=0.0)
    category = st.selectbox("Categoria", ["Alimentação", "Salário", "Transporte", "Outros"])
    type_ = st.selectbox("Tipo", ["Receita", "Despesa"])
    date = st.date_input("Data", value=datetime.today())

    if st.button("Salvar"):
        add_transaction(user_id, name, value, category, type_, str(date))
        st.success("Salvo!")
        st.rerun()

def manage_screen(user_id):
    df = get_transactions(user_id)

    for _, row in df.iterrows():
        col1, col2 = st.columns([4, 1])

        col1.write(f"{row['name']} - R$ {row['value']} ({row['type']})")

        if col2.button("Excluir", key=row['id']):
            delete_transaction(row['id'])
            st.rerun()