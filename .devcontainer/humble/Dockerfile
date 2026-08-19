FROM ros:humble

# Add vscode user with same UID and GID as your host system
# (modified from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
# ubuntu now has a 1000 user ubuntu
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
    
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo \
    git \
    libpoco-dev \
    libsqlite3-dev \
    libyaml-cpp-dev \
    uuid-dev \
    libeigen3-dev \
    nlohmann-json3-dev \
    ros-${ROS_DISTRO}-bondcpp \
    ros-${ROS_DISTRO}-tinyxml2-vendor \
    ros-${ROS_DISTRO}-diagnostic-msgs \
    ros-${ROS_DISTRO}-backward-ros \
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

RUN git clone https://github.com/CollaborativeRoboticsLab/capabilities2.git
RUN git clone https://github.com/CollaborativeRoboticsLab/fabric.git
RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_capabilities.git
RUN git clone https://github.com/CollaborativeRoboticsLab/prompt_tools.git
RUN git clone https://github.com/CollaborativeRoboticsLab/prompt_capabilities.git
RUN git clone https://github.com/CollaborativeRoboticsLab/fp_perception.git
RUN git clone https://github.com/CollaborativeRoboticsLab/fp_perception_capabilities.git
RUN git clone https://github.com/CollaborativeRoboticsLab/nav2_capabilities.git
RUN git clone https://github.com/CollaborativeRoboticsLab/grasping.git
RUN git clone https://github.com/CollaborativeRoboticsLab/tmr_ros2.git
RUN git clone https://github.com/CollaborativeRoboticsLab/omron_amr.git
RUN git clone https://github.com/CollaborativeRoboticsLab/omron_moma.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/moveit2_capabilities.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/grasping_omron_moma.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/supervisor.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_generator_experience.git
# RUN git clone https://github.com/CollaborativeRoboticsLab/fabric_generator_prompttools.git