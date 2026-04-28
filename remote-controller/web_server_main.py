from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
from mobility import Motor
import time


app = Flask(__name__)

turn_rate = 0.9
up_rate = 1
down_rate = 1

left_bias = 1
right_bias = 1

SPEED = 40



MotorA = Motor(26, 20)
MotorB = Motor(19,16)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_state', methods=['POST'])
def update_state():
    state = request.json.get('state', 'stop')

    movement = [0, 0]

    if state == 'stop': #Reset all motion, no movment at all
        movement = [0, 0]

    else: #Some kind of movment so must caculate exactly what
        if 'left' in state:
            movement = [movement[0] - turn_rate, movement[1] + turn_rate]
        elif 'right' in state:
            movement = [movement[0] + turn_rate, movement[1] - turn_rate]
        elif 'up' in state:
            movement = [movement[0] + up_rate, movement[1] + up_rate]
        elif 'down' in state:
            movement = [movement[0] - down_rate, movement[1] - down_rate]
            
    if movement[0] < 0:
        MotorA.backward(abs(movement[0]) * SPEED * left_bias)
    else:
        MotorA.forward(abs(movement[0]) * SPEED * left_bias)
    
    if movement[1] < 0:
        MotorB.backward(abs(movement[1]) * SPEED * right_bias)
    else:
        MotorB.forward(abs(movement[1]) * SPEED * right_bias)

    return jsonify({'status': 'success', 'state': state})



if __name__ == '__main__':
    
    app.run(host = '0.0.0.0', port= 5000)
    
