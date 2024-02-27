from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    missions = db.relationship("Mission", back_populates="planet")
    scientists = association_proxy("missions", "scientist")

    serialize_rules = ("-missions.planet", "-scientists")


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    missions = db.relationship("Mission", back_populates="scientist")
    planets = association_proxy("missions", "planet")

    serialize_rules = ("-missions.scientist", "-planets")

    @validates("name")
    def validate_name(self, key, name):
        if name and len(name) > 0:
            return name
        else:
            raise ValueError("Name cannot be empty")

    @validates("field_of_study")
    def validate_field_of_study(self, key, field_of_study):
        if field_of_study and len(field_of_study) > 0:
            return field_of_study
        else:
            raise ValueError("Field of study cannot be empty")

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets_table.id'), nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists_table.id'), nullable=False)

    scientist = db.relationship("Scientist", back_populates="missions")
    planet = db.relationship("Planet", back_populates="missions")

    serialize_rules = ("-scientist.missions", "-planet.missions")