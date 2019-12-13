# MathematicsQuiz
This is an online quiz portal.
A user 'Admin' (Teacher) can add/update/delete Single/Multiple choice type Questions. 
A user 'Admin' (Teacher) can check the marks of all listed students.

A non-Admin user (Student) after registration/login can participate in online quiz and check his/her performance on leaderboard.


# Prerequisites

Please run requirements.txt  to install required modules in your local machine.
* [pip install -r requirements.txt]


Current Admin details->
	Username-> Admin
	Password-> Test123

# Run the code base

We are running flask app on 2 ports 
1. For Login/Registration and template rendering we are using app.py. Run the command
* python app.py

2. We are using Flask RestPlus module for Rest API's. Run the command
* python main_rest_app.py

