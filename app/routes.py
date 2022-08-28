from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import outerjoin
# from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse
from app import app, db
from app.forms import Invul_Form, Edit_Form, Filter_Form
from app.models import Recept, Type, Ingredient, recept_type, recept_ingredient
# from datetime import datetime

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def find_ingredienten(recept_id=None):
    if recept_id:
        find_ingredienten_all = Ingredient.query.outerjoin(recept_ingredient).\
            filter(recept_ingredient.c.recept_id == recept_id).\
            order_by(Ingredient.ingredient).\
            all()
    else:
        find_ingredienten_all = Ingredient.query.order_by(Ingredient.ingredient).all()
    find_ingredienten_all = [(g.ingredient_id, g.ingredient) for g in find_ingredienten_all]
    return find_ingredienten_all

def find_types(recept_id=None):
    if recept_id:
        find_types_all = Type.query.outerjoin(recept_type).filter(recept_type.c.recept_id == recept_id).order_by(Type.type).all()
    else:
        find_types_all = Type.query.order_by(Type.type).all()
    find_types_all = [(g.type_id, g.type) for g in find_types_all]
    return find_types_all

def update_multiselect(recept_id, recept_to_edit, editform, multiselect):
    if multiselect == 'ingredienten':
        oud_tuple = find_ingredienten(recept_id)
        tabel = Ingredient
        assoc_tabel = recept_to_edit.welke_ingredienten
    elif multiselect == 'types':
        oud_tuple = find_types(recept_id)
        tabel = Type
        assoc_tabel = recept_to_edit.welke_types

    oud_list = []
    if(oud_tuple):
        oud_list = [oud[0] for oud in oud_tuple]

    nieuw = editform.data[multiselect]

    for nw in nieuw:
        if (oud_list) and (nw in oud_list):
            oud_list.remove(nw)
        else:
            nw = db.session.query(tabel).get(nw)
            assoc_tabel.append(nw)
    if(oud_list):
        for oud in oud_list:
            oud = db.session.query(tabel).get(oud)
            assoc_tabel.remove(oud)

@app.route('/')
@app.route('/index')
def index():
    invulform = Invul_Form(find_ingredienten(None))
    return render_template('index.html', title='Overzicht', form=invulform)


@app.route("/overzicht")
def overzicht(recepten=[]):
    if(recepten):
        recepten_all = recepten
    else:
        recepten_all = Recept.query.order_by(Recept.recept_id).all()
    return render_template('overzicht.html', title="Overzicht van recepten", recepten=recepten_all)

@app.route("/overzicht_type")
def overzicht_type():
    types_all = find_types()
    recepten = []
    if request.args.get('type_id'):
        type_id = request.args.get('type_id')
        recepten = db.session.query(Recept).outerjoin(recept_type).filter(recept_type.c.type_id == type_id)
    return render_template('overzicht_type.html', title="Overzicht van recepten per type", types=types_all, recepten=recepten)

@app.route("/overzicht_ingredienten")
def overzicht_ingredienten():
    ingredienten_all = find_ingredienten()
    recepten = []
    if request.args.get('ingredient_id'):
        ingredient_id = request.args.get('ingredient_id')
        recepten = db.session.query(Recept).outerjoin(recept_ingredient).filter(recept_ingredient.c.ingredient_id == ingredient_id)
    return render_template('overzicht_ingredienten.html', title="Overzicht van recepten per ingredient", ingredienten=ingredienten_all, recepten=recepten)

@app.route('/invulformulier', methods=['GET', 'POST'])
def invulformulier():
    invulform = Invul_Form()
    print('ok1')
    if invulform.validate_on_submit():
        recept_to_add = Recept()
        print('ok2')
        invulform.populate_obj(recept_to_add)
        # steek alle recept-records in databank
        db.session.add(recept_to_add)
        db.session.flush()
        # haal nieuwe recept_id op
        recept_id = recept_to_add.recept_id
        print('ok3')
        print(recept_id)

        # update de ingredienten_lijst
        update_multiselect(recept_id, recept_to_add, invulform, 'ingredienten')
        # update de types-lijst
        update_multiselect(recept_id, recept_to_add, invulform, 'types')

        db.session.commit()
        flash("Recept is opgeslagen.")
        return redirect('/overzicht')
    return render_template('invul.html', title='InvulFormulier', form=invulform)

@app.route("/fiche")
def fiche_recept():
    recept_id = request.args.get('id')
    recept = Recept.query.get(recept_id)
    type_recept = find_types(recept_id)
    ingredienten_recept = find_ingredienten(recept_id)
    return render_template('receptfiche.html', title='Receptfiche', gegevens=recept, types=type_recept, ingredienten=ingredienten_recept)


@app.route('/edit', methods=['GET', 'POST'])
def edit_recept():
    recept_id = request.args.get('id')
    recept_to_edit = Recept.query.get(recept_id)
    editform = Edit_Form(obj=recept_to_edit)
    if editform.validate_on_submit():
        # steek alle recept-records in databank
        editform.populate_obj(recept_to_edit)
        db.session.add(recept_to_edit)
        # update de ingredienten_lijst
        update_multiselect(recept_id, recept_to_edit, editform, 'ingredienten')
        # update de types-lijst
        update_multiselect(recept_id, recept_to_edit, editform, 'types')

        db.session.commit()
        print(recept_to_edit.id)
        flash("Recept is opgeslagen.")
        return redirect(url_for('edit_recept', id=recept_to_edit.id))
    elif request.method == 'GET':
        editform.id.data = recept_to_edit.recept_id
        editform.naam.data = recept_to_edit.naam
        editform.beschrijving.data = recept_to_edit.beschrijving
        editform.bron.data = recept_to_edit.bron
        editform.gemaakt.data = recept_to_edit.gemaakt
        editform.locatie.data = recept_to_edit.locatie
        editform.types.data = [b[0] for b in find_types(recept_id)]
        editform.ingredienten.data = [c[0] for c in find_ingredienten(recept_id)]
    return render_template('edit.html', title='Edit Recept', form=editform, id=recept_id)

@app.route("/filter", methods=['GET', 'POST'])
def filter():
    filterform = Filter_Form()
    if filterform.validate_on_submit():
        filter_type = filterform.data['type']
        filter_ingredient = filterform.data['ingredient']
        query_filter = db.session.query(Recept)
        if len(filter_type)>0:
            query_filter = query_filter.outerjoin(recept_type).filter(recept_type.c.type_id.in_(filter_type))
        if(len(filter_ingredient))>0:
            query_filter = query_filter.outerjoin(recept_ingredient).filter(recept_ingredient.c.ingredient_id.in_(filter_ingredient))
        recepten_filter = query_filter.all()
        return render_template('overzicht.html', title="Gefilterd", recepten=recepten_filter)
    else:
        return render_template('filter.html', title="Filter van recepten", form=filterform)
