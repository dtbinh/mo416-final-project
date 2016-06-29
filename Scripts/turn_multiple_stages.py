# -*- encoding: UTF-8 -*- 

import vrep,time,sys

if __name__ == "__main__":
    #INIT V-REP IMAGE SENSOR	
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.2',19997,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        #Get and display the pictures from the camera
        #Get the handle of the vision sensor
        returnCode = 0;
        outInts=[];outFloats=[];outStrings=[];outBuffer = '';
        inInts=[];inFloats=[];inStrings=[];inBuffer = '';

        states = [0,2,1,2,0,2,1,0,1,0]
		
        i = 0
        #Simulate 10 different states for the traffic light
        while(i < 10):
            state = states[i]
            if(state == 0):
                function = 'turnRed'
            else:
                if(state == 1):
                    function = 'turnYellow'
                else:
                    if(state == 2):
					    function = 'turnGreen'
		    
            returnCode,outInts,outFloats,outStrings,outBuffer=vrep.simxCallScriptFunction(clientID,'Semaforo',vrep.sim_scripttype_childscript,function,inInts,inFloats,inStrings,inBuffer,vrep.simx_opmode_blocking)
            i = i + 1
            time.sleep(10)
