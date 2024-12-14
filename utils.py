#This file contains utility functions for fetching data.
from db import run_query

def get_recipe(recipe_name):
    query = "SELECT recept_id, Beschrijving, Bron, Gemaakt, Locatie FROM recepten WHERE Naam = %s"
    params = (recipe_name,)
    return run_query(query, params)

def get_all_recipe_names():
    query = "SELECT recept_id, Naam FROM recepten ORDER BY Naam"
    return [row[1] for row in run_query(query)]

def get_types(recipe_name):
    """Return is list met list[type_id, type_naam] voor een bepaald recept"""
    query = "SELECT type_id FROM MtM_recept_type WHERE recept_id = %s"
    params = (recipe_name,)
    types_ids = run_query(query, params)
    types = []
    for i in types_ids:
        type_id = i[0]
        query2 = "SELECT * FROM type WHERE type_id = %s"
        params2 = (type_id,)
        type_details = run_query(query2, params2)
        if type_details:
            types.append(type_details[0])
    return types


def get_all_types():
    query = "SELECT type_id, type FROM type ORDER BY type"
    return [row[1] for row in run_query(query)]

def get_ingredients(recipe_id):
    query = "SELECT ingredient_id FROM MtM_recept_ingredient WHERE recept_id = %s"
    params = (recipe_id,)
    ingredient_ids = run_query(query, params)

    ingredients = []
    for i in ingredient_ids:
        ingredient_id = i[0]
        query2 = "SELECT * FROM ingredient WHERE ingredient_id = %s"
        params2 = (ingredient_id,)
        ingredient_details = run_query(query2, params2)
        if ingredient_details:
            ingredients.append(ingredient_details[0])  # Assuming ingredient_details is a list of tuples
    return ingredients

def get_all_ingredients():
    query = "SELECT ingredient_id, ingredient, type FROM ingredient ORDER BY ingredient"
    return [(row[1], row[2]) for row in run_query(query)]

def get_all_ingredients_in_month(month):
    query = f"SELECT ingredient_id, ingredient, type FROM ingredient WHERE hele_jaar = '1' OR {month} = '1' ORDER BY ingredient"
    return [(row[1], row[2]) for row in run_query(query)]

def get_ingredient_id(ingredient_naam):
    query = "SELECT ingredient_id FROM ingredient WHERE ingredient = %s"
    params = (ingredient_naam,)
    rows = run_query(query, params)
    if rows:
        return rows[0][0]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found

def insert_recipe(name, description, source, made, location):
    query = "INSERT INTO recepten (Naam, Beschrijving, Bron, Gemaakt, Locatie) VALUES (%s, %s, %s, %s, %s)"
    params = (name, description, source, made, location)
    return run_query(query, params)

def insert_types_for_recipe(type_list, recipe_id):
    for i in type_list:
        query = "INSERT INTO MtM_recept_type (recept_id, type_id) VALUES (%s, %s)"
        params = (recipe_id, i)
        return run_query(query, params)


def insert_ingredients_for_recipe(ingredient_list, recipe_id):
    for i in ingredient_list:
        print(i)
        query = "INSERT INTO MtM_recept_ingredient (recept_id, ingredient_id) VALUES (%s, %s)"
        params = (recipe_id, i)
        run_query(query, params)
    return True

def insert_new_ingredients(ingredient_name):
    query = "INSERT INTO ingredient (ingredient) VALUES (%s)"
    params = (ingredient_name, )
    return run_query(query, params)
#TODO: zorg dat je type kan ingeven met dropdowmenu

def delete_ingredients(ingredient_list, recipe_id):
    for i in ingredient_list:
        query = "DELETE FROM MtM_recept_ingredient WHERE recept_id = (%s) AND ingredient_id = (%s)"
        params = (recipe_id, i)
        return run_query(query, params)

def delete_types(type_list, recipe_id):
    for i in type_list:
        query = "DELETE FROM MtM_recept_type WHERE recept_id = (%s) AND type_id = (%s)"
        params = (recipe_id, i)
        return run_query(query, params)

def update_recipe(recipe_id, title, beschrijving, bron, gemaakt, locatie):
    query = "UPDATE recepten SET Naam = %s, Beschrijving = %s, Bron = %s, Gemaakt = %s, Locatie = %s WHERE recept_id = %s"
    params = (title, beschrijving, bron, gemaakt, locatie, recipe_id)
    return run_query(query, params)

def update_types(old_types, new_types, recipe_id):
    unchanged_types = [item for item in old_types if item in new_types]
    todelete_types = [item for item in old_types if item not in unchanged_types]
    todelete_types_ids = [get_type_id(item) for item in todelete_types]
    insert_types = [item for item in new_types if item not in unchanged_types]

    insert_types_ids = []
    for type in insert_types:
        try:
            type_id = get_type_id(type)
            insert_types_ids.append(type_id)
        except Exception as e:
            st.text(f"Error bij update_types - type_id: {e}")

    if todelete_types_ids:
        delete_types(todelete_types_ids, recipe_id)
    if insert_types_ids:
        insert_types_for_recipe(insert_types_ids, recipe_id)

def get_type_id(type_naam):
    query = "SELECT type_id FROM type WHERE type = %s"
    params = (type_naam,)
    rows = run_query(query, params)
    if rows:
        return rows[0][0]  # Return the first ingredient_id found
    else:
        return None  # Return None if ingredient not found

def update_ingredients(old_ingredients, new_ingredients, recipe_id):
    unchanged_ingredients = [item for item in old_ingredients if item in new_ingredients]
    todelete_ingredients = [item for item in old_ingredients if item not in unchanged_ingredients]
    todelete_ingredients_ids = [get_ingredient_id(item) for item in todelete_ingredients]
    insert_ingredients = [item for item in new_ingredients if item not in unchanged_ingredients]

    insert_ingredients_ids = []
    for ingredient in insert_ingredients:
        ingredient_id = get_ingredient_id(ingredient)
        if ingredient_id:
            insert_ingredients_ids.append(ingredient_id)
        else:
            ingredient_id = insert_new_ingredients(ingredient)
            insert_ingredients_ids.append(ingredient_id)

    if todelete_ingredients_ids:
        delete_ingredients(todelete_ingredients_ids, recipe_id)
    if insert_ingredients_ids:
        insert_ingredients_for_recipe(insert_ingredients_ids, recipe_id)

def get_all_type_ingredients():
    query = "SELECT DISTINCT type FROM ingredient ORDER BY type"
    return [row[0] for row in run_query(query)]
