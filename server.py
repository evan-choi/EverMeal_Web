from enum import Enum

from app import create_app

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

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080)
else:
    app = create_app()
