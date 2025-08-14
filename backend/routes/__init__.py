from flask import Blueprint

auth_bp = Blueprint("auth", __name__)
donors_bp = Blueprint("donors", __name__)
recipients_bp = Blueprint("recipients", __name__)
drives_bp = Blueprint("drives", __name__)
