
import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.table("recepten_ingredient").select("*").execute()

#Om te kunnen werken op Supabase RLS Row Level Security op de tabel afzetten
# Print results.
for row in rows.data:
    st.write(f"{row['Naam']} has a :{row['Bron']}:")


