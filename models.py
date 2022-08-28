#for creating the mapper code
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, Enum, PrimaryKeyConstraint
#for  creating foreign key relationship between the tables
from sqlalchemy.orm import relationship
from database import Base

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Recept(Base, DictMixIn):
    __tablename__ = 'recept'

    recept_id = Column(Integer, primary_key=True, index=True)
    naam = Column(String(250), unique=True, nullable=False)
    beschrijving = Column(String(250), unique=False)
    bron = Column(String(250), unique=False)
    gemaakt = Column(Boolean)
    locatie = Column(String(250))

class Type(Base, DictMixIn):
    __tablename__ = 'type'
    type_id = Column(Integer, primary_key=True, index=True)
    type = Column(String(250), unique=True, nullable=False)

class Ingredient(Base, DictMixIn):
    __tablename__ = 'ingredient'
    ingredient_id = Column(Integer, primary_key=True, index=True)
    ingredient = Column(String(250), unique=True, nullable=False)

class ReceptIngredient(Base):
    __tablename__ = "recept_ingredient"
    recept_id = Column(Integer, ForeignKey("recept.recept_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.ingredient_id"), primary_key=True)

    recepten = relationship(Recept, lazy="joined")

class ReceptType(Base):
    __tablename__ = "recept_type"
    recept_id = Column(Integer, ForeignKey("recept.recept_id"), primary_key=True)
    type_id = Column(Integer, ForeignKey("type.type_id"), primary_key=True)

    recepten = relationship(Recept, lazy="joined")
    #'ingredienten' (meervoud) geeft aan dat het een collectie is in dit geval many-to-many-relatie
    # relationsship(class-name -> aangeven dat er een relatie is en dat die in die Class kan gevonden worden
    #                  secondary=tabel die M-t-M linkt,
    #                  backpopulates="naam van relatie in andere moedertabel"
    #               )
