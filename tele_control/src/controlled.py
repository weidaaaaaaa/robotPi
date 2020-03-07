#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from tele_control.msg import go
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

bl_pwm = 0
br_pwm = 26
bl_1 = 5
bl_2 = 6
br_1 = 13
br_2 = 19

fl_pwm = 21
fr_pwm = 7
fl_1 = 20
fl_2 = 16
fr_1 = 12
fr_2 = 1

outpulist = [bl_pwm, br_pwm, bl_1, bl_2, br_1, br_2, fl_pwm, fr_pwm, fl_1, fl_2, fr_1, fr_2]

GPIO.setup(outpulist, GPIO.OUT, initial=GPIO.LOW)
init_freq = 490
go_dc = 10
turn_dc = 20
stop_dc = 0
pwm_bl = GPIO.PWM(bl_pwm, init_freq)
pwm_br = GPIO.PWM(br_pwm, init_freq)
pwm_fl = GPIO.PWM(fl_pwm, init_freq)
pwm_fr = GPIO.PWM(fr_pwm, init_freq)
pwm_bl.start(stop_dc)
pwm_br.start(stop_dc)
pwm_fl.start(stop_dc)
pwm_fr.start(stop_dc)


def gpio_controller(key):
    if key == go.forward:
        print('forward')
        pwm_bl.ChangeDutyCycle(go_dc)
        pwm_br.ChangeDutyCycle(go_dc)
        pwm_fl.ChangeDutyCycle(go_dc)
        pwm_fr.ChangeDutyCycle(go_dc)
        GPIO.output(bl_1, GPIO.HIGH)
        GPIO.output(bl_2, GPIO.LOW)
        GPIO.output(br_1, GPIO.HIGH)
        GPIO.output(br_2, GPIO.LOW)
        GPIO.output(fl_1, GPIO.HIGH)
        GPIO.output(fl_2, GPIO.LOW)
        GPIO.output(fr_1, GPIO.HIGH)
        GPIO.output(fr_2, GPIO.LOW)

    elif key == go.left:
        print('left')
        pwm_fr.ChangeDutyCycle(turn_dc)
        pwm_br.ChangeDutyCycle(turn_dc)
        # GPIO.output(bl_1, GPIO.HIGH)
        # GPIO.output(bl_2, GPIO.LOW)
        # GPIO.output(br_1, GPIO.HIGH)
        # GPIO.output(br_2, GPIO.LOW)
        # GPIO.output(fl_1, GPIO.HIGH)
        # GPIO.output(fl_2, GPIO.LOW)
        # GPIO.output(fr_1, GPIO.HIGH)
        # GPIO.output(fr_2, GPIO.LOW)

    elif key == go.right:
        print('right')
        pwm_fl.ChangeDutyCycle(turn_dc)
        pwm_bl.ChangeDutyCycle(turn_dc)
        # GPIO.output(bl_1, GPIO.HIGH)
        # GPIO.output(bl_2, GPIO.LOW)
        # GPIO.output(br_1, GPIO.HIGH)
        # GPIO.output(br_2, GPIO.LOW)
        # GPIO.output(fl_1, GPIO.HIGH)
        # GPIO.output(fl_2, GPIO.LOW)
        # GPIO.output(fr_1, GPIO.HIGH)
        # GPIO.output(fr_2, GPIO.LOW)

    elif key == go.back:
        print('back')
        pwm_bl.ChangeDutyCycle(go_dc)
        pwm_br.ChangeDutyCycle(go_dc)
        pwm_fl.ChangeDutyCycle(go_dc)
        pwm_fr.ChangeDutyCycle(go_dc)
        GPIO.output(bl_2, GPIO.HIGH)
        GPIO.output(bl_1, GPIO.LOW)
        GPIO.output(br_2, GPIO.HIGH)
        GPIO.output(br_1, GPIO.LOW)
        GPIO.output(fl_2, GPIO.HIGH)
        GPIO.output(fl_1, GPIO.LOW)
        GPIO.output(fr_2, GPIO.HIGH)
        GPIO.output(fr_1, GPIO.LOW)

    elif key == go.stop:
        print('stop')
        pwm_bl.ChangeDutyCycle(stop_dc)
        pwm_br.ChangeDutyCycle(stop_dc)
        pwm_fl.ChangeDutyCycle(stop_dc)
        pwm_fr.ChangeDutyCycle(stop_dc)
        GPIO.output(bl_2, GPIO.LOW)
        GPIO.output(bl_1, GPIO.LOW)
        GPIO.output(br_2, GPIO.LOW)
        GPIO.output(br_1, GPIO.LOW)
        GPIO.output(fl_2, GPIO.LOW)
        GPIO.output(fl_1, GPIO.LOW)
        GPIO.output(fr_2, GPIO.LOW)
        GPIO.output(fr_1, GPIO.LOW)


def goInfoCallback(goto_msg):
    key = goto_msg.go
    if key:
        rospy.loginfo("robot[%s]", key)
        gpio_controller(key)


def controlled():
    # ROS节点初始化
    rospy.init_node('controlled', anonymous=True)

    # 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/goto_info", go, goInfoCallback)

    # 循环等待回调函数
    rospy.spin()


if __name__ == '__main__':
    controlled()
