from flask import Blueprint

basic = Blueprint('basic', __name__,
                  template_folder='templates',
                  static_url_path='/assets',
                  static_folder='assets')
