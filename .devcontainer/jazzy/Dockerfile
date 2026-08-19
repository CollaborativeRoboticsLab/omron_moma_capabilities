FROM ros:jazzy

# Add vscode user with same UID and GID as your host system
# (modified from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
# ubuntu now has a 1000 user ubuntu
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo \
    git \
    curl \
    libpoco-dev \
    libqt5core5t64 \
    libsqlite3-dev \
    libyaml-cpp-dev \
    uuid-dev \
    libeigen3-dev \
    libcurl4-openssl-dev \
    nlohmann-json3-dev \
    python3-yaml \
    qt5-qmake \
    qtbase5-dev \
    libportaudio2 \
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    ros-${ROS_DISTRO}-vision-opencv \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-bondcpp \
    ros-${ROS_DISTRO}-tinyxml2-vendor \
    ros-${ROS_DISTRO}-diagnostic-msgs \
    ros-${ROS_DISTRO}-backward-ros \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-moveit-configs-utils \
    ros-${ROS_DISTRO}-moveit-kinematics \
    ros-${ROS_DISTRO}-moveit-msgs \
    ros-${ROS_DISTRO}-moveit-planners \
    ros-${ROS_DISTRO}-moveit-ros-move-group \
    ros-${ROS_DISTRO}-moveit-ros-visualization \
    ros-${ROS_DISTRO}-moveit-ros-warehouse \
    ros-${ROS_DISTRO}-moveit-servo \
    ros-${ROS_DISTRO}-moveit-setup-assistant \
    ros-${ROS_DISTRO}-moveit-simple-controller-manager \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-nav2-msgs \
    ros-${ROS_DISTRO}-nav2-rviz-plugins \
    ros-${ROS_DISTRO}-navigation2 \
    ros-${ROS_DISTRO}-teleop-twist-keyboard \
    ros-${ROS_DISTRO}-teleop-twist-joy \
    && rm -rf /var/lib/apt/lists/*
    
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch from root to user
USER $USERNAME

# Rosdep update
RUN rosdep update

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

# make sure folders exist
WORKDIR /home/$USERNAME/colcon_ws/src

RUN git clone https://github.com/CollaborativeRoboticsLab/capabilities2.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/fabric.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_capabilities.git -b experience-integration
RUN git clone --recurse-submodules https://github.com/CollaborativeRoboticsLab/prompt_tools.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/prompt_capabilities.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/fp_perception.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/fp_perception_capabilities.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/nav2_capabilities.git -b experience-integration
RUN git clone https://github.com/CollaborativeRoboticsLab/grasping.git
RUN git clone https://github.com/CollaborativeRoboticsLab/grippers.git
RUN git clone https://github.com/CollaborativeRoboticsLab/tmr_ros2.git
RUN git clone --recurse-submodules https://github.com/CollaborativeRoboticsLab/omron_amr.git
RUN git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/moveit2_capabilities.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/grasping_omron_moma.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/supervisor.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/experience.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_generator_experience.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_generator_prompttools.git