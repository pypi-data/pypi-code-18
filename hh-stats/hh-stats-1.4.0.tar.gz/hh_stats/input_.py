import json

import jsonschema

from . import vacancy

_VACANCY_LIST_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "pattern": r"^\d+$",
            },
            "skills": {
                "type": "array",
                "items": {
                    "type": "string",
                    "minLength": 1,
                },
                "minItems": 1,
            },
            "salary": {
                "type": "object",
                "properties": {
                    "minimal": {
                        "$ref": "#/definitions/amount",
                    },
                    "maximal": {
                        "$ref": "#/definitions/amount",
                    },
                },
                "required": [
                    "minimal",
                    "maximal",
                ],
                "additionalProperties": False,
            },
        },
        "required": [
            "id",
            "skills",
            "salary",
        ],
        "additionalProperties": False,
    },
    "minItems": 1,
    "definitions": {
        "amount": {
            "oneOf": [
                {
                    "type": "null",
                },
                {
                    "type": "number",
                    "minimum": 0,
                },
            ],
        },
    },
}

def read_vacancies(filenames):
    vacancies = []
    for filename in filenames:
        vacancies += _read_vacancies(filename)

    return vacancies

def _read_vacancies(filename):
    vacancies = []
    with open(filename) as raw_file:
        raw_data = json.load(raw_file)
        jsonschema.validate(raw_data, _VACANCY_LIST_SCHEMA)

        vacancies = [
            vacancy.Vacancy(
                vacancy_['id'],
                vacancy_['skills'],
                vacancy.Salary(
                    vacancy_['salary']['minimal'],
                    vacancy_['salary']['maximal'],
                ),
            )
            for vacancy_ in raw_data
        ]

    return vacancies
