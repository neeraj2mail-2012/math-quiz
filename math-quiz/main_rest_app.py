import os

from flask import Flask, render_template, request, redirect, jsonify
from flask_restplus import Api, Resource, fields, reqparse
from flask_restplus import cors 

from werkzeug.contrib.fixers import ProxyFix
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from models import *
from models import app, db
import json
from flask_cors import CORS, cross_origin

from werkzeug.datastructures import ImmutableMultiDict

#app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Mathematics Quiz API',
    description='A Mathematics quiz API',
)
#db = SQLAlchemy(app)
ns = api.namespace('math', description='Mathematics Quiz')

@ns.route('/quiz_questions')
class MathematicsQuiz(Resource):
	def get(self):
		args = list(request.args)[0]
		userid = json.loads(args).get("userid")

		#check user participated in quiz
		user = User.query.with_entities(User.quiz_done).filter_by(id=userid).one() 

		question_context = []
		if not user.quiz_done:		
			# After login, fetch all questions from 'Questions' table for the current user.	
			questions = Questions.query.all()
			#question_context = []
			for question in questions:
				q = {}
				q["id"] = question.id
				q["question"] = question.question
				q["option1"] = question.option1
				q["option2"] = question.option2
				q["option3"] = question.option3
				q["option4"] = question.option4
				q["ans1"] = question.ans1
				q["ans2"] = question.ans2
				q["ans3"] = question.ans3
				q["ans4"] = question.ans4
				q["QuizCategory"] = question.QuizCategory
				q["Type"] = question.Type
			
				question_context.append(q)
						
			# Add a record in 'UserQA' table(if record is not availabein 'UserQA' table)- All question in json format
			user_qa = UserQA.query.filter_by(user_id=userid).first()		
			if not user_qa:
				print("Iam in ..")
				user_records = {}
				user_records['user_id'] = userid
				user_records['question_id'] = 999
				user_records['questions'] = json.dumps(question_context)

				db.session.add(UserQA(**user_records))
				db.session.commit()
		else:			
			# User participated in quiz. fetch the updated QA template from 'UserQA' table and display it	
			qes_template = UserQA.query.filter_by(user_id=userid).first()			
			question_context = json.loads(qes_template.questions)
		return question_context, 201

	def post(self):
		data = api.payload
		#{'uid': '1', 'qid': 4, 'aid': 'ans1'}
		
		# Get the QA template fro 'Questions' table
		question = Questions.query.filter_by(id=data['qid']).first()
		
		# Calculate the score by comparing user input with answer's in Qustion table
		user_score = User.query.filter_by(id=data['uid']).first()
		score = user_score.mathematics_score 

		answer_flag = 0
		correct_ans = ['ans'+str(i+1) for i, ans in enumerate([question.ans1,question.ans2, question.ans3, question.ans4]) if ans]
		if sorted(correct_ans) == sorted(data['aid']):
			score += 10  # Give 10 marks 
			answer_flag = 1
			print("correct ans", correct_ans)
		else: 
			score += 0 # No Negative marking as of now
			answer_flag = 2 # For wrong answer
		# Update 'mathematics_score' and quiz_done columns of User table
		db.session.query(User).filter_by(id=data['uid']).update(({"mathematics_score":score, "quiz_done":1 }))
		db.session.commit()
		
		# Fetch the template from UserQA table and update it with answer given by user.
		answer_option_mapping = {"ans1":"option1", "ans2":"option2", "ans3":"option3", "ans4":"option4"}
		user_qa = UserQA.query.with_entities(UserQA.questions).filter_by(user_id=data['uid']).one()	
		
		if user_qa.questions:
			updated_qa_template = []
			for qes in json.loads(user_qa.questions):
				if qes.get('id') == data['qid'] :
					# update the record with the answer selected by user from checkbox/radio options
					option_selected = [answer_option_mapping[d] for d in data['aid']]					
					qes.update({"option-selected": option_selected, "answer_flag":answer_flag})
					updated_qa_template.append(qes)
				else:
					updated_qa_template.append(qes)
			#print(updated_qa_template)
			db.session.query(UserQA).filter_by(user_id=data['uid']).update({"questions": json.dumps(updated_qa_template)}) 
			db.session.commit()
			
		return {"answer_flag":answer_flag, 'qid': data['qid']}, 201

@ns.route('/final_state')
class Status(Resource):
	def get(self):
		args = list(request.args)[0]
		userid = json.loads(args).get("uid")

		status = User.query.filter_by(id=userid).first()
		#print("status.final_submit", status)
		return {"final_submit":status.final_submit}, 201

	def post(self):
		data = api.payload
		User.query.filter_by(id=data['uid']).update({"final_submit":data["final_submit"]})
		db.session.commit()
		return {"test":1}, 201

@ns.route('/leaderboard')
class leaderBoard(Resource):
	def get(self):
		args = list(request.args)[0]
		userid = int(json.loads(args).get("uid"))
	
		user_score = []
		if userid == 1: # For Admin user - he can see scores of  all users.
			scores = User.query.all()
			user_score = []
			for ss in scores:
				s={}
				s['username'] = ss.username
				s['mathematics_score'] = ss.mathematics_score
				user_score.append(s)
			return user_score, 201
		else:
			scores = User.query.filter_by(id=userid).first()			
			return [{"username": scores.username, "mathematics_score":scores.mathematics_score}], 201

if __name__ =="__main__":
	app.run(debug=True, port=9090)


