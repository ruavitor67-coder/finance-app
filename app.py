import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client, Client

# =========================
# 🔑 CONFIGURAÇÃO SUPABASE
# =========================
SUPABASE_URL = "https://gpmhnytpcbypqdocuxtq.supabase.co"
SUPABASE_KEY = "sb_publishable_YwzbLWkqevBoT-yYarCIJQ_fRZxB6VD"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Finance App", layout="centered")

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# FUNÇÕES
# =========================
def get_data(user_id):
    try:
        response = supabase.table("transactions") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("date", desc=True) \
            .execute()

        return pd.DataFrame(response.data)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()

def add_data(user_id, name, value, category, type_, dt):
    try:
        supabase.table("transactions").insert({
            "user_id": user_id,
            "name": name,
            "value": float(value),
            "category": category,
            "type": type_,
            "date": str(dt)
        }).execute()

        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def delete_data(row_id):
    try:
        supabase.table("transactions") \
            .delete() \
            .eq("id", row_id) \
            .execute()
        return True
    except Exception as e:
        st.error(f"Erro ao excluir: {e}")
        return False

# =========================
# LOGIN / REGISTRO
# =========================
if st.session_state.user is None:

    st.title("🔐 Login")

    tab1, tab2 = st.tabs(["Entrar", "Registrar"])

    # LOGIN
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if res.user:
                    st.session_state.user = res.user
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")

            except Exception as e:
                st.error(f"Erro no login: {e}")

    # REGISTRO
    with tab2:
        email2 = st.text_input("Novo Email")
        password2 = st.text_input("Nova Senha", type="password")

        if st.button("Criar conta"):
            try:
                supabase.auth.sign_up({
                    "email": email2,
                    "password": password2
                })
                st.success("Conta criada! Agora faça login.")
            except Exception as e:
                st.error(f"Erro ao registrar: {e}")

# =========================
# APP LOGADO
# =========================
else:

    user_id = st.session_state.user.id

    st.sidebar.title("Menu")

    if st.sidebar.button("Sair"):
        st.session_state.user = None
        st.rerun()

    menu = st.sidebar.radio("Navegação", ["Dashboard", "Adicionar", "Gerenciar"])

    # =========================
    # DASHBOARD
    # =========================
    if menu == "Dashboard":
        st.title("💰 Meu Financeiro")

        df = get_data(user_id)

        if not df.empty:

            receitas = df[df["type"] == "Receita"]["value"].sum()
            despesas = df[df["type"] == "Despesa"]["value"].sum()
            saldo = receitas - despesas

            col1, col2, col3 = st.columns(3)

            col1.metric("Receitas", f"R$ {receitas:.2f}")
            col2.metric("Despesas", f"R$ {despesas:.2f}")
            col3.metric("Saldo", f"R$ {saldo:.2f}")

            # GRÁFICO CATEGORIA
            st.subheader("📊 Por Categoria")
            st.bar_chart(df.groupby("category")["value"].sum())

            # GRÁFICO TEMPO
            st.subheader("📈 Evolução")
            df["date"] = pd.to_datetime(df["date"])
            st.line_chart(df.groupby("date")["value"].sum())

            st.subheader("📋 Histórico")
            st.dataframe(df, use_container_width=True)

        else:
            st.info("Nenhum dado ainda")

    # =========================
    # ADICIONAR
    # =========================
    elif menu == "Adicionar":
        st.subheader("➕ Nova movimentação")

        name = st.text_input("Descrição")
        value = st.number_input("Valor", min_value=0.0, format="%.2f")
        category = st.selectbox(
            "Categoria",
            ["Alimentação", "Salário", "Transporte", "Lazer", "Outros"]
        )
        type_ = st.selectbox("Tipo", ["Receita", "Despesa"])
        dt = st.date_input("Data", value=date.today())

        if st.button("Salvar"):
            if name and value > 0:
                if add_data(user_id, name, value, category, type_, dt):
                    st.success("Salvo com sucesso!")
                    st.rerun()
            else:
                st.warning("Preencha os campos corretamente")

    # =========================
    # GERENCIAR
    # =========================
    elif menu == "Gerenciar":
        st.subheader("🗑️ Gerenciar dados")

        df = get_data(user_id)

        if not df.empty:
            for _, row in df.iterrows():
                col1, col2 = st.columns([4, 1])

                col1.write(
                    f"{row['name']} - R$ {row['value']} ({row['type']})"
                )

                if col2.button("Excluir", key=row['id']):
                    if delete_data(row["id"]):
                        st.success("Excluído!")
                        st.rerun()
        else:
            st.info("Sem dados para excluir")
