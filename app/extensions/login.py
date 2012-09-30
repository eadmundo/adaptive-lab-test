from flask.ext.login import LoginManager, current_user
from app.blueprints.users.models import User

login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
