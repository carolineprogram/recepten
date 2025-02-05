import streamlit as st
from supabase import create_client, Client

# Initialize connection.
# Uses st.cache_resource to only run once.
#@st.cache_resource
def init_connection():
    url = "https://qnmvdxpiuvtotkkxmgbw.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFubXZkeHBpdXZ0b3Rra3htZ2J3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMwNzk0MDUsImV4cCI6MjA0ODY1NTQwNX0.V27BENxyRWwuNC0YRVcmzL5yhbTO37x_FLDJjdHnWAc"
    return create_client(url, key)

supabase = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
def run_query():
    return supabase.table("recepten_recepten").select("*").execute()

rows = run_query()

# Print results.
for row in rows.data:
    st.write("koekoek")
    #st.write(f"{row['Naam']} has a :{row['Bron']}:")
