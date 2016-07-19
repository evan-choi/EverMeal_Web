import json
from flask import jsonify

from app import create_app
from core.Core import Meal, EducationOffice


"""
for n in Meal.Search("장곡고등학교", EducationOffice.경기도):
    print(n.Name)
    for m in Meal.GetMeals(n, 2016, 7):
        print(json.dumps(m))
"""

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080)
else:
    app = create_app()
