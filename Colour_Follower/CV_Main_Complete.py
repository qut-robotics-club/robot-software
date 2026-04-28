
import cv2
from mobility import Motor

"Comment / Uncomment these lines depending if you are working on a pi or computer"
import picamera
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)

MotorA = Motor(26, 20)
MotorB = Motor(19,16)

#import all the relevant functions
from CV_Find_Object_Complete import find_object
from CV_Find_Contours_Complete import find_contours
from CV_Caculations_Complete import caculate_distance, caculate_position
from CV_Focal_Length_Complete import caculate_focal_Length
from CV_Draw_Info_Complete import draw_information 

"Below is the function that applys all the above imports to process our frame, you wont need to edit this stuff but feel free to have a look"

FOCAL_LENGTH = 320#caculate_focal_Length()


def process_frame(frame):
    #Process a given camera frame

    imageObject = find_object(frame)

    contours, width_List_px = find_contours(imageObject[0])

    item_not_found = width_List_px[0] == -1
    
    if(item_not_found):
        return frame, imageObject, [None]

    box_details = []

    for box_id in range(len(width_List_px)):

        distance = caculate_distance(FOCAL_LENGTH, width_List_px[box_id])
        
        pos_x, pos_y, height_px, width_px = caculate_position(contours[box_id])

        updated_frame = draw_information(frame, pos_x, pos_y, width_px, height_px, distance)

        box_details.append({"dist" : distance, "x" : pos_x, "y" : pos_y})

    return updated_frame, imageObject, box_details



"*** DO NOT EDIT THIS CODE ***"
"*** The below code creates the website to view the camera Feed, and is easily broken ***"

import cv2
import threading
from flask import Flask, Response, render_template

app = Flask(__name__)


capture_frames = True 


#Main function to process the frames
def generate_frames(idx):
    cap = cv2.VideoCapture(0)

    while capture_frames:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            frame = cv2.flip(frame, -1)
            prsdFrame, imageOut, boxInfo = process_frame(frame)
            
            try:
                pos_x = boxInfo[0]['x']
                pos_y = boxInfo[0]['y']
                dist = boxInfo[0]['dist']
                
                if 190 <= pos_x <= 430: #forward
                    MotorA.forward(50)
                    MotorB.forward(50)
                    
                elif pos_x < 190:
                    MotorB.forward(10)
                    MotorA.backward(10)
                    
                elif  pos_x > 430:
                    MotorA.forward(10)
                    MotorB.backward(10)
                else:
                   MotorA.forward(0)
                   MotorB.forward(0)
            except:
                MotorA.forward(0)
                MotorB.forward(0)

            if idx == 1:
                _, buffer = cv2.imencode('.jpg', prsdFrame)
            else:
                _, buffer = cv2.imencode('.jpg', imageOut[idx - 2])

        frame_data = buffer.tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


#Localised  HTML for all video streams
@app.route('/')
def index():
    return render_template('index.html', num_streams=2)


#Each video stream is ot putted to a specific page
@app.route('/video_feed_0')
def video_feed_0():
    return Response(generate_frames(1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_1')
def video_feed_1():
    return Response(generate_frames(2), mimetype='multipart/x-mixed-replace; boundary=frame')

#@app.route('/video_feed_2')
#def video_feed_2():
#    return Response(generate_frames(3), mimetype='multipart/x-mixed-replace; boundary=frame')


#Start the web page and the threading to improve efficency
if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0')
    capture_frames = False  # Stop capturing frames when the app exits
   


