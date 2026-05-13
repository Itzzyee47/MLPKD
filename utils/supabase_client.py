"""
Supabase client singleton — cached for the lifetime of the Streamlit server process.
Credentials are read from .streamlit/secrets.toml:

    [supabase]
    url = "https://<project-ref>.supabase.co"
    key = "<anon-public-key>"
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource
def get_client() -> Client:
    url: str = st.secrets["supabase"]["url"]
    key: str = st.secrets["supabase"]["key"]
    return create_client(url, key)
