"""
   Servo Example - Example of usage ASMpi class

.. Licence MIT
.. codeauthor:: Jan Lipovský <janlipovsky@gmail.com>, janlipovsky.cz
"""
import keyboard  # Using module keyboard
from AMSpi import AMSpi
import time

amspi = AMSpi(use_board=False)


def init():
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"

    # Set PINs for controlling shift register (GPIO numbering)
    amspi.set_74HC595_pins(21, 20, 16)
    # Set PINs for controlling all 4 motors (GPIO numbering)
    amspi.set_L293D_pins(5, 6, 13, 19)


def move_forward(forward_time, forward_speed=None):
    print("GO: clockwise")
    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], speed=forward_speed)
    time.sleep(forward_time)
    print("Stop")
    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])


def move_backward(back_time, back_speed=None):
    print("GO: counterclockwise")
    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False,
                        speed=back_speed)
    time.sleep(back_time)
    print("Stop")
    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])


def move_right(right_time, right_speed=None):
    print("Turn right")
    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2], clockwise=False, speed=right_speed)
    amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_4], speed=right_speed)

    time.sleep(right_time)
    print("Stop")
    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])


def move_left(left_time, left_speed=None):
    print("Turn left")
    amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2], speed=left_speed)
    amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False, speed=left_speed)
    time.sleep(left_time)
    print("Stop")
    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])


if __name__ == '__main__':

    init()
    move_forward(forward_time=0.1)
    move_backward(back_time=0.1)
    move_right(right_time=0.1)
    move_left(left_time=0.1)

    while True:  # making a loop
        print('waiting')
        try:  # used try so that if user pressed other than the given key error will not be shown
            k = input()
            if k == 'w':  # if key 'q' is pressed
                move_forward(forward_time=0.1)
            elif k == 's':  # if key 'q' is pressed
                move_backward(back_time=0.1)
            elif k == 'd':  # if key 'q' is pressed
                move_right(right_time=0.1)
            elif k == 'a':  # if key 'q' is pressed
                move_left(left_time=0.1)
            elif k == 'q':  # if key 'q' is pressed
                print('You Pressed Q Key!')
                break  # finishing the loop
            else:
                pass
        except:
            break  # if user pressed other than the given key the loop will break
