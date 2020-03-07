#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from tele_control.msg import go
import sys, select, termios, tty


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def controller():
    rospy.init_node('controller', anonymous=True)

    goto_info_pub = rospy.Publisher('/goto_info', go, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        key = getKey()
        goto_msg = go()
        if key == go.left.strip("'"):
            goto_msg.go = go.left
            rospy.loginfo('goto:[%s]:left', goto_msg.go)
        elif key == go.right.strip("'"):
            goto_msg.go = go.right
            rospy.loginfo('goto:[%s]:right', goto_msg.go)
        elif key == go.back.strip("'"):
            goto_msg.go = go.back
            rospy.loginfo('goto:[%s]:back', goto_msg.go)
        elif key == go.forward.strip("'"):
            goto_msg.go = go.forward
            rospy.loginfo('goto:[%s]:forward', goto_msg.go)
        elif key == go.stop.strip("'"):
            goto_msg.go = go.stop
            rospy.loginfo('goto:[%s]:stop', goto_msg.go)
        if key == 'o':
            return
        goto_info_pub.publish(goto_msg)

        rate.sleep()


if __name__ == '__main__':
    try:
        settings = termios.tcgetattr(sys.stdin)
        controller()
    except rospy.ROSInterruptException:
        pass
