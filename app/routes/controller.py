from app.blueprint import basic


@basic.route('/')
def index():
	return '과제 넘나 빡쌘것'
