# -*- encoding: UTF-8 -*- 

'''Walk: Small example to make Nao walk'''
import vrep,time,sys
import motion
import time
import array
import numpy
import matplotlib.pyplot as plt
from stage_recognizer import StageRecognizer
from PIL import Image as I
from naoqi import ALProxy
	
def Walk(motionProxy):
    #START WALKING AT MAX SPEED
    print "Walkin!!"
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # max speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def Stop(motionProxy):
    #TARGET VELOCITY
    print "Stoping!!"
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =0.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def SlowDown(motionProxy):
    #START WALKING SLOW
    print "Slowing Down!!"
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =0.5 # half speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(robotIP, robotPort):
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

	#INIT V-REP IMAGE SENSOR	
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.2',19998,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        #Get and display the pictures from the camera
        #Get the handle of the vision sensor
        res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,'NAO_vision1',vrep.simx_opmode_oneshot_wait)
        #Get the image
        res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
        #Allow the display to be refreshed
        plt.ion()
        #Initialiazation of the figure
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
        time.sleep(1)
        im = I.new("RGB", (640,480), "white")
        #Give a title to the figure
        fig = plt.figure(1)    
        fig.canvas.set_window_title('NAO_vision1')
        #inverse the picture
        plotimg = plt.imshow(im,origin='lower')
		
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
	
    ## Initilize the StageRecognizer
    rec = StageRecognizer('trained_net_0_15.bin')

    #####################
    ## Enable arms control by Walk algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)
    #~ motionProxy.setWalkArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
    NAO_state = 'stop'
	#WHILE THE TRAFFIC LIGHT IS GREEN, KEEP WALKING
	#IF THE TRAFFIC LIGHT IS YELLOW, REDUCE SPEED
	#IF THE TRAFFIC LIGHT IR RED, STOP AND ONLY PROCEED TO WALK WHEN IT IS GREEN AGAIN
    print "Starting the main loop"
    while (vrep.simxGetConnectionId(clientID)!=-1):
        #Get the image from the vision sensor
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
        time.sleep(1)
        #Transform the image so it can be displayed using pyplot
        image_byte_array = array.array('b',image)
        im = I.frombuffer("RGB", (640,480), image_byte_array, "raw", "RGB", 0, 1)
        #infile = 'D:\_dev\mo416-final-project\Images\Semaforo_verde\img_2016-06-26-11-17-14.png'
        #pil_image = I.open(infile)
        #Update the image
        plotimg.set_data(im)
        #Refresh the display
        plt.draw()
        #The mandatory pause ! (or it'll not work)
        plt.pause(0.001)
        
		#ROTATE THE IMAGE - IT IS UPSIDE DOWN
        pil_image = im.transpose(I.ROTATE_180)
        open_cv_image = numpy.array(pil_image) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        color, precision = rec.recognize_image(open_cv_image)
        print 'Color:' + color + ' / Precision:' + precision
		
        if color == 'yellow' and NAO_state != 'slowdown':
            SlowDown(motionProxy)
            NAO_state = 'slowdown'
        
        if color == 'red' and NAO_state != 'stop':
            Stop(motionProxy)
            NAO_state = 'stop'
		
        if color == 'green' and NAO_state != 'walking':
            Walk(motionProxy)
            NAO_state = 'walking'
		
		#if (traffic_light == 'Green'):
        #   Walk(motionProxy)
		#else:
		#    if (traffic_light == 'Yellow'):
		#	    SlowDown(motionProxy)
		#	else:
		#	    if (traffic_light == 'Red'):
        #            Stop(motionProxy)
    #####################
    ## End Walk
    #####################
    Stop(motionProxy)


if __name__ == "__main__":
    robotIp = "127.0.0.1"
    robotPort = 8080

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]
        robotPort = sys.argv[2]
    main(robotIp, robotPort)
