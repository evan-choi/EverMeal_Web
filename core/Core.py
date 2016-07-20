#-*- coding: utf-8 -*-
import datetime

import requests
import json
import re

from enum import Enum
from app.model.neis import MealCache, Neis
from app.database import DBManager

allergy = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩', '⑪', '⑫', '⑬', '⑭', '⑮', '⑯', '⑰', '⑱']

url_meal = "http://stu.%s.kr/sts_sci_md00_001.do"

w_break = "조식"
w_lunch = "중식"
w_dinner = "석식"

meal_dataPattern = "<tbody>([\S\s\W\w]*)<\/tbody>"
meal_pattern = "<div>(\d+)(.*)<\/div"
meal_semiDataPattern = u"\[({0}|{1}|{2})\]([^\[]*)".format(w_break, w_lunch, w_dinner)
meal_dayPattern = "<td><div>(\d+)<br ?\/>"

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


class DishData:
    def __init__(self):
        self.Name = ""
        self.Types = []

    def __dict__(self):
        return \
            {
                "name": self.Name,
                "types": [t.value for t in self.Types]
            }

    def __str__(self):
        return str(self.__dict__())


class Meal:
    def __init__(self):
        self.Type = MealType.Unknown
        self.Dishes = []

    def __dict__(self):
        return \
            {
                "type": str(self.Type.value),
                "dishes": [d.__dict__() for d in self.Dishes]
            }

    def __str__(self):
        return str(self.__dict__())


class MealData:
    def __init__(self):
        self.Date = str(datetime.date.today())
        self.Breakfast = Meal()
        self.Lunch = Meal()
        self.Dinner = Meal()

    def __dict__(self):
        return \
            {
                "date": self.Date,
                "breakfast": self.Breakfast.__dict__(),
                "lunch": self.Lunch.__dict__(),
                "dinner": self.Dinner.__dict__()
            }

    def __str__(self):
        return str(self.__dict__())


class SchoolData:
    def __init__(self):
        self.Name = ""
        self.ZipAddress = ""
        self.Code = ""
        self.EducationOffice = EducationOffice.UnKnown
        self.EducationCode = ""
        self.KindScCode = ""
        self.CrseScCode = ""

    def __str__(self):
        return \
            {
                "name": self.name,
                "zipAddress": self.ZipAddress,
                "code": self.Code,
                "educationOffice": self.EducationOffice,
                "educationCode": self.EducationCode,
                "kindScCode": self.KindScCode,
                "crseScCode": self.CrseScCode
            }

class NeisEngine:
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

        idx = 0
        days = re.findall(meal_dayPattern, html)

        for m in re.findall(meal_pattern, html):
            if len(m[1]) > 0:
                day = days[idx]
                idx += 1

                meal = MealData()
                meal.Date = str(year) + "-" + str(month) + "-" + day

                for sm in re.findall(meal_semiDataPattern, m[1]):
                    dishes = []

                    for d in re.split("<br ?\/>", sm[1].strip('<br \/>')):
                        dd = DishData()
                        dd.Name = re.sub(meal_allergyPattern, "", d)
                        dd.Types = [Allergy.fromString(x) for x in re.findall(meal_allergyPattern, d)]
                        dishes.append(dd)

                    if sm[0] == w_break:
                        meal.Breakfast.Type = MealType.Lunch
                        meal.Breakfast.Dishes = dishes
                    elif sm[0] == w_lunch:
                        meal.Lunch.Type = MealType.Lunch
                        meal.Lunch.Dishes = dishes
                    elif sm[0] == w_dinner:
                        meal.Dinner.Type = MealType.Lunch
                        meal.Dinner.Dishes = dishes

                yield meal

    @staticmethod
    def SearchFromName(schoolName):
        for s in Neis.query.filter(Neis.name.like("%" + schoolName + "%")).all():
            yield NeisEngine.toSchoolStruct(s)


    @staticmethod
    def SearchFromToken(token):
        for s in Neis.query.filter(Neis.token == token).all():
            yield NeisEngine.toSchoolStruct(s)


    @staticmethod
    def toSchoolStruct(neis: Neis):
        school = SchoolData()
        school.EducationOffice = EducationOffice(neis.education_office)
        school.Name = neis.name
        school.Code = neis.code
        school.KindScCode = neis.kind_sc_code
        school.CrseScCode = neis.crse_sc_Code
        school.ZipAddress = neis.zip_address

        return school


    @staticmethod
    def GetJsonMeals(self: SchoolData, year: int, month: int):
        jData = ""
        d = str(year) + "_" + str(month)
        mData = MealCache.query.filter_by(code=self.Code, update_date=d).first()

        if mData is None:
            jData = json.dumps([m.__dict__() for m in NeisEngine.GetMeals(self, year, month)])

            DBManager.db.session.add(MealCache(self.Code, jData, d))
            DBManager.db.session.commit()
        else:
            jData = mData.json

        return jData



def index(l, f):
    return next((i for i in range(len(l)) if f(l[i])), None)