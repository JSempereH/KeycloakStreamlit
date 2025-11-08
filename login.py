"""This script controls de login into de platform.

It will check the username and passwords depending on the role
"""

import requests
import streamlit as st
from loguru import logger

from settings import settings


def login():
    hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("Login system")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        login_info = {
            "grant_type": settings.keycloak_grant_type,
            "client_id": settings.keycloak_client_id,
            "client_secret": settings.keycloak_client_secret,
            "username": username,
            "password": password,
        }

        response = requests.post(settings.keycloak_token_url, data=login_info)

        if response.status_code == 200:
            token = response.json()["token_type"] + " " + response.json()["access_token"]
            st.session_state.token = token
            headers = {"Authorization": f"{token}"}
            user_info = requests.get(settings.keycloak_userinfo_url, headers=headers)
            st.session_state.roles = user_info.json().get("realm_access", {}).get("roles", [])
            st.success("Authenticated successfully")
            logger.info(f"Username {username} has successfully authenticated.")
            st.session_state["query_params"] = {}
            st.session_state["authenticated_user"] = username
            st.rerun()
        else:
            st.error("Wrong username or password.")
