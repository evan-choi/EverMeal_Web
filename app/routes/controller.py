from app.blueprint import basic

@basic.route('/')
def index():
    return "please"
