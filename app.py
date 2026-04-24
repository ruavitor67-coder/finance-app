import streamlit as st
from db import create_tables
from auth import login, register
from ui import dashboard, add_screen, manage_screen

create_tables()

st.set_page_config(page_title="Finance App")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# LOGIN
if st.session_state.user_id is None:
    st.title("🔐 Login")

    tab1, tab2 = st.tabs(["Entrar", "Registrar"])

    with tab1:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            uid = login(user, password)
            if uid:
                st.session_state.user_id = uid
                st.rerun()
            else:
                st.error("Login inválido")

    with tab2:
        new_user = st.text_input("Novo usuário")
        new_pass = st.text_input("Nova senha", type="password")

        if st.button("Registrar"):
            if register(new_user, new_pass):
                st.success("Usuário criado!")
            else:
                st.error("Usuário já existe")

# APP
else:
    st.sidebar.title("Menu")

    if st.sidebar.button("Sair"):
        st.session_state.user_id = None
        st.rerun()

    menu = st.sidebar.radio("Navegação", ["Dashboard", "Adicionar", "Gerenciar"])

    if menu == "Dashboard":
        dashboard(st.session_state.user_id)

    elif menu == "Adicionar":
        add_screen(st.session_state.user_id)

    elif menu == "Gerenciar":
        manage_screen(st.session_state.user_id)