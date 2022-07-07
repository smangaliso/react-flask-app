from flask import jsonify
import itertools
import json
import urllib.request
from app.models import *


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


@app.route('/', methods=['GET'])
@app.route('/cases', methods=['GET'])
def get_cases():
    upsert_cases()
    all_cases = CasesModel.query.all()
    results = cases_schema.dump(all_cases)
    return jsonify(results)


@app.route('/vaccines', methods=['GET'])
def get_vaccines():
    upsert_vaccines()
    all_vaccines = VaccineModel.query.all()
    results = vaccines_schema.dump(all_vaccines)

    return jsonify(results)
