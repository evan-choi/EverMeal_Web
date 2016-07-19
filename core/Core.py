import datetime

import requests
import json
import re

from enum import Enum

allergy = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱']

url_meal = "http://stu.%s.kr/sts_sci_md00_001.do"

meal_dataPattern = "<tbody>([\S\s\W\w]*)<\/tbody>"
meal_pattern = "<div>(\d+)(.*)<\/div"
meal_semiDataPattern = "\[(조식|중식|석식)\]([^\[]*)"

meal_allergyPattern = "(%s)" % '|'.join(allergy)

class EducationOffice(Enum):
    UnKnown = ""
    서울특별시 = "sen.go"
    부산광역시 = "pen.go"
    대구광역시 = "dge.go"
    인천광역시 = "ice.go"
    광주광역시 = "gen.go"
    대전광역시 = "dje.go"
    울산광역시 = "use.go"
    세종특별자치시 = "sje.go"
    경기도 = "goe.go"
    강원도 = "kwe.go"
    충청북도 = "cbe.go"
    충청남도 = "cne.go"
    전라북도 = "jbe.go"
    전라남도 = "jne.go"
    경상북도 = "gbe"
    경상남도 = "gne.go"
    제주특별자치도 = "jje.go"

class MealType(Enum):
    Unknown = 0
    Breakfast = 1
    Lunch = 2
    Dinner = 3

class Allergy(Enum):
    Unknown = 0
    난류 = 1
    우유 = 2
    메밀 = 3
    땅콩 = 4
    대두 = 5
    밀 = 6
    고등어 = 7
    게 = 8
    새우 = 9
    돼지고기 = 10
    복숭아 = 11
    토마토 = 12
    아황산류 = 13
    호두 = 14
    닭고기 = 15
    쇠고기 = 16
    오징어 = 17
    조개류 = 18

    def fromString(str):
        idx = index(allergy, lambda item: item == str)

        if idx is not None:
            return Allergy(idx + 1)
        else:
            return Allergy.Unknown

class Response(object):
    def __init__(self):
        self.r = 0

class DishData(Response):
    def __init__(self):
        self.Name = ""
        self.Types = []

class Meal(Response):
    def __init__(self):
        self.Type = MealType.Unknown
        self.Dishes = []

class MealData(Response):
    def __init__(self):
        self.Date = datetime.date.today()
        self.Beakfast = Meal()
        self.Lunch = Meal()
        self.Dinner = Meal()

class SchoolData(Response):
    def __init__(self):
        self.Name = ""
        self.ZipAddress = ""
        self.Code = ""
        self.EducationOffice = EducationOffice.UnKnown
        self.EducationCode = ""
        self.KindScCode = ""
        self.CrseScCode = ""

class Meal:
    @staticmethod
    def Search(schoolName, edu: EducationOffice):
        url = 'http://par.' + edu.value + '.kr/spr_ccm_cm01_100.do'
        params = \
            {
                'kraOrgNm': schoolName.encode('utf-8'),
                'atptOfcdcScCode': "",
                'srCode': ""
            }

        data = json.loads(requests.get(url, params=params).text)

        for d in data['resultSVO']['orgDVOList']:
            sd = SchoolData()
            sd.EducationOffice = edu
            sd.Name = d['kraOrgNm']
            sd.Code = d['orgCode']
            sd.ZipAddress = d['zipAdres']
            sd.EducationCode = d['atptOfcdcOrgCode']
            sd.KindScCode = d['schulKndScCode']
            sd.CrseScCode = d['schulCrseScCode']
            yield sd

    @staticmethod
    def GetMeals(self: SchoolData, year: int, month: int):
        url = url_meal % self.EducationOffice.value
        postData = \
            {
                "insttNm": self.Name,
                "schulCode": self.Code,
                "schulCrseScCode": self.CrseScCode,
                "schulKndScCode": self.KindScCode,
                "ay": year,
                "mm": "%02d" % month
            }

        html = requests.post(url, data=postData).text
        h_match = re.match(meal_dataPattern, html)

        if h_match:
            html = h_match.group(1)

        for m in re.findall(meal_pattern, html):
            if len(m[1]) > 0:
                meal = MealData()
                for sm in re.findall(meal_semiDataPattern, m[1]):
                    dishes = []

                    for d in re.split("<br ?\/>", sm[1].strip('<br \/>')):
                        dd = DishData()
                        dd.Name = re.sub(meal_allergyPattern, "", d)
                        dd.Types = [Allergy.fromString(x) for x in re.findall(meal_allergyPattern, d)]
                        dishes.append(dd)

                    if sm[0] == "조식":
                        meal.Beakfast.Type = MealType.Lunch
                        meal.Beakfast.Dishes = dishes
                    elif sm[0] == "중식":
                        meal.Lunch.Type = MealType.Lunch
                        meal.Lunch.Dishes = dishes
                    elif sm[0] == "석식":
                        meal.Dinner.Type = MealType.Lunch
                        meal.Dinner.Dishes = dishes

                yield meal


def index(l, f):
    return next((i for i in range(len(l)) if f(l[i])), None)


""" < Sample Code >
for n in Meal.Search("장곡고등학교", EducationOffice.경기도):
    print(n.EducationOffice.name)
    print(n.Name)
    print(n.Code)
    print(n.ZipAddress)
    print(n.EducationCode)
    print(n.KindScCode)
    print(n.CrseScCode)
    print("-" * 20)

    for m in Meal.GetMeals(n, 2016, 7):
        for n in m.Lunch.Dishes:
            print(n.Name)
            print(n.Types)
        print("=" * 15)
"""
