#This file will handle database connections and queries.

import streamlit as st
import mysql.connector
from st_supabase_connection import SupabaseConnection

# Initialize connection.
def get_connection():
    # op tommy-server
    # return mysql.connector.connect(**st.secrets["mysql_recepten"])
    # hier op de pc
    # return mysql.connector.connect(**st.secrets["mysql_recepten_lokaal"])
    # op Supabase
    return st.connection("supabase", type=SupabaseConnection)

# Perform query.
def run_query(query, params=None):
    with get_connection() as conn:
        with conn.cursor(buffered=True) as cur:
            cur.execute(query, params or ())
            if query.strip().lower().startswith(('insert', 'update', 'delete')):
                conn.commit()
                return cur.lastrowid
            else:
                return cur.fetchall()
