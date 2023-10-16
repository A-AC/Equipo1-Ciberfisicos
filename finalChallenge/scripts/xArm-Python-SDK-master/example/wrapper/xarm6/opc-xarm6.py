#!/usr/bin/env python3
import os
import sys
import time
import math   
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

import pywintypes

import OpenOPC

pywintypes.datetime = pywintypes.TimeType

opc = OpenOPC.client()
opc.connect('Kepware.KEPServerEX.V6')    
print(opc.list('codesys.LAPTOP-2UBR64OI.Application.PLC_PRG'))

#######################################################
ip = '192.168.1.228'
class MainProgram():
    def __init__(self):
        self.activate = True
        

    def programsdk1(self):
        print("program1test activated")
        arm = XArmAPI(ip)
        arm.motion_enable(enable=True)
        arm.set_mode(0)
        arm.set_state(state=0)

        arm.reset(wait=True)

        speed = 50
        arm.set_servo_angle(angle=[90, 0, 0, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[90, 0, -60, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[90, -30, -60, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, -30, -60, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, 0, -60, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))


        arm.reset(wait=True)
        speed = math.radians(50)
        arm.set_servo_angle(angle=[math.radians(90), 0, 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[math.radians(90), 0, math.radians(-60), 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[math.radians(90), math.radians(-30), math.radians(-60), 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, math.radians(-30), math.radians(-60), 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, 0, math.radians(-60), 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
        arm.reset(wait=True)
        arm.disconnect()
        self.activate=False
    def programsdk2(self):
        print("program2 activated")
        arm = XArmAPI(ip, is_radian=True)
        arm.motion_enable(enable=True)
        arm.set_mode(0)
        arm.set_state(state=0)
        arm.reset(wait=True)
        speed = 50
        arm.set_servo_angle(angle=[90, 0, 0, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[90, 0, -60, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[90, -30, -60, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, -30, -60, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, 0, -60, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=speed, is_radian=False, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))


        arm.reset(wait=True)
        speed = math.radians(50)
        arm.set_servo_angle(angle=[math.radians(90), 0, 0, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[math.radians(90), 0, math.radians(-60), 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[math.radians(90), math.radians(-30), math.radians(-60), 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, math.radians(-30), math.radians(-60), 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, 0, math.radians(-60), 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=speed, wait=True)
        print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=False))
        arm.reset(wait=True)
        arm.disconnect()
#opc = OpenOPC.client()
# opc.connect('Kepware.KEPServerEX.V6')    
if __name__ == "__main__" :
    main = MainProgram()
    
    while True:
        #opc.write( ('mycodesys.EDISONRICARDO.Application.PLC_PRG.start_program1', 1) )
        #print(opc.read(opc.list('mycodesys.EDISONRICARDO.Application.PLC_PRG')))
        program1= opc.read('codesys.LAPTOP-2UBR64OI.Application.PLC_PRG.start_program1')
        program2= opc.read('codesys.LAPTOP-2UBR64OI.Application.PLC_PRG.start_program2')
        if( program1[0] and not(program2[0])):
            #Activate program1 
    #         print("program1 activated")
            main.programsdk1()
        elif (not(program1[0]) and program2[0] ):
            #Activate program2 
    #         print("program2 activated")
            main.programsdk2()

        else:
            #Stop robot 
            print("robot stopped")
            