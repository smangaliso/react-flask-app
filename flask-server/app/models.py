from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)


class CasesModel(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(), unique=True)
    confirmed = db.Column(db.Integer)
    death = db.Column(db.Integer)

    def __init__(self, country, confirmed, death):
        self.country = country
        self.confirmed = confirmed
        self.death = death

    def __repr__(self):
        return f"<Cases {self.country}>"


class VaccineModel(db.Model):
    __tablename__ = 'vaccines'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(), unique=True)
    administered = db.Column(db.Integer)
    people_vaccinated = db.Column(db.Integer)
    people_partially_vaccinated = db.Column(db.Integer)

    def __init__(self, country, administered, people_vaccinated, people_partially_vaccinated):
        self.country = country
        self.administered = administered
        self.people_vaccinated = people_vaccinated
        self.people_partially_vaccinated = people_partially_vaccinated

    def __repr__(self):
        return f"<Vaccines {self.country}>"


class CasesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'country', 'confirmed', 'death')


class VaccinesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'country', 'administered', 'people_vaccinated', 'people_partially_vaccinated')


case_schema = CasesSchema()
cases_schema = CasesSchema(many=True)

vaccine_schema = VaccinesSchema()
vaccines_schema = VaccinesSchema(many=True)
