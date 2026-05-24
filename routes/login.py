from flask import Blueprint
from services.login import login_service

login = Blueprint('login', __name__)

@login.route('/', methods=['POST'])
def iniciar_sesion():
    return login_service()