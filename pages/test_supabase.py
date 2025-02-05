
#def init_connection():
#    url = "https://qnmvdxpiuvtotkkxmgbw.supabase.co"
#    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFubXZkeHBpdXZ0b3Rra3htZ2J3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMwNzk0MDUsImV4cCI6MjA0ODY1NTQwNX0.V27BENxyRWwuNC0YRVcmzL5yhbTO37x_FLDJjdHnWAc"
#    return create_client(url, key)

import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.table("recepten_recepten").select("*").execute()
#Om te kunnen werken op Supabase RLS Row Level Security op de tabel afzetten
# Print results.
for row in rows.data:
    st.write(f"{row['Naam']} has a :{row['Bron']}:")


