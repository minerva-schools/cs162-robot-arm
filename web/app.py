#Importing All the needed libraries
from . import db, app, login
import os #To handle files path
from flask import Flask, render_template, redirect, request, send_file, g, session #Main Flask
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user #To create the Login
from flask_sqlalchemy import SQLAlchemy #SQL Alchemy to create the database
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from .robotmodel.python_to_aduino import forward_kin_end, forward_kin_mid, coordinates_to_angles
#Creating the primary database
class User(UserMixin, db.Model): # A table to store users data
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
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
    return render_template('index.html')

@app.route('/observe')
def observe():
    return render_template('observe.html')

@app.route('/help')
def help():
    return render_template("help.html")


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

        # store user information, with password hashed
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        register_success_message = 'Registered successful. Please log in'
        return render_template('index.html', message=register_success_message)
    elif request.method == 'GET':
        return render_template('index.html')


"""
This function is responsible for logging users in to their personal kanban board
This function validates users credentials, if the user is registered it redirects to the Kanban board
If the user is not registered it displays an error that the user is not registered
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
    logout_user()
    return redirect('login')

"""
This functions sends the user to waitroom after they have logged in
The reason for this addition is that it keeps in mind the scalability of the project
Where in future if more robots are added, we can control the user traffic in each room accordingly
"""

@app.route('/waitroom', methods=["GET", "POST"])
@login_required
def waitroom():
    g.user = current_user
    return render_template("waitroom.html", myuser=current_user)


"""
This is the primary function responsible for displaying the tasks
This function does not allow duplicate tasks to exist
"""
@app.route('/main', methods=["GET", "POST"])
@login_required
def home():
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

# allows downloading the updated file using url '/download'
@app.route('/download')
def download():
    path = "sources/command_info.txt"
    return send_file(path, as_attachment=True)
#Running the application
if __name__ == "__main__":
    app.run(debug=True)
