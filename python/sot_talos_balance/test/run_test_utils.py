'''This module contains utilities for running the tests.'''

from __future__ import print_function

import rospy

from std_srvs.srv import *
from dynamic_graph_bridge.srv import *
from dynamic_graph_bridge_msgs.srv import *

from gazebo_msgs.srv import ApplyBodyWrench
from geometry_msgs.msg import Wrench

runCommandClient = rospy.ServiceProxy('run_command', RunCommand)
runCommandStartDynamicGraph = rospy.ServiceProxy('start_dynamic_graph', Empty)

def launch_script(code,title,description = ""):
    raw_input(title+':   '+description)
    rospy.loginfo(title)
    rospy.loginfo(code)
    for line in code:
        if line != '' and line[0] != '#':
            print(line)
            answer = runCommandClient(str(line))
            rospy.logdebug(answer)
            print(answer)
    rospy.loginfo("...done with "+title)

def format_args(args):
    res = ''
    for a in args:
        res += str(a) + ', '
    if(len(args)>0):
        res = res[:-2]
    return res

def format_kwargs(kwargs):
    res = ''
    for key, value in kwargs.iteritems():
        res += ( '%s=%s, ' % (key, value) )
    if(len(kwargs)>0):
        res = res[:-2]
    return res

def format_args_and_kwargs(args,kwargs):
    if len(args)==0 and len(kwargs)==0:
        return ''
    elif len(kwargs)==0:
        return format_args(args)
    elif len(args)==0:
        return format_kwargs(kwargs)
    else:
        return format_args(args) + ', ' + format_kwargs(kwargs)

def run_test(module,main,*args,**kwargs):
    try:
        rospy.loginfo("Waiting for run_command")
        rospy.wait_for_service('/run_command')
        rospy.loginfo("...ok")

        rospy.loginfo("Waiting for start_dynamic_graph")
        rospy.wait_for_service('/start_dynamic_graph')
        rospy.loginfo("...ok")

        rospy.loginfo("Stack of Tasks launched")

        importline = 'from sot_talos_balance.test import ' + module
        mainargs = format_args_and_kwargs(args,kwargs)
        execline = module + '.' + main +'(' + mainargs + ')'
        initCode = [importline,execline]

        launch_script(initCode,'initialize SoT')
        raw_input("Wait before starting the dynamic graph")
        runCommandStartDynamicGraph()
        print()
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s" % e)

def apply_force(force,duration, body_name = "talos::torso_2_link"):
    '''Gazebo service call for applying a force on a body.'''
    rospy.wait_for_service('/gazebo/apply_body_wrench')
    apply_body_wrench_proxy = rospy.ServiceProxy('/gazebo/apply_body_wrench',ApplyBodyWrench)
    wrench          = Wrench()
    wrench.force.x  = force[0]
    wrench.force.y  = force[1]
    wrench.force.z  = force[2]
    wrench.torque.x = 0
    wrench.torque.y = 0
    wrench.torque.z = 0
    apply_body_wrench_proxy(body_name = body_name, wrench = wrench, duration = rospy.Duration(duration))
