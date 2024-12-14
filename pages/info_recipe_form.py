#This file contains the form to select recipes.
import streamlit as st
from utils import get_recipe, get_ingredients, get_types
from form_snippets import select_recipe


if "clicked"not in st.session_state:
    st.session_state["clicked"] = False

def click_button():
    st.session_state["clicked"] = True

def recipe_info_form(recipe_name):
    recipe_data = get_recipe(recipe_name)
    recipe_id = recipe_data[0][0]
    beschrijving = recipe_data[0][1]
    bron = recipe_data[0][2]
    gemaakt = str(recipe_data[0][3])
    locatie = recipe_data[0][4]
    st.title(recipe_name)
    st.markdown("Beschrijving: " + beschrijving)
    st.markdown("Bron: " + bron)
    st.markdown("Gemaakt: " + gemaakt)
    st.markdown("Locatie: " + locatie)
    ingredients = get_ingredients(recipe_id)
    st.markdown('<h3><strong>Ingrediënten</strong></h3>', unsafe_allow_html=True)
    for i in ingredients:
        st.markdown(f"{i[1]} (id: {i[0]})")
        ingredient_data = {'hele jaar': i[2], 'januari': i[3], 'februari': i[4], 'maart': i[5], 'april': i[6], 'mei': i[7], 'juni': i[8], 'juli': i[9], 'augustus': i[10], 'september': i[11], 'oktober': i[12], 'november': i[13], 'december': i[14]}
        maanden = ['jan', 'feb', 'maa', 'apr',
                           'mei', 'jun', 'jul', 'aug', 'sep',
                           'okt', 'nov', 'dec']

        #col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(12)
        cols = st.columns(12)
        for m in range(len(maanden)):
            with cols[m]:
                 st.markdown(maanden[m])
                 st.write(i[m+2])
    st.markdown('<h3><strong>Type</strong></h3>', unsafe_allow_html=True)
    types = get_types(recipe_id)
    for j in types:
        st.markdown(f"{j[1]}")

def recipe_info_page(recipe_request=None):
    if recipe_request:
        selected_recipe = recipe_request
    else:
        selected_recipe = select_recipe(form_key="Select Recipe Info", button_label="Info")

    if selected_recipe:
        recipe_info_form(selected_recipe)
        st.session_state["recipe"] = selected_recipe
        st.button(label="Update recept", on_click=click_button)

    if st.session_state["clicked"] == True:
        st.write("session state is True")
        st.switch_page("pages/update_recipe_form.py")

if __name__ == "__main__":
    recipe_info_page(None)
