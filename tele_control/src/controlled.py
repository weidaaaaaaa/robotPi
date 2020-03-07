#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from tele_control.msg import go
from gpio_control import gpio_controller


def goInfoCallback(goto_msg):
    key = goto_msg.go.strip("'")
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
