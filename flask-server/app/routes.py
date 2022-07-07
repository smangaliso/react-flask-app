from flask import jsonify


from app.models import *


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
