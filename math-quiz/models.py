from flask import Flask, request
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS

app = Flask(__name__)




app.config['SECRET_KEY'] = 'mathematicsquiz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mathematics_quiz.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_APP_NAME'] = 'MATHEMATICSQUIZ'
app.config['USER_SEND_PASSWORD_CHANGED_EMAIL'] = False
app.config['USER_SEND_REGISTERED_EMAIL'] = False
app.config['USER_SEND_USERNAME_CHANGED_EMAIL'] = False
app.config['USER_ENABLE_CONFIRM_EMAIL'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['CORS_ENABLED'] = False
#app.config['CORS_SUPPORTS_CREDENTIALS'] = True

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False, server_default='')
	active = db.Column(db.Boolean(), nullable=False, server_default='0')	
	mathematics_score = db.Column(db.Integer, nullable=False, default=0)
	email = db.Column(db.String(255), nullable=False, unique=True)
	quiz_done = db.Column(db.Boolean(), nullable=False, default=0)
	final_submit = db.Column(db.Boolean(), nullable=False, default=0)
	role = db.Column(db.Boolean(), default=False)

class Questions(db.Model):
	__tablename__ = 'questions'
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(300), nullable=False, unique=True)
	option1 = db.Column(db.String(40), nullable=False)
	option2 = db.Column(db.String(40), nullable=False)
	option3 = db.Column(db.String(40), nullable=False)
	option4 = db.Column(db.String(40), nullable=False)
	ans1 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans2 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans3 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans4 = db.Column(db.Boolean(), nullable=False, server_default='0')
	QuizCategory = db.Column(db.String(50), nullable=False)
	Type = db.Column(db.String(50), nullable=False)

class UserQA(db.Model):
	__tablename__ = 'userqa'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, nullable=False)
	question_id = db.Column(db.Integer, nullable=False)

	ans1 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans2 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans3 = db.Column(db.Boolean(), nullable=False, server_default='0')
	ans4 = db.Column(db.Boolean(), nullable=False, server_default='0')
	questions = db.Column(db.String(5000))
	
class MyModelView(ModelView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:
				return True
			return False
		return False

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		if current_user.is_anonymous is not True:
			if current_user.role == True:	
				return True
			return False
		return False

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Questions, db.session))
admin.add_view(MyModelView(UserQA, db.session))

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)

def init_db():
	db.init_app(app)
	db.drop_all()
	db.create_all()


