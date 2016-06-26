# -*- encoding: UTF-8 -*- 

'''Walk: Small example to make Nao walk'''
import vrep,time,sys
import motion
import time
import array
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

def get_traffic_light_state(im):
    return 'Green'

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
    clientID=vrep.simxStart('127.0.0.2',19999,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        #Get and display the pictures from the camera
        #Get the handle of the vision sensor
        res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,'NAO_vision1',vrep.simx_opmode_oneshot_wait)
        #Get the image
        res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
		
		#Get the traffic light handle
        res3,trafficLightHandle=vrep.simxGetObjectHandle(clientID,'Semaforo',vrep.simx_opmode_oneshot_wait)
        time.sleep(1)
		
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

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

    #START WALKING AT MAX SPEED
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # max speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
    i = 0;
    
	#WHILE THE TRAFFIC LIGHT IS GREEN, KEEP WALKING
	#IF THE TRAFFIC LIGHT IS YELLOW, REDUCE SPEED
	#IF THE TRAFFIC LIGHT IR RED, STOP AND ONLY PROCEED TO WALK WHEN IT IS GREEN AGAIN
    print "Starting the main loop"
    while (vrep.simxGetConnectionId(clientID)!=-1):
        i = i + 1
        #Get the image of the vision sensor
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_oneshot_wait)
        #Transform the image so it can be displayed using pyplot
        #image_byte_array = array.array('b',image)
        #im = I.frombuffer("RGB", (640,480), image_byte_array, "raw", "RGB", 0, 1)
        
		#ROTATE THE IMAGE - IT IS UPSIDE DOWN
        #rotated_im = im.transpose(I.ROTATE_180)
        #traffic_light = get_traffic_light_state(im)
        if i % 3 == 0:
            SlowDown(motionProxy)
        
        if i % 7 == 0:
		    Stop(motionProxy)
		
        if i % 11 == 0:
		    Walk(motionProxy)
		
        time.sleep(1)
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
