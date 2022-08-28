from app import db

recept_ingredient = db.Table('recept_ingredient',
    db.Column('recept_id', db.Integer, db.ForeignKey("recept.recept_id")),
    db.Column('ingredient_id', db.Integer, db.ForeignKey("ingredient.ingredient_id"))
)

recept_type = db.Table('recept_type',
    db.Column('recept_id', db.Integer, db.ForeignKey("recept.recept_id")),
    db.Column('type_id', db.Integer, db.ForeignKey("type.type_id"))
)

class Recept(db.Model):
    __tablename__ = 'recept'
    recept_id = db.Column(db.Integer, primary_key=True, index=  True)
    naam = db.Column(db.String(250), unique=True, nullable=False)
    beschrijving = db.Column(db.String(250), unique=False)
    bron = db.Column(db.String(250), unique=False)
    gemaakt = db.Column(db.Boolean)
    locatie = db.Column(db.String(250))

    welke_ingredienten = db.relationship('Ingredient', secondary=recept_ingredient,
                               primaryjoin=(recept_ingredient.c.recept_id == recept_id),
                               backref=db.backref('welk_recept', lazy='dynamic'), lazy='dynamic')

    welke_types = db.relationship('Type', secondary=recept_type,
                        primaryjoin=(recept_type.c.recept_id == recept_id),
                        backref=db.backref('welk_recept', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Recept: {}>'.format(self.naam)

class Type(db.Model):
    __tablename__ = 'type'
    type_id = db.Column(db.Integer, primary_key=True, index=True)
    type = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return format(self.type)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True, index=True)
    ingredient = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return format(self.ingredient)

