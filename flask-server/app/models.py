from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import itertools
import json
import urllib.request

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


def get_api_data(name):
    url = "https://covid-api.mmediagroup.fr/v1/" + name
    response = urllib.request.urlopen(url)
    data = response.read()
    to_dict = json.loads(data)
    to_dict = dict(itertools.islice(to_dict.items(), 10))

    return to_dict


def upsert_vaccines():
    vaccines = get_api_data('vaccines')

    for key in vaccines.keys():
        country = key

        try:
            administered = vaccines[country]['All']['administered']
            people_vaccinated = vaccines[country]['All']['people_vaccinated']
            people_partially_vaccinated = vaccines[country]['All']['people_partially_vaccinated']

            vaccine = VaccineModel(country, administered, people_vaccinated, people_partially_vaccinated)
            db.session.add(vaccine)
            db.session.commit()

        except:
            db.session.rollback()
            vaccine = VaccineModel.query.filter('country' == country)
            administered = vaccines[country]['All']['administered']
            people_vaccinated = vaccines[country]['All']['people_vaccinated']
            people_partially_vaccinated = vaccines[country]['All']['people_partially_vaccinated']

            vaccine.administered = administered
            vaccine.people_vaccinated = people_vaccinated
            vaccine.people_partially_vaccinated = people_partially_vaccinated
            db.session.commit()


def upsert_cases():
    cases = get_api_data('cases')

    for key in cases.keys():
        country = key

        try:
            confirmed = cases[country]['All']['confirmed']
            death = cases[country]['All']['deaths']
            case = CasesModel(country, confirmed, death)
            db.session.add(case)
            db.session.commit()
        except:
            db.session.rollback()
            case = CasesModel.query.filter('country' == country)
            confirmed = cases[country]['All']['confirmed']
            death = cases[country]['All']['deaths']
            case.confirmed = confirmed
            case.death = death
            db.session.commit()
