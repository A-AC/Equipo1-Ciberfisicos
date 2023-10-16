import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

import os
import sys
import time
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI
arm = ""

def seq1():
    speed = 50
    arm.set_servo_angle(angle=[10.4, -24.2, -53.8, -0.1, 63.8, 46], speed=speed, wait=True)
    print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
    arm.set_servo_angle(angle=[102.5, -23.8, -53.4, -0.1, 63.8, 46], speed=speed, wait=True)
    print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

def seq2():
    speed = 50
    arm.set_servo_angle(angle=[10.4, -24.2, -53.8, -0.1, 63.8, 46], speed=speed, wait=True)
    print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
    arm.set_servo_angle(angle=[59.5, -25.5, -81.3, -0.1, 63.8, 46], speed=speed, wait=True)
    print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))


def disc():
    global arm
    arm.disconnect()

def setseq():
    global arm
    """
    Just for test example
    """
    if len(sys.argv) >= 2:
        ip = sys.argv[1]
    else:
        try:
            from configparser import ConfigParser
            parser = ConfigParser()
            parser.read('../robot.conf')
            ip = parser.get('xArm', 'ip')
        except:
            ip = input('Please input the xArm ip address:')
            if not ip:
                print('input error, exit')
                sys.exit(1)

    arm = XArmAPI(ip)
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)


# Create the main window with a larger initial size
root = tk.Tk()
root.title("Secuencias de Xarm")
root.geometry("600x400")  # Set the initial window size

# Create a frame for the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Create two buttons and place them in the button frame
button1 = ttk.Button(button_frame, text="Secuencia 1", command=seq1)
button2 = ttk.Button(button_frame, text="Secuencia 2", command=seq2)
button3 = ttk.Button(button_frame, text="Power ON", command=setseq)
button4 = ttk.Button(button_frame, text="Disconnect", command=disc)
button3.grid(row=0, column=1, padx=10)
button1.grid(row=0, column=0, padx=10)
button2.grid(row=0, column=2, padx=10)
button4.grid(row=1, column=1, padx=10)

# Load and scale down the image (replace 'your_image.png' with the actual image file)
image = PhotoImage(file='tec.png')
image = image.subsample(4)  # Scale the image down by a factor of 4

image2 = PhotoImage(file="power.png")
image2 = image2.subsample(8) 
button3.config(image=image2)

# Create a label to display the scaled image
image_label = ttk.Label(root, image=image)
image_label.pack()

copyright_label = ttk.Label(root, text="© 2023 Roboindustriales. All Rights Reserved.")
copyright_label.pack(side=tk.BOTTOM, pady=10)

# Center the image label in the middle of the window
root.update_idletasks()
image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Start the Tkinter main loop
root.mainloop()