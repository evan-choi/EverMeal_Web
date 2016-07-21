# coding: utf-8

from app import create_app

if __name__ == '__main__':
    app = create_app()

    from core.Core import NeisEngine, EducationOffice
    #print([d.Name for d in NeisEngine.Search("장곡고", EducationOffice.Gyunggi)])

    for s in NeisEngine.SearchFromName(u"대덕소프트웨어"):
        for m in NeisEngine.GetMeals(s, 2016, 7):
            print(m.toDict())

    app.run(host='127.0.0.1', port=8080)
else:
    app = create_app()
