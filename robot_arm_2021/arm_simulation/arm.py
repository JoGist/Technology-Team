import roboticstoolbox as rtb
from roboticstoolbox import DHRobot, RevoluteMDH, ERobot, ELink, ETS
from spatialmath import SE3
from roboticstoolbox.tools.trajectory import tpoly,lspb
from math import pi as pi
import numpy as np

# DH parameters
a = [0, 0, 1.2, 0, 0.8, 0]
d = [0, 0, 0, 0, 0, 0]
alpha = [0, pi/2, 0, pi/2, pi/2, pi/2]

robot = DHRobot([RevoluteMDH(d[0], a[0], alpha[0]),
    RevoluteMDH(d[1], a[1], alpha[1]),
    RevoluteMDH(d[2], a[2], alpha[2]),
    RevoluteMDH(d[3], a[3], alpha[3]),
    RevoluteMDH(d[4], a[4], alpha[4]),
    RevoluteMDH(d[5], a[5], alpha[5])],
    name='6R')

time = np.array(range(1,100))

T1 = robot.fkine([pi/2, pi/3, -pi/2, 0, 0, 0])
T2 = robot.fkine([-pi/2, pi/6, -pi/3, pi/4, 3, 3])

#[q_des_1, qd_des_1, qdd_des_1] = robot.jtraj(T1=T1, T2=T2, t=time)
trajectory = robot.jtraj(T1=T1, T2=T2, t=time)
print(robot.jtraj(T1=T1, T2=T2, t=time))

#figure("Name", "animation")

# trajectory.qd returns velocity
# trajectory.qdd returns acceleration
DHRobot.plot(robot, trajectory.q, movie='animation_tech_robot.mp4')
