from flask_login import LoginManager

login_manager = LoginManager()

# from app.models.user import User
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
