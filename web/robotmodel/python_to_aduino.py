#Importing all the needed libraries, please note that several libraries are needed to generate machine learning model.

from keras.models import load_model
import numpy as np #To Generate the numby arrays
import math #Used for forward Kinamatics calculations
import matplotlib.pyplot as plt #Used to generate the 3D plots
from matplotlib import pyplot #Used to generate the 3D plots
from mpl_toolkits.mplot3d import Axes3D #Used to generate the 3D plots
import random #used for the dataset generation
import keras #Using Keras library to build the model
from keras import models #Using Keras library to build the model
from keras import layers #Using Keras library to build the model
import tensorflow as tf
# from sklearn.model_selection import train_test_split #used later to split the dataset in training and testing
# import serial #used to communicate with the Arduino
import time  #Used to time some events



#Loads the machine learning model generated to change coordinates into angles
#The machine learning file is included in the same folder as this file
#To examine how this model was generated please refer to the main code included as a jupyter notebook

model = load_model('web/robotmodel/model1.h5')
# model = load_model('model1.h5')
global graph
graph = tf.get_default_graph()


"""
This function is used to find the coordinates of the end effector in 3D space corresponding to any combination
This function is built based on the transformation matrix generated using mathematica shown above

>> Inputs:
        > q1: First joint angle in degrees
        > q2: Second joint angle in degrees
        > q3: Second joint angle in degrees

>> output:
        > X, Y, Z in cm

"""

def forward_kin_end(q1,q2,q3):
    q1 = math.radians(q1) #changes angle from radians
    q2 = math.radians(q2) #changes angle from radians
    q3 = math.radians(q3) #changes angle from radians

    x = 8 * ((1*(math.cos(q1)* math.sin(q2))) #Calculates X coordinate based on the transformation matrix shown above

           + (1*(math.cos(q1)* math.cos(q3)*math.sin(q2)))

           + (1*(math.cos(q1)* math.cos(q2)*math.sin(q3))))


    y = 8 * ((1*(math.sin(q1)* math.sin(q2))) #Calculates Y coordinate based on the transformation matrix shown above

           + (1*(math.cos(q3)* math.sin(q1)*math.sin(q2)))

           + (1*(math.cos(q2)* math.sin(q1)*math.sin(q3))))

    z = 8 * (0.3125                         #Calculates Z coordinate based on the transformation matrix shown above

             + (1*math.cos(q2))

             + (1*(math.cos(q2)* math.cos(q3)))

             - (1*(math.sin(q2)*math.sin(q3))))

    return (x, y, z)



"""
This function calculates the forward kinmatics but for the middle joint this time
This function Changes joints angles into XYZ coordinates for the middle joint
This function is used mainly to be able to represent the arm graphically
To represent the arm graphically we need to change angles into coordinates for each joint
"""

def forward_kin_mid(q1,q2,q3):
    q1 = math.radians(q1)
    q2 = math.radians(q2)

    x = 8 * (math.cos(q1) * math.sin(q2))

    y = 8 * (math.sin(q1) * math.sin(q2))

    z = 2.5 + (8 * math.cos(q2))

    return x, y, z


#This is the main function that uses the machine learning model to change coordinates into joints angles

def coordinates_to_angles(x,y,z):
    posX = x
    posY = y
    posZ = z

    pred = np.array([[posX, posY, posZ]])
    with graph.as_default():
        a = model.predict(pred)
    teta1 = a[0][0]
    teta2 = a[0][1]
    teta3 = a[0][2]
    return teta1, teta2, teta3
# print('HEY',coordinates_to_angles(1,2,3))

"""
This function is used to show the arm graphically in the simplest form possible
The simplest form possible for this robotic arm is representing each joint as a dot and representing each link as a line in 3D space
This function takes the joints angles as inputs
The function then uses forward kinmatics to change angles into XYZ locations for each join to show the real arm location in 3D space
"""

def draw_arm(q1,q2,q3):

    fig = pyplot.figure()
    ax = Axes3D(fig)

    joint1_x, joint1_y, joint1_z = forward_kin_mid(q1,q2,q3)
    joint2_x, joint2_y, joint2_z = forward_kin_end(q1,q2,q3)

    x_vals = [0,0,joint1_x,joint2_x]
    y_vals = [0,0,joint1_y,joint2_y]
    z_vals = [0,2.5,joint1_z,joint2_z]

    ax.set_xlim3d(-16, 16)
    ax.set_ylim3d(-16, 16)
    ax.set_zlim3d(0, 16)
    ax.scatter(x_vals, y_vals, z_vals,s = 400, c = 'black', marker = '.', edgecolors = 'red')
    ax.plot(x_vals, y_vals, z_vals, linewidth=3)
    pyplot.show()



#This is the part that asks the user for input and sends the arm into coordinates in 3D space

# x = input("Which Location do you want to send the arm to?")
# if x == 'm':
#     with serial.Serial('COM3', 9600, timeout=1) as ser:
#         ser.write(b'H')   # send the pyte string 'H'
#         time.sleep(3)   # wait 0.5 seconds
#         ser.write(b'M')   # send the byte string 'L'
#
#
# elif x == 'l':
#     draw_arm(35,30,39)
#     with serial.Serial('COM3', 9600, timeout=1) as ser:
#         ser.write(b'H')   # send the pyte string 'H'
#         time.sleep(3)   # wait 0.5 seconds
#         ser.write(b'L')   # send the byte string 'L'
#
# elif x == 'h':
#     with serial.Serial('COM3', 9600, timeout=1) as ser:
#         ser.write(b'H')   # send the pyte string 'H'
#         time.sleep(3)   # wait 0.5 seconds
#         ser.write(b'H')   # send the byte string 'L'
