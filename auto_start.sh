#!/bin/bash

#gnome-terminal -- bash -c "echo \"1asdf\"; exec bash"
#gnome-terminal -- bash -c "sleep 6;echo \"afasdf\"; exec bash"
# source ROS environment
source /opt/ros/melodic/setup.bash
source ~/tp_sep25/devel/setup.bash
sleep 2
#Launch roscore
gnome-terminal -- bash -c "roscore; exec bash;"
sleep 7
#luanch jupiter bringup
#gnome-terminal -- tab -- bash -c "roslaunch jupiterobot_bringup jupiterobot_bringup.launch; exec bash;"
#sleep 7

#Launch Jupiter
gnome-terminal --tab -- bash -c "roslaunch jupiterobot_bringup jupiterobot_bringup.launch; exec bash;"
sleep 7
#Launch map
gnome-terminal --tab -- bash -c "roslaunch jupiterobot_navigation rplidar_amcl_demo.launch map_file:=/home/mustar/tp_sep25/robot_lab_sep25.yaml; exec bash;"
sleep 7
#Launch Rviz
gnome-terminal --tab -- bash -c "roslaunch turtlebot_rviz_launchers view_navigation.launch; exec bash;"
sleep 7
# #Localize
gnome-terminal --tab -- bash -c "rostopic pub -1 /initialpose geometry_msgs/PoseWithCovarianceStamped '{header: {frame_id: "map", stamp: now}, pose: {pose: {position: {x: -0.28, y: -0.17,  z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.066, w: 0.9984}}}}'; exec bash;"
sleep 7
# #Launch waypoint navigation 
gnome-terminal --tab -- bash -c "source ~/tp_sep25/devel/setup.bash; roslaunch follow_waypoints follow_waypoints.launch; exec bash;"
sleep 7
# # #Launch Astra
gnome-terminal --tab -- bash -c "roslaunch rchomeedu_vision multi_astra.launch; exec bash;"
sleep 7
# # #Launch Yolo
# # gnome-terminal -- bash -c "roslaunch robot_vision_openvino yolo_ros.launch; exec bash;"
# # sleep 7
# # #Launch Script
# # gnome-terminal -- bash -c "~/tp_ws/src/tp_sep23/scripts/obj_det_ctrl3.py; exec bash;"
# gnome-terminal -- bash -c "source ~/tp_ws/devel/setup.bash; rosrun serial_listener lux_recorder_node.py  > /home/mustar/team1_log_file.txt; exec bash;"
# sleep 7

# # sleep 7
# gnome-terminal -- bash -c  "rosrun follow_waypoint follow_waypoint.py"
# # Launch Journey

#gnome-terminal -- bash -c "rostopic pub /start_journey std_msgs/Empty -1; exec bash;"

gnome-terminal --tab -- bash -c "source ~/tp_sep25/devel/setup.bash; rosrun jupiter_autostart recognizer_display.py; exec bash"
sleep 5

gnome-terminal --tab -- bash -c "source ~/tp_sep25/devel/setup.bash; sh ~/tp_sep25/MCI_autostart.sh; exec bash"
sleep 4

gnome-terminal --tab -- bash -c "source ~/tp_sep25/devel/setup.bash; roslaunch rchomeedu_arm arm.launch; exec bash"
sleep 4

gnome-terminal --tab -- bash -c "source ~/tp_sep25/devel/setup.bash; rosrun arm_control_pkg 5DOF_robot.py; exec bash"
sleep 4

