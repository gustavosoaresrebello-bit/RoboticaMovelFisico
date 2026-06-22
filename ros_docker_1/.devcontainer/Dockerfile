FROM osrf/ros:noetic-desktop-full

# Instala ferramentas adicionais e pacotes do TurtleBot3
RUN apt-get update && apt-get install -y \
    ros-noetic-turtlebot3 \
    ros-noetic-turtlebot3-gazebo \
    ros-noetic-turtlebot3-simulations \
    ros-noetic-turtlebot3-slam \
    ros-noetic-gmapping ros-noetic-map-server \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Inicializa rosdep (evita erro se já existir)
RUN rosdep init || true && rosdep update

# Já adiciona o source do ROS ao bashrc para você não precisar digitar toda hora
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc