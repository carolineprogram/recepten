
import streamlit as st
from st_supabase_connection import SupabaseConnection

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.table("recepten_ingredient").select("*").execute()

#Om te kunnen werken op Supabase RLS Row Level Security op de tabel afzetten
# Print results.
#for row in rows.data:
#    st.write(f"{row['ingredient']} has a :{row['type']}:")

def run_query(query, params=None):
    try:
        with get_connection() as conn:
            with conn.cursor(buffered=True) as cur:
                cur.execute(query, params or ())
                if query.strip().lower().startswith(('insert', 'update', 'delete')):
                    conn.commit()
                    return cur.lastrowid
                else:
                    return cur.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
query ="SELECT recept_id FROM recepten_MtM_recept_ingredient"
result = run_query(query)
st.write(result)