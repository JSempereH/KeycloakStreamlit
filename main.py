"""This module manages the principal configurations.

Logging configuration, application initialization,
and user session control within a Streamlit-based application.

"""

import logging

import streamlit as st
from loguru import logger

from login import login

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Avoid duplicates by removing existing handlers
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

handler = logging.StreamHandler()
root_logger.addHandler(handler)

logging.getLogger().handlers.clear()


# From logging to loguru
class InterceptHandler(logging.Handler):
    """Intercept logging to send it to loguru."""

    def emit(self, record):
        """Send the record to loguru."""
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)
logging.getLogger().addHandler(InterceptHandler())

# Add a handler to loguru
logger.remove()
logger.add(
    "app.log",
    rotation="1 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


def main_app():
    """Main application."""
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

    if st.sidebar.button("Log out"):
        username = st.session_state.authenticated_user
        for key in ["token", "roles", "query_params", "authenticated_user"]:
            if key in st.session_state:
                del st.session_state[key]
        logger.info(f"Username {username} has logged out.")
        st.rerun()
    
    st.header("Now you are logged in :)")


def run():
    """Function to run the application."""
    if "token" not in st.session_state:
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True,
        )
        login()
    else:
        main_app()


run()
