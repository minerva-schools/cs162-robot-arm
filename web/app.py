#Importing All the needed libraries
from __init__ import db, app, login
import os #To handle files path
from flask import Flask, render_template, redirect, request, send_file, g, session #Main Flask
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user #To create the Login
from flask_sqlalchemy import SQLAlchemy #SQL Alchemy to create the database
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import time
import sys
#from .robotmodel.python_to_aduino import forward_kin_end, forward_kin_mid, coordinates_to_angles

#Creating the primary database
class User(UserMixin, db.Model): # A table to store users data
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    student = db.Column(db.Integer) #Equals 1 if this is a student, and 0 otherwise
    logged_in = db.Column(db.Integer, default=0) #Equals 1 if logged in, and 0 if you are not logged in
    in_cue = db.Column(db.Integer, default=0) #Equals 1 if user is waiting for access to the robot arm, and 0 if not
    time = db.Column(db.DateTime, default=datetime.utcnow) #Records the time the user requests access to the robot arm controls
    controller = db.Column(db.Integer, default=0) #Records if someone is using the control room
                                                           
    def __repr__(self):
        return "<Username: {}>".format(self.username)

# Generating the database with the two tables
db.create_all()
db.session.commit()


#The primary functions

"""
This function redirects users to the Login page
"""
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if current_user is not None:
        current_user.logged_in = 0 #update the database
        current_user.controller = 0
        db.session.commit()
        logout_user()      #If logged in, every time you go to the home page you will be automatically logged out
    return render_template('index.html')

@app.route('/observe')
def observe():
    if current_user is not None:
        current_user.in_cue = 0 #update the database
        current_user.controller = 0
        db.session.commit()
    return render_template('observe.html')

@app.route('/help')
def help():
    return render_template("help.html")

@app.route('/logoutallusers')
def logoutallusers():
    list_of_all_users = User.query.all()
    for user in list_of_all_users:
        user.controller = 0
        db.session.commit()
    return redirect('/')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
This the primary function responsible for registering new users
This function assures that the password has at least 8 figures
This function returns an error if the password does not meet the requirements
This function returns an error if the password do not match
This function returns an error if the username already exists in the database
"""
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat = request.form['repeat']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            error = 'This username already exists! please choose a new username'
            return render_template('index.html', error_register=error)
        if len(password) < 8:
            error = 'Your password should be at least 8 symbols long. Please, try again.'
            return render_template('index.html', error_register=error)
        if password != repeat:
            error = 'Passwords do not match. Please, try again.'
            return render_template('index.html', error_register=error)

        # check if user is a student
        if "@minerva.kgi.edu" in username:
            is_student = 1
        else:
            is_student = 0

        # store user information, with password hashed
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), student=is_student)
        db.session.add(new_user)
        db.session.commit()
        register_success_message = 'Registered successful. Please log in'
        return render_template('index.html', message=register_success_message)
    elif request.method == 'GET':
        return render_template('index.html')


"""
This function is responsible for logging users to the server.
This function validates user credentials.
If the user is registered it redirects to the observe page of the robotic arm.
If the user is not registered it displays an error that the user is not registered.
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # check if the user exists
        # Take the password, hash it, and compare it with the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            error = 'The password or the username you entered is not correct!'
            return render_template('index.html', message=error)
        login_user(user)
        user.controller = 0 # update the database
        user.logged_in = 1
        user.time = datetime.now()
        user.in_cue = 1
        db.session.commit()
        return redirect('/waitroom')
        # return render_template('main.html')
    elif request.method == 'GET':
        return render_template('index.html')

"""
This function is responsible for logging users out
"""
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user.logged_in = 0 #update the database
    db.session.commit()
    logout_user()
    return redirect('login')

"""
This functions sends the user to waitroom after they have logged in
"""
@app.route('/waitroom', methods=["GET", "POST"])
@login_required
def waitroom():
    '''
    This function retrieves a list of all users waiting to use the robot arm
    Then it sorts it by who came first, and second by who is a student
    '''
    user_list = User.query.filter_by(logged_in=1).filter_by(in_cue=1).all() #returns the list of users waiting to use the robot
    user_list.sort(key=lambda User: User.time)                  #sorts the list by who came first
    user_list.sort(key=lambda User: User.student, reverse=True) #sorts the list by who is a student
    #print(current_user, file=sys.stderr)
    #print(user_list, file=sys.stderr)
    #print(user_list.index(current_user)+1)
    place_in_line = user_list.index(current_user)
    return render_template("waitroom.html", cue_number=place_in_line)


"""
This is the main room, where the user can observe the stream of the robot arm
This function requires the user to be logged in using his credentials or as guest
"""
@app.route('/main', methods=["GET", "POST"])
@login_required
def home():
    list_of_all_users = User.query.all()
    controllers = 0
    for user in list_of_all_users:
        controllers += user.controller

    if controllers > 0:
        error_message = "Someone is currently using the robot arm. Please wait your turn"
        print(error_message, file=sys.stderr)
        return render_template("index.html", message=error_message)
    else:
        current_user.controller = 1
        g.user = current_user
        return render_template("main.html", myuser=current_user)

@app.route('/main/send_angles', methods=["POST"])
@login_required
def process_angles():
    # angle measures from user
    # these angles are 1st, 2nd, and 3rd joint angle IN DEGREES
    theta1, theta2, theta3 = request.form['theta1'], request.form['theta2'], request.form['theta3']
    # convert to float to work with conversion function
    theta1, theta2, theta3 = float(theta1), float(theta2), float(theta3)

    # export to a txt file
    file_object = open(r"web/sources/command_info.txt", "w")
    for line in [str(int(theta1))+'\n', str(int(theta2))+'\n', str(int(theta3))]:
        file_object.writelines(line)

    # # convert to float to work with conversion function
    # theta1, theta2, theta3 = float(theta1), float(theta2), float(theta3)
    # coordinates of the end effector
    x1, y1, z1 = forward_kin_end(theta1, theta2, theta3)
    # coordinate of the mid joint
    x2, y2, z2 = forward_kin_mid(theta1, theta2, theta3)
    content = {'x1': str(round(x1,2)), 'y1':str(round(y1,2)), 'z1':str(round(z1,2)),
               'x2': str(round(x2,2)), 'y2':str(round(y2,2)), 'z2':str(round(z2,2)),
               'theta1': str(theta1), 'theta2': str(theta2), 'theta3': str(theta3)}
    return render_template("main.html", sent_back_angles=True, **content)

@app.route('/main/send_coordinates', methods=["POST"])
@login_required
def process_coordinates():
    # coordinate measures from user
    x, y, z = float(request.form['x']), float(request.form['y']), float(request.form['z'])
    # converted angles
    theta1, theta2, theta3 = coordinates_to_angles(x, y, z)
    # export to a txt file
    file_object = open(r"web/sources/command_info.txt", "w")
    for line in [str(int(theta1))+'\n', str(int(theta2))+'\n', str(int(theta3))]:
        file_object.writelines(line)

    theta1, theta2, theta3 = str(round(theta1,2)), str(round(theta2,2)), str(round(theta3,2))
    content = {'x': str(x), 'y':str(y), 'z':str(z),
               'theta1': theta1, 'theta2': theta2, 'theta3': theta3}
    return render_template("main.html", sent_back_coordinates=True, **content)

@app.route('/controlroom', methods=["GET"]) #This is a master controlroom that will show information about the users.
@login_required
def controlroom():
    print(current_user, file=sys.stderr)
    print(current_user.username, file=sys.stderr)
    if current_user.username == 'gera@minerva.kgi.edu' or \
                                'mikulas.plesak@minerva.kgi.edu' or \
                                'ara.mkhoyan@minerva.kgi.edu' or \
                                'quang.tran@minerva.kgi.edu' or \
                                'a.kamel@minerva.kgi.edu' or \
                                'arham.hameed@minerva.kgi.edu' or \
                                'psterne@minerva.kgi.edu':
        current_user.controller = 0
        list_of_all_users = User.query.all()
        print('Successfully accessed controlroom.html logged in as user', file=sys.stderr)
        return render_template('controlroom.html', userlist=list_of_all_users)
    else:
        print('Unsuccessfully accessed controlroom.html', file=sys.stderr)
        error_message = 'The control room is only for admin. Please log in'
        return render_template('controlroom.html', userlist=list_of_all_users)

# allows downloading the updated file using url '/download'
@app.route('/download')
def download():
    path = "sources/command_info.txt"
    return send_file(path, as_attachment=True)

#Running the application
if __name__ == "__main__":
    app.run(debug=True)
