#This file contains the form to select by type.

import streamlit as st
from utils import get_all_types
from db import run_query

def select_type():
    types = get_all_types()

    with st.form(key="Select Type", clear_on_submit=True):
        selected_type = st.selectbox("Welk type?", types)
        submitted = st.form_submit_button("Submit")

    if submitted:
        query = "SELECT type_id FROM type WHERE type = %s"
        type_id = run_query(query, (selected_type,))[0][0]

        query = "SELECT recept_id FROM MtM_recept_type WHERE type_id = %s"
        recipe_ids = [row[0] for row in run_query(query, (type_id,))]

        for recipe_id in recipe_ids:
            query = "SELECT Naam, Beschrijving, Bron, Gemaakt, Locatie FROM recepten WHERE recept_id = %s ORDER BY Naam"
            recipe_details = run_query(query, (recipe_id,))
            st.write(recipe_details[0])
if __name__ == "__main__":
    select_type()
