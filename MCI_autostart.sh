#!/bin/bash
# Script to launch Nubot MCI System Components for ROS Melodic

# --- Configuration ---
# Workspace setup (Adjust if your username or home directory path differs)
ROS_WS_SETUP="source ~/tp_sep25/devel/setup.bash"

# Directory containing nubot_ui.html
PACKAGE_SCRIPTS_DIR="$HOME/tp_sep25/src/nubot_mci/scripts"

# Command to open a new gnome-terminal tab and execute a sequence of commands
launch_terminal() {
    # The 'bash -c' structure is critical for running commands sequentially
    gnome-terminal --tab --title="$1" -- bash -c "$2; exec bash"
}

echo "Starting Nubot MCI System Components..."
echo "======================================="

# 1. Start ROS Master (roscore) - Required first
# launch_terminal "1. ROSCORE MASTER" "roscore"
# sleep 2

# 2. Start ROS Bridge Server (WebSocket 9090)
launch_terminal "2. ROS BRIDGE (WebSocket 9090)" "$ROS_WS_SETUP; roslaunch rosbridge_server rosbridge_websocket.launch"
sleep 3

# 3. Start Nubot Brain Node (The Logic & Mic Listener)
# NOTE: This includes the sourcing and then running the node.
launch_terminal "3. NUBOT BRAIN NODE" "$ROS_WS_SETUP; rosrun nubot_mci nubot_brain.py"
sleep 4

# 4. Start Python HTTP Server (Serving HTML)
# This command navigates to the directory and starts the server.
launch_terminal "4. HTTP SERVER (127.0.0.1:8000)" "cd $PACKAGE_SCRIPTS_DIR && python -m SimpleHTTPServer 8000"
sleep 1

# 5. Open the Web Browser
google-chrome http://localhost:8000/nubot_ui.html

echo "======================================="
echo "System launch complete. Check terminal windows for logs."
