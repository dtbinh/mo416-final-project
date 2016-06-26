# -*- encoding: UTF-8 -*- 

import vrep

if __name__ == "__main__":
    #INIT V-REP IMAGE SENSOR	
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.2',19999,True,True,5000,5)
    if clientID!=-1:
        print('Connected to remote API server')
        #Get and display the pictures from the camera
        #Get the handle of the vision sensor
        returnCode = 0;
        outInts=[];outFloats=[];outStrings=[];outBuffer = '';
        inInts=[];inFloats=[];inStrings=[];inBuffer = '';
        returnCode,outInts,outFloats,outStrings,outBuffer=vrep.simxCallScriptFunction(clientID,'Semaforo',vrep.sim_scripttype_childscript,'turnRed',inInts,inFloats,inStrings,inBuffer,vrep.simx_opmode_blocking)
