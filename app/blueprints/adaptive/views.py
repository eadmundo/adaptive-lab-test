from app.blueprints.adaptive import blueprint
from app.blueprints.adaptive.models import Tweet, User

@blueprint.route('/')
def tweets():
    return 'adaptive blueprint'
