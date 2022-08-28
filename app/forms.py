from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired
from app.models import Ingredient, Type

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def find_ingredienten():
    find_ingredienten_all = Ingredient.query.order_by(Ingredient.ingredient).all()
    ingredienten_all = [(g.ingredient_id, g.ingredient) for g in find_ingredienten_all]
    return ingredienten_all

def find_types():
    find_types_all = Type.query.order_by(Type.type).all()
    types_all = [(g.type_id, g.type) for g in find_types_all]
    return types_all

class Invul_Form(FlaskForm):
    naam = StringField("Naam recept", validators=[DataRequired()])
    beschrijving = StringField("Beschrijving", validators=[DataRequired()])
    bron = StringField("Vanwaar komt het")
    gemaakt = BooleanField("Al gemaakt?")
    locatie = StringField("Waar kan je het recept vinden?", validators=[DataRequired()])
    types = MultiCheckboxField("Types", coerce=int, choices=find_types())
    ingredienten = MultiCheckboxField("Ingredienten", coerce=int, choices=find_ingredienten())
    submit = SubmitField("Invoeren")

class Edit_Form(FlaskForm):
    id = IntegerField("Id recept")
    naam = StringField("Naam recept")
    beschrijving = StringField("Beschrijving")
    bron = StringField("Vanwaar komt het")
    gemaakt = BooleanField("Al gemaakt?")
    locatie = StringField("Waar kan je het recept vinden?")
    types = MultiCheckboxField("Types", coerce=int, choices=find_types())
    ingredienten = MultiCheckboxField("Ingredienten", coerce=int, choices=find_ingredienten())
    submit = SubmitField("Invoeren")

class Filter_Form(FlaskForm):
    ingredient = MultiCheckboxField('Selecteer ingredient', coerce=int, choices=find_ingredienten())
    type = MultiCheckboxField('Selecteer type', coerce= int, choices=find_types())
    submit = SubmitField("Zoeken")