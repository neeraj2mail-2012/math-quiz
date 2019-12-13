import os
from flask import Flask, render_template, request, redirect
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter, current_user
from models import *
import json

from models import app
CORS(app)

#init_db() // Uncomment it for First run


@app.route('/', defaults={'category':'mathematics'})
@app.route('/quiz/<category>', defaults={'category':'mathematics'})
@login_required
def play(category):
	return render_template('play.html', array=[], category=[], currentuser=current_user.username)	

@app.route('/leaderboard')
@login_required
def leaderboard():
	return render_template('leaderboard.html')

@app.errorhandler(404)
def custom404(error):
	return render_template('custom404.html')

## Admin/Test123
if __name__ == '__main__':
	if User.query.filter_by(username="Admin").first(): 
		pass
	else:
		db.session.add(
			User(username="Admin", password="$2b$12$73oNniK.gUj3n43h/MAlpe14Q2sMqKe7f1KNHlbwdlnS0s5WYiLq.",
				email='admin@gmail.com', role=True, active=True)
			)
		db.session.commit()
	app.run(debug=True)
